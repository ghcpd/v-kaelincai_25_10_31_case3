#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv_original
if [[ "${OS:-}" == "Windows_NT" ]]; then source .venv_original/Scripts/activate; else source .venv_original/bin/activate; fi
python -m pip install --upgrade pip
pip install -r requirements_original.txt
python - <<'PY'
import sys, platform
print('ENV_INFO original')
print('Python', sys.version)
print('Platform', platform.platform())
PY
