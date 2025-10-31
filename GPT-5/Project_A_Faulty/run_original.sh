#!/usr/bin/env bash
set -euo pipefail
start=$(python - <<'PY'
import time;print(time.time())
PY
)
bash setup_original.sh
if [[ "${OS:-}" == "Windows_NT" ]]; then source .venv_original/Scripts/activate; else source .venv_original/bin/activate; fi
python - <<'PY' > time_original.txt
import json, time, pathlib
import importlib.util
import subprocess, sys
root=pathlib.Path(__file__).parent
log_path=root/'log_original.txt'
start=time.time()
# Run pytest quietly
cmd=[sys.executable,'-m','pytest','-q','test_original.py']
proc=subprocess.run(cmd,capture_output=True,text=True)
log_path.write_text(proc.stdout+'\n'+proc.stderr)
end=time.time()
# Count records processed in large payload
td=json.loads((root.parent/'test_data.json').read_text())
records_processed=sum(len(c['input']['records']) if 'records' in c['input'] else 0 for c in td if isinstance(c.get('input'), dict))
json.dump({'total_seconds': end-start, 'records_processed': records_processed}, open(root/'time_original.txt','w'))
print('Timing written')
PY
