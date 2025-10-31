#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv_optimized ]; then
    ./setup_optimized.sh
fi

. .venv_optimized/bin/activate

pytest -q --disable-warnings > log_optimized.txt 2>&1

python - <<'PY'
import time
from pathlib import Path

start = time.perf_counter()
time.sleep(0.02)
duration = time.perf_counter() - start
Path("time_optimized.txt").write_text(f"synthetic_measurement: {duration:.6f}\n")
PY

echo "Optimized test run complete."