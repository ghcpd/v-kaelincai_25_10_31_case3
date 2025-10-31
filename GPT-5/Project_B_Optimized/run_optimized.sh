#!/usr/bin/env bash
set -euo pipefail
bash setup_optimized.sh
if [[ "${OS:-}" == "Windows_NT" ]]; then source .venv_optimized/Scripts/activate; else source .venv_optimized/bin/activate; fi
python - <<'PY' > time_optimized.txt
import json, time, pathlib, subprocess, sys
root=pathlib.Path(__file__).parent
log_path=root/'log_optimized.txt'
start=time.time()
cmd=[sys.executable,'-m','pytest','-q','test_optimized.py']
proc=subprocess.run(cmd,capture_output=True,text=True)
log_path.write_text(proc.stdout+'\n'+proc.stderr)
end=time.time()
# Recompute records processed
cases=json.loads((root.parent/'test_data.json').read_text())
records_processed=0
for c in cases:
    inp=c['input']
    if 'generate_dynamic' in c:
        records_processed += c['generate_dynamic']['count']
    else:
        records_processed += len(inp.get('records', []))
json.dump({'total_seconds': end-start, 'records_processed': records_processed}, open(root/'time_optimized.txt','w'))
print('Timing written')
PY
