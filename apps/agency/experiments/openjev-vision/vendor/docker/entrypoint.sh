#!/usr/bin/env bash
# Starts vLLM on 127.0.0.1:8000, waits for the model to load, then serves the
# OpenJev API on :8080. If either process exits, the container exits too.
# Set OPENJEV_UPSTREAM to use an existing vLLM server instead.
set -euo pipefail

if [[ -n "${OPENJEV_UPSTREAM:-}" ]]; then
  exec python -m openjev
fi

MODEL="${OPENJEV_MODEL:-nvidia/diffusiongemma-26B-A4B-it-NVFP4}"
export OPENJEV_TOKENIZER="${OPENJEV_TOKENIZER:-$MODEL}"
export OPENJEV_CANVAS="${OPENJEV_CANVAS:-64}"

vllm serve "$MODEL" \
  --served-model-name dgemma \
  --host 127.0.0.1 --port 8000 \
  --diffusion-config "{\"canvas_length\": ${OPENJEV_CANVAS}}" \
  --max-logprobs 32 \
  --limit-mm-per-prompt "{\"image\": ${OPENJEV_MAX_IMAGES:-8}, \"video\": 0}" \
  --enable-auto-tool-choice --tool-call-parser gemma4 --reasoning-parser gemma4 \
  --override-generation-config '{"max_new_tokens": null}' \
  --enable-prefix-caching \
  --async-scheduling \
  --attention-backend TRITON_ATTN \
  --max-num-seqs "${OPENJEV_MAX_NUM_SEQS:-64}" \
  --max-model-len "${OPENJEV_MAX_MODEL_LEN:-65536}" \
  --gpu-memory-utilization "${OPENJEV_GPU_UTIL:-0.9}" \
  ${OPENJEV_VLLM_ARGS:-} &
vllm_pid=$!
trap 'kill -TERM $(jobs -p) 2>/dev/null; wait' TERM INT

echo "openjev: waiting for vLLM to load $MODEL"
until curl -sf http://127.0.0.1:8000/health >/dev/null; do
  kill -0 "$vllm_pid" 2>/dev/null || { echo "openjev: vLLM exited during startup" >&2; exit 1; }
  sleep 5
done

python -m openjev.warmup
python -m openjev &
wait -n
echo "openjev: a process exited; stopping" >&2
kill -TERM $(jobs -p) 2>/dev/null || true
wait
exit 1
