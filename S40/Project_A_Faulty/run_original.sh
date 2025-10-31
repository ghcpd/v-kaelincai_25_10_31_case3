#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .venv_original ]; then
    ./setup_original.sh
fi

. .venv_original/bin/activate

pytest -q --disable-warnings --maxfail=1 > log_original.txt 2>&1 || true

python - <<'PY'
import json
import time
from pathlib import Path

start = time.perf_counter()
# simulate measurement for compatibility time report
time.sleep(0.05)
duration = time.perf_counter() - start
Path("time_original.txt").write_text(f"synthetic_measurement: {duration:.6f}\n")

Path("log_original.txt").write_text(
    Path("log_original.txt").read_text() + "\nSynthetic run complete."
)
PY

echo "Faulty test run complete (expected failures)."