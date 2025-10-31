#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv_optimized
. .venv_optimized/bin/activate
pip install --upgrade pip
pip install -r requirements_optimized.txt

echo "Optimized environment ready."