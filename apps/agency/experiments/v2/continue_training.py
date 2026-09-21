"""Serialize a separate development-only continuation after current diagnostics."""
import json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone
root=Path('experiments/v2');runs=root/'runs';status=runs/'continuation-status.json'
def record(stage,**kw):
 data={'pid':os.getpid(),'stage':stage,'utc':datetime.now(timezone.utc).isoformat(),**kw}
 status.write_text(json.dumps(data,indent=2));print(data,flush=True)
record('waiting-for-serving-diagnostics')
while True:
 prior=json.loads((runs/'post-training-status.json').read_text())
 if prior['stage']=='diagnostics-complete':break
 if prior['stage'] in ['diagnostics-failed','stopped']:raise RuntimeError('Existing diagnostics failed; do not train over unresolved serving issue')
 try:os.kill(prior['pid'],0)
 except ProcessLookupError:raise RuntimeError('Diagnostic controller disappeared without terminal success')
 time.sleep(5)
checkpoint=root/'models/deberta-travel-continued'
commands=[('training',[sys.executable,str(root/'train_deberta.py'),'--init-checkpoint',str(root/'models/deberta-travel'),'--output',str(checkpoint),'--history',str(runs/'deberta-continued-history.json'),'--epochs','2','--lr','2e-6']),('diagnostics',[sys.executable,str(root/'diagnose_development.py'),'--checkpoint',str(checkpoint)])]
for stage,command in commands:
 record(stage,status='running',command=command)
 with (runs/f'continuation-{stage}.log').open('x') as log:
  result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=7200)
 if result.returncode:
  record('failed',step=stage,exit_code=result.returncode);sys.exit(result.returncode)
record('complete',next='Inspect development and coverage gates; no final generation, freeze, or promotion performed')
