# OpenJev in one image: vLLM with PR #57250 (DiffusionGemma structured reads)
# plus the Jev-compatible API server. The pin is the PR's head plus three fixes
# that keep the engine alive: vllm-project/vllm#54309 (image input) and two
# sampler fixes (eager fallback after torch.compile's recompile limit; logprob
# stashes of different widths). It also carries #57416, which merged upstream
# after the PR's base. Move back to mmastrac/vllm once the PR carries them.
# The PR only touches Python, so the compiled kernels come from the upstream
# nightly wheel of the fork's merge-base commit: no CUDA build.
FROM nvidia/cuda:13.0.1-devel-ubuntu24.04

ARG VLLM_REPO=https://github.com/razorback16/vllm
ARG VLLM_COMMIT=baa833874881ba62cef99e0c5b716fb136c4a009
ARG VLLM_BASE_COMMIT=36fa72d2d0d2f86c7c83e1e99c9012b7bd26463b

ENV DEBIAN_FRONTEND=noninteractive UV_LINK_MODE=copy PATH=/opt/venv/bin:$PATH \
    UV_PYTHON_INSTALL_DIR=/opt/python
RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /usr/local/bin/uv

RUN git clone --filter=blob:none "$VLLM_REPO" /opt/vllm && git -C /opt/vllm checkout "$VLLM_COMMIT"
RUN uv venv --python 3.12 /opt/venv \
    && cd /opt/vllm && VLLM_USE_PRECOMPILED=1 VLLM_PRECOMPILED_WHEEL_COMMIT="$VLLM_BASE_COMMIT" \
       uv pip install --python /opt/venv/bin/python . \
    && rm -rf /root/.cache/uv

# The API server goes last so a code change only rebuilds a few small layers.
WORKDIR /app
COPY pyproject.toml README.md ./
COPY openjev ./openjev
RUN uv pip install --python /opt/venv/bin/python --no-cache .
COPY docker/entrypoint.sh /usr/local/bin/openjev-entrypoint

ENV PYTHONUNBUFFERED=1 OPENJEV_HOST=0.0.0.0 OPENJEV_PORT=8080
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=900s \
    CMD curl -sf http://127.0.0.1:8080/health || exit 1
ENTRYPOINT ["openjev-entrypoint"]
