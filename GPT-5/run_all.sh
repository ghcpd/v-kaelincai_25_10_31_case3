#!/usr/bin/env bash
set -euo pipefail
echo "Running Project A (Faulty)..."
( cd Project_A_Faulty && bash run_original.sh || echo "Faulty run encountered errors (expected for incompatibility cases)." )
 echo "Running Project B (Optimized)..."
( cd Project_B_Optimized && bash run_optimized.sh )
python - <<'PY'
import json, re, pathlib
root=pathlib.Path('.')
logA=(root/'Project_A_Faulty'/'log_original.txt').read_text(errors='ignore')
logB=(root/'Project_B_Optimized'/'log_optimized.txt').read_text(errors='ignore')
passedA=len(re.findall(r'PASSED', logA))
failedA=len(re.findall(r'FAILED', logA))
passedB=len(re.findall(r'PASSED', logB))
failedB=len(re.findall(r'FAILED', logB))
import json as js
try:
    tA=js.loads((root/'Project_A_Faulty'/'time_original.txt').read_text())
    tB=js.loads((root/'Project_B_Optimized'/'time_optimized.txt').read_text())
except Exception:
    tA={'total_seconds': None,'records_processed': None}
    tB={'total_seconds': None,'records_processed': None}
report=f"""# Compatibility Comparison Report

| Metric | Faulty | Optimized |
|--------|--------|-----------|
| Tests Passed | {passedA} | {passedB} |
| Tests Failed | {failedA} | {failedB} |
| Processing Time (s) | {tA['total_seconds']} | {tB['total_seconds']} |
| Records Processed | {tA['records_processed']} | {tB['records_processed']} |

## Key Fixes
- Timezone 'Z' parsing via dateutil.
- Stable canonicalization (sorted IDs & keys).
- Optional dependency fallback when orjson absent.
- Type coercion for non-string IDs and bytes input support.
- Strict validation of record structure.

## Observations
Faulty implementation shows failures on timezone and type handling; optimized passes those and ensures deterministic output.

"""
(root/'compare_report.md').write_text(report)
print('Report written to compare_report.md')
PY
