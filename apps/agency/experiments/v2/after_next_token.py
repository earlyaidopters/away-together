"""Speed-priority queue: benchmark directly after deeper training/diagnostics."""
import json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone
root=Path('experiments/v2');status=root/'runs/precision-benchmark-status.json'
if status.exists():raise FileExistsError('Inspect existing precision controller before relaunch')
def record(stage,**kw):
    d=dict(pid=os.getpid(),stage=stage,utc=datetime.now(timezone.utc).isoformat(),**kw)
    status.write_text(json.dumps(d,indent=2));print(d,flush=True)
try:
    record('waiting-for-deeper-experiment')
    while True:
        prior=json.loads(Path('experiments/v2/runs/deeper-experiment-status.json').read_text())
        if prior['stage']=='complete':break
        if prior['stage']=='failed':raise RuntimeError('Deeper experiment failed; inspect GPU state before benchmarking')
        os.kill(prior['pid'],0);time.sleep(5)
    command=[sys.executable,str(root/'benchmark_precision.py'),'--checkpoint',str(root/'models/deberta-travel-deeper'),
             '--output',str(root/'runs/deeper-precision-benchmark')]
    with (root/'runs/precision-benchmark.log').open('x') as log:
        child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT)
        record('benchmarking',child_pid=child.pid,command=command)
        try:code=child.wait(timeout=7200)
        except subprocess.TimeoutExpired:
            child.terminate()
            try:child.wait(timeout=30)
            except subprocess.TimeoutExpired:child.kill();child.wait()
            raise
    if code:raise RuntimeError(f'Precision benchmark exited with code {code}')
    record('complete',next='Inspect speed and changed decisions; no precision promotion performed')
except Exception as error:
    record('failed',error=str(error));raise
