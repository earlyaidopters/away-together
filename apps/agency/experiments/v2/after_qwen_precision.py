"""Validate the faster candidate after the running Qwen comparator releases GPU."""
import json,os,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
root=Path('experiments/v2');status=root/'runs/precision-candidate-status.json'
if status.exists():raise FileExistsError('Inspect existing precision validation before relaunch')
def record(stage,**kw):
    d=dict(pid=os.getpid(),stage=stage,utc=datetime.now(timezone.utc).isoformat(),**kw)
    status.write_text(json.dumps(d,indent=2));print(d,flush=True)
try:
    record('waiting-for-qwen')
    while True:
        prior=json.loads(Path('experiments/next-token/controller-status.json').read_text())
        if prior['stage']=='complete':break
        if prior['stage']=='failed':raise RuntimeError('Qwen comparator failed; verify GPU release before continuing')
        os.kill(prior['pid'],0);time.sleep(5)
    checkpoint=root/'models/deberta-travel-deeper-fp16'
    commands=[('calibration',[sys.executable,str(root/'prepare_precision_candidate.py'),'--checkpoint',str(root/'models/deberta-travel-deeper'),'--output',str(checkpoint)]),
              ('diagnostics',[sys.executable,str(root/'diagnose_development.py'),'--checkpoint',str(checkpoint)])]
    for stage,command in commands:
        with (root/f'runs/precision-candidate-{stage}.log').open('x') as log:
            child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT)
            record(stage,child_pid=child.pid,command=command)
            try:code=child.wait(timeout=3600)
            except subprocess.TimeoutExpired:
                child.terminate()
                try:child.wait(timeout=30)
                except subprocess.TimeoutExpired:child.kill();child.wait()
                raise
        if code:raise RuntimeError(f'{stage} failed with code {code}')
    record('complete',next='Review comparator and optimized candidate before freeze; no final inference or deployment performed')
except Exception as error:
    record('failed',error=str(error));raise
