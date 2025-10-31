#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

/bin/echo "[RUN_ALL] Executing Project A (Faulty)" 
"$REPO_ROOT/Project_A_Faulty/run_original.sh"

/bin/echo "[RUN_ALL] Executing Project B (Optimized)" 
"$REPO_ROOT/Project_B_Optimized/run_optimized.sh"

/bin/echo "[RUN_ALL] Aggregation complete. Comparison report available at $REPO_ROOT/compare_report.md"
