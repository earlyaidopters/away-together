# DiffusionGemma comparison lane

Status: response adapter implemented; four mock-transport tests pass. No model inference or benchmark result yet. The frozen local classifier evaluation is complete; it failed promotion. This optional lane remains unexecuted.

Sources checked 21 September 2026:
- https://github.com/vllm-project/vllm/pull/57250 (open/unmerged, exact revision in pin.json).
- https://huggingface.co/nvidia/diffusiongemma-26B-A4B-it-NVFP4 (exact model revision in pin.json).

This experimental vLLM change offers fixed-slot structured decisions and a prototype systemone endpoint. Its demonstration uses NVIDIA hardware. Published demonstration timings are author reports, not our travel measurements. The NVIDIA checkpoint targets GPU infrastructure; it is not a drop-in replacement for the current Apple-MPS runtime.

## Comparison protocol

Use identical full documents, questions and candidate descriptions. The adapter excludes gold labels. Report fixed single-read and four-read configurations separately; both use one denoising step and no generated thinking. Select any configuration using development only, calibrate acceptance on calibration only, and freeze its settings and deployment revision before final evaluation. Record actual loaded model revision, precision, hardware, warm-up, concurrency, GPU billing and end-to-end latency. Do not interpret returned confidence or across-read agreement as demonstrated calibration.

The existing travel reliability gates apply unchanged. Public benchmarks remain separate. A diffusion comparison does not qualify our own trained classifier automatically. Never replace missing diffusion measurements with upstream demo figures.

## Deployment state

No Modal/Runpod CLI, relevant environment credentials, or default private config was found in a narrow environment check. Railway CLI exists; its existence does not prove GPU access. The only SSH host alias found was mini, with no evidence it is a compatible GPU server. No paid resource was provisioned, no model downloaded, and no key exposed. This optional lane was not required to resolve the frozen local classifier experiment.

`DiffusionEngine(base_url, samples=1|4)` expects the pinned prototype server at `/v1/systemone`; an optional separate DIFFUSION_API_KEY is read at request time. Never reuse the Jev key for this endpoint. Transport tests validate payload isolation, candidate mapping and malformed-response rejection; they do not establish model quality or server compatibility on actual hardware.
