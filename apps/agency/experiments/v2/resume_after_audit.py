"""Wait for the verified existing pipeline, repair data gaps once, then train.

Never races a live audit or weakens its inclusion gate. Never runs final tests.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone

root = Path('experiments/v2')
prior = root/'runs/pipeline-status.json'
status = root/'runs/recovery-status.json'

def record(stage, **extra):
    item = {'pid': os.getpid(), 'stage': stage, 'updated_utc': datetime.now(timezone.utc).isoformat(), **extra}
    status.write_text(json.dumps(item, indent=2))
    print(item, flush=True)

state = json.loads(prior.read_text())
pid = state['pid']
record('waiting-for-existing-pipeline', pipeline_pid=pid)
while True:
    state = json.loads(prior.read_text())
    if state.get('status') == 'failed' or state.get('stage') == 'development-complete':
        break
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        record('stopped', reason='Original pipeline disappeared without terminal status; inspect before resuming')
        sys.exit(1)
    time.sleep(5)
if state.get('stage') == 'development-complete':
    record('complete', reason='Original pipeline completed; no duplicate training')
    sys.exit(0)
if state.get('stage') != 'build_development':
    record('stopped', reason='Failure outside data coverage gate requires diagnosis', prior=state)
    sys.exit(1)
for script in ['repair_phrases', 'audit_phrases', 'build_development', 'train_deberta']:
    record(script, status='running')
    with (root/f'runs/{script}-recovery.log').open('a') as log:
        result = subprocess.run([sys.executable, str(root/f'{script}.py')], stdout=log, stderr=subprocess.STDOUT, timeout=14400)
    if result.returncode:
        record(script, status='failed', exit_code=result.returncode)
        sys.exit(result.returncode)
record('development-complete', status='complete', next='Inspect development/calibration; model not yet frozen or deployed')
