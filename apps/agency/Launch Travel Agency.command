#!/bin/zsh
set -e
# Local demo never exports tracing, including during a Node/Vite build.
unset OTEL_CONFIG_FILE OTEL_EXPERIMENTAL_CONFIG_FILE
export OTEL_SDK_DISABLED=true
export OTEL_TRACES_EXPORTER=none OTEL_METRICS_EXPORTER=none OTEL_LOGS_EXPORTER=none
cd "$(dirname "$0")"
if [[ -f experiments/openjev-vision/runtime/bin/python && -f experiments/openjev-vision/model-path.txt ]]; then
  .venv/bin/python scripts/start_vision.py --background
fi
if curl --silent --fail --connect-timeout 2 --max-time 3 http://127.0.0.1:8765/api/status >/dev/null; then
  open http://127.0.0.1:8765
  exit 0
fi
if [[ ! -f models/selection.json ]]; then
  echo 'The model is not trained yet. Run uv run python -m travel_lab.run first.'
  exit 1
fi
if [[ ! -d .venv ]]; then uv sync --frozen; fi
if [[ ! -d app/dist ]]; then npm ci --prefix app; npm run build --prefix app; fi
(sleep 3; open http://127.0.0.1:8765) &
exec .venv/bin/python -m travel_lab.serve
