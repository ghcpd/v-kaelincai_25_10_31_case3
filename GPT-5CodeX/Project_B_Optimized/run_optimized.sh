#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if [[ ! -d .venv_optimized ]]; then
  ./setup_optimized.sh
fi

if [[ "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* ]]; then
  source .venv_optimized/Scripts/activate
else
  source .venv_optimized/bin/activate
fi

python <<'PY'
import json
import subprocess
import sys
import time
from pathlib import Path

LOG_PATH = Path("log_optimized.txt")
TIME_PATH = Path("time_optimized.txt")

start = time.perf_counter()
proc = subprocess.run(
    [sys.executable, "-m", "pytest", "-q"],
    capture_output=True,
    text=True,
)
elapsed = time.perf_counter() - start

LOG_PATH.write_text(proc.stdout + proc.stderr, encoding="utf-8")
TIME_PATH.write_text(
    f"elapsed_seconds={elapsed:.4f}\nexit_code={proc.returncode}\n",
    encoding="utf-8",
)

sys.exit(proc.returncode)
PY
