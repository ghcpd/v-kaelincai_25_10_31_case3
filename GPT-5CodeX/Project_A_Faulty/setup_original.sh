#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv_original

if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* ]]; then
  # Git Bash on Windows exposes msys/cygwin OSTYPE values
  source .venv_original/Scripts/activate
else
  source .venv_original/bin/activate
fi

python -m pip install --upgrade pip
python -m pip install -r requirements_original.txt
