# Run the project

## 1. Explore without loading a model

Use Python 3.12 and Node 22 or later. From the repository root:

```bash
python3 apps/explainer/serve.py
```

Open http://localhost:8770. The visual lessons work immediately. The opening live check needs the services below.

## 2. Restore the complete agency artifact

The member-access `companion-v2` release contains the complete agency bundle, including the active V2 text checkpoint, its immutable freeze record, and the supporting runtime evidence. Sign in with a GitHub account authorized for this private repository. Download it in a browser or use the command below.

```bash
gh release download companion-v2 --repo earlyaidopters/away-together \
  --pattern Away-Together-Complete.zip --dir downloads
python3 tools/restore_companion.py downloads/Away-Together-Complete.zip
```

The restoration tool validates paths and manifest hashes, then adds missing files to apps/agency. It refuses to overwrite differing existing files. The source checkout remains authoritative if a later revision changes code; use a matching release or a separate extraction for historical evidence.

## 3. Run the agency

```bash
cd apps/agency
uv sync --frozen
npm --prefix app ci
npm --prefix app run build
uv run uvicorn travel_lab.serve:app --host 127.0.0.1 --port 8765
```

The text model loads on the first check. Original macOS launchers are also included. Model loading and first-run latency are separate from warm inference timing.

## 4. Enable the photos on Apple silicon

In another terminal, from apps/agency:

```bash
uv run python scripts/start_vision.py --setup --background
```

The launcher verifies pinned OpenJev source, creates its isolated runtime and downloads the pinned MLX image model (approximately 16 GB). It binds to 127.0.0.1:8081. Follow upstream model terms. The image stack uses its own environment so it does not replace the text model’s Transformers version.

Reload the explainer, check the holiday, exclude the stairs photo and run again. The photo-aware 40-offer measurement in evidence is from the original machine, not a promise for yours.

## 5. Test and inspect

```bash
cd apps/agency
uv run pytest tests experiments/v2/tests experiments/next-token/test_engine.py \
  experiments/diffusion/test_engine.py --import-mode=importlib -q
npm --prefix app test
```

Some full experiment commands require large downloads or paid Jev calls. Read their protocol before rerunning. The preserved evidence can be inspected without credentials or fresh paid inference. The old text-only diffusion experiment was mocked/unexecuted; the newer image integration is separately verified.

## Tested machine and recovery

Tested host: Apple M5 Max, 128 GB RAM, macOS 26.5.2. This is not a minimum specification. The vision model download is approximately 16 GB; RAM needs on smaller hosts have not been established. Windows/Linux vision and mobile inference have not been validated.

Run `python3 tools/first_run.py` from the source-kit root to inspect local prerequisites, or `--probe` to check a running agency. A selected model is not proof of successful inference: run a holiday and inspect the fresh receipt. After sleep or a terminated service, restart it and recheck. Keep the app bound to loopback. Do not infer public hosting or unattended operation.
