# Photo-aware travel decisions

This is a real local OpenJev / DiffusionGemma image integration, added 21 September 2026. The text classifier remains historical V1; the frozen V2 challenger and its benchmark results are unchanged. The pretrained image model was integrated, not trained by this project.

## Run

Apple Silicon with roughly 16 GB free memory for the vision model, in addition to the text service and system overhead. Verified on this M5 Max Mac, not CPU or Windows. Python 3.12 is required by the project.

From the project root after the main `uv sync --frozen` setup:

```bash
.venv/bin/python scripts/start_vision.py --setup --background
.venv/bin/python -m travel_lab.serve
```

Or double-click `Launch Vision.command` once, then `Launch Travel Agency.command`. Setup downloads the pinned approximately 16 GB MLX model into the user's Hugging Face cache. Vision weights are not included in the resource ZIP. The launcher keeps dependencies in a separate runtime so the text model's pinned environment is unchanged. Subsequent agency launches start the configured vision service automatically. Logs are under this directory in server.log. API ports: agency 8765, image model 8081, both loopback only.

The exact source revision, model revision and MLX runtime are in pin.json. vendor-source-manifest.json pins every tracked upstream source file; runtime-requirements.lock.txt records the installed dependencies. The resource includes those sources and licenses, not virtual environments, credentials or machine-specific model paths.

## Use

Every offer has three fictional photos: the existing overview and two new shots, assigned by its destination. There are three sets shared by the 40 fictional offers, not 40 independently photographed hotels. The six added images were generated with the built-in image tool; prompts and hashes are in image-generation.json. Photos are labelled fictional in the app.

Click a photo to include/exclude it, then run a fresh holiday check. Each traveller's drawer has photo preferences. The default Maya avoids entrance stairs, Priya wants visible swimming-pool evidence, Noah wants mountains and Kai wants a garden. The app shows per-photo observations and links each positive visual finding back to its exact source image. Terms-only mode leaves required photo evidence in review; it does not silently waive preferences.

## What the model sees

The backend sends actual PNG bytes and six fixed feature questions, separately for each selected photo. It does not send the filename, caption, destination, generated-image prompt, expected labels, booking policy or reference answer. Features are pool, ocean, mountains, garden, entrance stairs and entrance ramp. Outputs are visible/not_visible/unclear with categorical probabilities. The .8 visible-support threshold is a conservative demonstration rule, not a calibrated correctness guarantee.

The text branch still reads all four terms. Budgets and final combination are application logic. Photos never override a paid-pool clause, refund policy, arrival hours or activity price. Seeing no stairs does not prove a complete step-free route. A visible ramp is only a visible ramp, not accessibility certification. If vision is offline, malformed or no selected image establishes a requested feature, that preference requires review.

OpenJev uses diffusion structured reads with one sample and one denoise step. It may reuse image/prompt prefills, but every photo read executes decision inference; there is no saved-result substitution from disk. Saved replay is explicitly labelled in the app.

Since 22 September 2026 a check first calls `POST /api/vision` for one live read of the selected photos, then `POST /api/decide` with that read's `vision_run_id`. During Scan all 40, offers that share the exact same destination photo selection reuse that one in-memory read from the same server process, so the scan performs three photo reads instead of forty. The server refuses a mismatched photo selection (422) or an unknown/expired read (409). Every decision receipt records `reused_from_run`. Decision `elapsed_ms` is then text inference only; the photo read's own `elapsed_ms` stays in `vision`. Timings must stay separate from old text-only benchmarks.

## Evidence

- real-image-observations.json: real model responses for all nine images, hashes, timing and pinned backend identity.
- output/qa/vision-causal-checks.json: identical text answers across all-photos, stairs-removed and photos-off requests. Maya changes decline to review when stairs are removed; Priya goes to review without pool-photo evidence.
- output/qa/vision-full-scan.json: 40 unique live requests with three photos each completed in approximately 40.7 seconds on this run. Not a general speed benchmark or GPU cold start.
- tests/test_vision.py: fusion, missing evidence, outage, candidate validation, source selection and policy non-override tests.

No broad vision accuracy, booking reliability or superiority claim follows from these selected synthetic examples. The earlier experiments/diffusion text-only comparison remains unexecuted. This image integration is a separate completed lane.
