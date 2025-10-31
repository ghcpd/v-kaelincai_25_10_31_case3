#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$PROJECT_ROOT/log_original.txt"
TIME_FILE="$PROJECT_ROOT/time_original.txt"

/bin/echo "[INFO] Setting up legacy environment" | tee "$LOG_FILE"
"$PROJECT_ROOT/setup_original.sh"

source "$PROJECT_ROOT/.venv_original/bin/activate"
/bin/echo "[INFO] Running pytest for faulty client" | tee -a "$LOG_FILE"
start_time=$(date +%s)
if pytest "$PROJECT_ROOT/test_original.py" -q >>"$LOG_FILE" 2>&1; then
  status="SUCCESS"
else
  status="FAILURE"
fi
end_time=$(date +%s)
duration=$((end_time - start_time))

/bin/echo "status=$status" > "$TIME_FILE"
/bin/echo "duration_seconds=$duration" >> "$TIME_FILE"
/bin/echo "completed_at=$(date --iso-8601=seconds)" >> "$TIME_FILE"

/bin/echo "[INFO] Legacy run finished with $status" | tee -a "$LOG_FILE"
