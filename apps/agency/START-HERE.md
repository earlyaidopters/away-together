# Your travel agency is ready to demo

**Frozen final result, 21 September 2026:** The V2 DeBERTa FP16 challenger scored **95.28%** versus **98.61%** for fresh Jev calls on 360 scenarios and 1,440 policy decisions per engine. Its paired accuracy gap was -3.33 percentage points (95% interval -4.38 to -2.29). Other registered quality and coverage floors passed, but the superiority gate failed. V2 was not promoted, conditional replication was not launched, and no replacement seed or final-error tuning followed. The agency remains on V1; the model page displays V2 evidence separately. Read the [final challenger report](output/benchmarks/FROZEN-V2-RESULTS.md) and [reference audit history](experiments/v2/final/round1-deeper-fp16/REFERENCE-VALIDATION.md).

The references are synthetic and model-assisted, without human validation. All 360 cases remained. Original drafts, 52 factual/wording repairs, seven unchanged re-audits and two non-unanimous writer-assisted adjudications are preserved.

Open http://127.0.0.1:8765 while the server is running. If stopped, double-click `Launch Travel Agency.command` in this folder. Everything needed for the selected local model is saved here; the demo does not require Jev or another generation API.

## Best 90-second demonstration
1. Press R to reset. Choose Four friends.
2. Keep Atlantic hideaway selected. Click Check this holiday. Maya, Leo and Priya match; Noah declines.
3. The completed check opens Results automatically. Click Noah’s decline to inspect the guided-hike exclusion. Close the panel.
4. Choose Find the best of all 40 from Results. The scan opens a ranked results page when complete, including the strongest group fit and each traveller’s cheapest matching option. P pauses/resumes the visual reveal; R stops the scan and resets the scene. Every offer check runs the local model again.
5. Open Inside the model for recorded comparisons and inspect actual errors. Replay saved run is explicitly a replay; use fresh Check/Scan for filming. Show results now bypasses the reveal; Stop and view ends a scan with its completed results. Failed requests time out after 45 seconds instead of waiting forever.

Profiles are editable. The catalogue, people and pictures are fictional. A match means the model/code checks passed, not a real booking recommendation. Forty offers reuse eight policy patterns with price variations. Four policy classifications per offer are shared across twelve client profiles.

## Historical V1 build and measurements
- Trained and saved two approaches locally. The selected pretrained NLI model was adapted for about 6.3 minutes; the unsuccessful earlier route took about 15.7 minutes. Whole build time includes much more than training.
- Main synthetic travel test: local 66.5%, Jev 96.25%. Local median 103 ms versus Jev 174 ms under this run's conditions.
- 1,100 fresh scored Jev requests plus four warmups. Estimated API cost including warmups about $0.0472, based on reported tokens and published input pricing, not an invoice.
- Local model failed the quality gate. This is an honest experimental build and filmed comparison, not an autonomous booking product.
- Independent public tests completed. Official TypeSafe benchmark reproduction is explicitly unavailable; no independent dataset is passed off as official.

## Frozen challenger evidence

V2 uses complete documents and a frozen 512-token refusal policy, with FP16 inference selected before final generation. Its fresh travel median was 98.6 ms versus 165.6 ms for remote Jev requests. These exclude checkpoint loading and browser time. The development FP16 experiment approximately halved warm model latency with zero changed choices across 2,176 decisions. This is not the active agency model or its measured HTTP speed.

V2 accepted 393 decisions with zero observed errors and recovered 83.44% of reference-meets decisions. Zero observed errors does not establish zero population risk. Public benchmarks are reported separately in the challenger report, including failures in denominators.

The bundle includes the unpromoted challenger checkpoint so the result can be reproduced. Use `scripts/report_frozen.py` to regenerate its report from preserved raw receipts without new Jev calls. Use `experiments/v2/seal_repaired_round1.py` to verify the repaired corpus seal; do not resume the original generator over repaired drafts.

## Files
- `production/FILMING-GUIDE.md` and `output/pdf/FILMING-GUIDE.pdf`: editable script and filming PDF.
- `output/benchmarks/index.html`, `RESULTS.md`, PNG/SVG charts, metrics.csv and summary.json: measured results.
- `runs/evaluation/*.jsonl`: raw predictions and per-request evidence.
- `models/selection.json`, `MODEL-CARD.md`: exact model and limits.
- `production/TRAVEL-AGENCY-END-TO-END-PLAN.md`: original research/build plan.
- `production/ASTRA-BUILD-PROMPT.md`: reusable initial specification; historical planning wording is not current status.
- `output/resource/`: packaged companion files and manifest.
- `output/qa/`: tests, browser and production checks.

## Reproduce
From this folder, install uv and Node if needed, then `uv sync --frozen`. Build the frontend with `cd app && npm ci && npm run build`, then return to this folder. Run `uv run python -m travel_lab.serve`. The launcher uses the already prepared environment and compiled app.

Training/evaluation controller: `uv run python -m travel_lab.run --config config/run.yaml`. Read config and research/JEV-COMPARISON-STATUS.md first; fresh Jev evaluation consumes the existing account. For local-only reruns use `--skip-jev`. Existing completed stages resume using the recorded run ID. To train a new experiment, preserve the shipped frozen model/results in a separate copy first.

Tests: `.venv/bin/python -m pytest tests -q`. Report-only regeneration: `.venv/bin/python -m travel_lab.report`. No new API calls for reports.

Combined V1/V2 checks: `.venv/bin/python -m pytest --import-mode=importlib tests experiments/v2/tests -q`. The import mode prevents two existing `test_freeze.py` modules from colliding during collection. V2 experiment reproduction is documented in `experiments/v2/PROTOCOL.md`; do not rerun training over the frozen checkpoint.

Full-agency timing: `scripts/benchmark_agency.py` records unique fresh HTTP requests, model latency and client wall time separately. Wait for other inference to finish before measuring. A cold run requires a freshly restarted server that reports `engine_loaded=false`; the script refuses to label a loaded model as cold. The earlier precision speedup excludes HTTP and browser time. Final active-V1 measurements: 10.1-second cold first HTTP request; 105 ms warm HTTP median; three complete forty-offer scans in 4.0, 4.2 and 4.5 seconds. All 121 requests were unique live runs, with zero failures. See output/qa/agency-http-final-20260921/report.json.

Archive validation: `scripts/verify_resource.py` checks exact manifest coverage and file hashes, scans for credential patterns without printing values, and extracts into a new directory. This is separate from the required offline runtime test. Packaging retains prior ZIPs under `output/resource/history/`.

## Hosting
Training and inference ran on the local Mac; no external GPU training or hosting was performed. The earlier text-only diffusion comparison is unexecuted. The new OpenJev image integration now runs locally on Apple Silicon; its selected-photo smoke checks do not establish general image accuracy. The optional Dockerfile is a starting point for a remote CPU deployment, not a verified hosted service. A remotely exposed app needs access controls and resource limits before deployment. Keep the localhost version for filming. No paid cloud service was provisioned.

## Photo-aware revision, 21 September 2026

The agency now uses real local OpenJev / DiffusionGemma image inference alongside the existing V1 text classifier. Each destination has three fictional listing photos, with selectable image evidence and editable traveller photo preferences. Run `Launch Vision.command` once to set up the pinned Apple Silicon backend, then launch the agency. The additional model download is about 16 GB and is not included in the ZIP. It runs in a separate environment on localhost:8081. Photo observations do not establish prices, free access, availability or accessibility. Missing evidence requires review. See `experiments/openjev-vision/README.md` for source pins, installation, real run receipts and limits. The historical V2 text comparison is unchanged; this is not a new Jev superiority result.
