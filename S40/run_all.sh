#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running Project A (Faulty)..."
pushd "$ROOT_DIR/Project_A_Faulty" >/dev/null
./run_original.sh || true
popd >/dev/null

echo "Running Project B (Optimized)..."
pushd "$ROOT_DIR/Project_B_Optimized" >/dev/null
./run_optimized.sh
popd >/dev/null

echo "Generating comparison report summary..."
python - <<'PY'
import json
from pathlib import Path

root = Path(__file__).resolve().parent
shared_cases = json.loads((root / "test_data.json").read_text())
faulty_log = Path(root / "Project_A_Faulty" / "log_original.txt")
optimized_log = Path(root / "Project_B_Optimized" / "log_optimized.txt")

report_lines = ["# Automated Comparison Summary", ""]
report_lines.append("| Case | Faulty | Optimized |")
report_lines.append("| --- | --- | --- |")

faulty_results = {}
if faulty_log.exists():
    for line in faulty_log.read_text().splitlines():
        try:
            faulty_results.update(json.loads(line))
        except json.JSONDecodeError:
            continue

optimized_results = {}
if optimized_log.exists():
    for line in optimized_log.read_text().splitlines():
        if line.strip():
            optimized_results.update(json.loads(line))

for case_name in shared_cases:
    faulty_status = faulty_results.get(case_name, {}).get("status", "n/a")
    optimized_status = optimized_results.get(case_name, {}).get("status", "n/a")
    report_lines.append(f"| {case_name} | {faulty_status} | {optimized_status} |")

(root / "compare_report.md").write_text("\n".join(report_lines), encoding="utf-8")
PY

echo "Run complete. See compare_report.md for details."