"""Run the pinned untuned comparator after the prioritized speed benchmark."""
import json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone
root = Path('experiments/next-token')
status = root / 'controller-status.json'
if status.exists(): raise FileExistsError('Inspect existing next-token controller before relaunch')
def record(stage, **kw):
    d = dict(pid=os.getpid(), stage=stage, utc=datetime.now(timezone.utc).isoformat(), **kw)
    status.write_text(json.dumps(d, indent=2)); print(d, flush=True)
try:
    record('waiting-for-precision-benchmark')
    while True:
        prior = json.loads(Path('experiments/v2/runs/precision-benchmark-status.json').read_text())
        if prior['stage'] in ['complete', 'ready-for-review']: break
        if prior['stage'] == 'failed': raise RuntimeError('Precision benchmark failed; inspect before proceeding')
        os.kill(prior['pid'], 0)
        time.sleep(5)
    with (root / 'development.log').open('x') as log:
        process = subprocess.Popen([sys.executable, str(root / 'evaluate_development.py')], stdout=log, stderr=subprocess.STDOUT)
        record('development-evaluation', child_pid=process.pid)
        try:
            code = process.wait(timeout=10800)
        except subprocess.TimeoutExpired:
            process.terminate()
            try: process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait()
            raise
    if code: raise RuntimeError(f'Comparator exited with code {code}')
    record('complete', next='Inspect development accuracy/order bias. Uncalibrated; not final qualified.')
except Exception as error:
    record('failed', error=str(error)); raise
