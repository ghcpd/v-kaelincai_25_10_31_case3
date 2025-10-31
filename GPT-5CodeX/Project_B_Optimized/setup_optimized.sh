#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv_optimized

if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* ]]; then
  source .venv_optimized/Scripts/activate
else
  source .venv_optimized/bin/activate
fi

python -m pip install --upgrade pip
python -m pip install -r requirements_optimized.txt
