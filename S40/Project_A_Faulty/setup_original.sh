#!/usr/bin/env bash
set -euo pipefail

# Faulty environment setup: pins legacy pytest version incompatible with Python 3.12
# and lacks platform detection.

python -m venv .venv_original
. .venv_original/bin/activate
pip install --upgrade pip
pip install -r requirements_original.txt

echo "Faulty environment ready."