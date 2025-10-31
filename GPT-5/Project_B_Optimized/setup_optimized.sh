#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv_optimized
if [[ "${OS:-}" == "Windows_NT" ]]; then source .venv_optimized/Scripts/activate; else source .venv_optimized/bin/activate; fi
python -m pip install --upgrade pip
pip install -r requirements_optimized.txt || echo "Continuing without optional packages"
python - <<'PY'
import sys, platform
print('ENV_INFO optimized')
print('Python', sys.version)
print('Platform', platform.platform())
PY
