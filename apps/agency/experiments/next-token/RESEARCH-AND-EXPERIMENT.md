# Direct next-token scoring experiment

Research lock: 21 September 2026. Read the complete article in Codex's internal browser and verified the endpoint against official SGLang documentation. No model or server has been installed or benchmarked for this experiment.

Sources:
- Avi Chawla: https://x.com/_avichawla/status/2101563610644496464
- Official endpoint: https://docs.sglang.io/docs/basic_usage/native_api#v1%2Fscore-decoder-only-scoring

## What transfers

A causal language model can classify by scoring single-token answer labels at the first answer position. SGLang's `/v1/score` takes a query, items, label token IDs, and optional softmax; returned scores follow label-token order. The model still processes the input. Removing the output decoding loop does not remove prefill cost, improve the underlying model automatically, or reproduce Jev's training/calibration.

Our DeBERTa classifier already returns distributions without autoregressive generation. Replacing its runtime with this technique is therefore not an established speed improvement. The useful new candidate is an instruction-tuned causal model making the same travel decisions without task-specific fine-tuning. This tests a different pretrained foundation and separates gains from fine-tuning from gains from choosing a better base model.

## Bounded development experiment

1. After the existing GPU diagnostics/calibration finish, select one non-reasoning instruction model with accessible full logits. The article uses Qwen3-4B-Instruct-2507, a candidate to verify and pin before download. Prefer a verified local-compatible runtime; use SGLang on suitable external hardware only when that materially helps. Do not assume SGLang or the existing Ollama API exposes this path on this Mac.
2. Pin model revision, tokenizer, chat template, precision, runtime and prompt. Render the actual assistant answer boundary, disable reasoning using supported model settings, and verify that each continuation label is exactly one token at that boundary. Standalone tokenization of `A` alone is insufficient to verify template/whitespace behavior. Use complete semantic candidate descriptions in the prompt; never expose gold, family tags, or selected source clauses.
3. Score three labels corresponding to the existing meets/violates/unknown candidates. Preserve full documents and reject overlong inputs. Normalize the three logits, return the existing engine schema, and retain raw scores, runtime configuration and timing. Check all scores are finite and candidate mapping is correct.
4. Evaluate on the existing development set against reference labels. Run a small preregistered candidate-order permutation diagnostic to expose letter/position bias. Select prompts/order only on development; preserve failures. Do not inspect any final test to choose this candidate.
5. If competitive, fit confidence calibration using the disjoint calibration split, with the existing acceptance-error and coverage gates. Score concentration is not probability of correctness. Preserve explicit unknown and abstention behavior.
6. Only a frozen candidate may enter fresh Jev head-to-head evaluation. Retain the existing accuracy interval, macro F1, false-accept and coverage requirements. A hybrid fallback would be a separately frozen system with its full latency/cost, not a hidden improvement to the classifier's standalone score.

## Visual and benchmark lesson

The article's two-lane race compares next-token scoring with text generation on the same model; its lane called Jev-style is not a call to the real Jev API. Its generation lane requests an explanation (up to 32 tokens), and concurrent lanes share the inference server. Those measurements cannot establish our speedup over Jev, isolate decoding cost, or demonstrate an accuracy advantage.

For our filming surface, consider three clearly named contestants: trained classifier, untuned next-token scorer, and actual Jev API. Each should visibly process identical holiday/customer decisions and finish with ranked results, correctness, elapsed time and acceptance coverage. Use real observed timings. If adding a same-model scoring-versus-generation demonstration, include both label-only and explanation-generation baselines, benchmark lanes separately with controlled warmup/cache/order/concurrency, and label any concurrent race as a contention demo. Never accelerate playback without disclosure.

Status: research and experiment specification only. No speed or accuracy gain claimed. Existing training and localhost app remain intact.

## Implementation checkpoint

Later on 21 September: downloaded the complete official Qwen3-4B-Instruct-2507 checkpoint at revision `cdbee75f17c01a7cc42f958dc650907174af0554`. Implemented a direct Transformers next-token adapter, using float16 MPS on this Mac, SDPA attention, no KV cache and only the final-position logits. This implements the scoring operation locally without requiring a new SGLang deployment.

The real pinned tokenizer passed exact chat-boundary checks on all 1,600 ordinary development decisions (maximum 328 tokens). Three CPU regression tests using a tiny randomly initialized Qwen architecture passed. They establish adapter invariants, not pretrained-model accuracy. The queued runner additionally checks actual pretrained batch/serial parity before evaluating 544 combined development scenarios and a 12-case candidate-order diagnostic. It records model/source/evaluator hashes and runtime versions. Probabilities remain uncalibrated and automatic acceptance is disabled in this initial comparison.

Run state is in `controller-status.json`; the runner waits for the deeper DeBERTa experiment to finish before loading GPU weights. No pretrained inference result yet at this checkpoint. Do not launch a second GPU evaluation while the controller is active.
