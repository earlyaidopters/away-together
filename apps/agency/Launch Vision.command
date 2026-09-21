#!/bin/zsh
set -e
cd "$(dirname "$0")"
if [[ ! -d .venv ]]; then uv sync --frozen; fi
exec .venv/bin/python scripts/start_vision.py --setup --background
