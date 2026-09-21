"""Serialize the optional calibration ablation after boundary training diagnostics."""
import json,os,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
root=Path('experiments/v2');runs=root/'runs';status=runs/'policy-calibration-status.json'
if status.exists():raise FileExistsError('Inspect existing calibration controller before relaunch')
def record(stage,**kw):
 d={'pid':os.getpid(),'stage':stage,'utc':datetime.now(timezone.utc).isoformat(),**kw};status.write_text(json.dumps(d,indent=2));print(d,flush=True)
try:
 record('waiting-for-boundary-diagnostics')
 while True:
  prior=json.loads((runs/'boundary-experiment-status.json').read_text())
  if prior['stage']=='complete':break
  if prior['stage'] in ['failed','ready-for-review']:raise RuntimeError('Boundary experiment did not complete; inspect before calibration')
  try:os.kill(prior['pid'],0)
  except ProcessLookupError:raise RuntimeError('Boundary controller missing without terminal success')
  time.sleep(5)
 checkpoint=root/'models/deberta-travel-boundary-policycal'
 commands=[('calibration',[sys.executable,str(root/'calibrate_policies.py'),'--checkpoint',str(root/'models/deberta-travel-boundary'),'--output',str(checkpoint)]),('diagnostics',[sys.executable,str(root/'diagnose_development.py'),'--checkpoint',str(checkpoint)]),('ledger',[sys.executable,str(root/'experiment_ledger.py')])]
 for stage,command in commands:
  record(stage,command=command)
  with (runs/f'policy-calibration-{stage}.log').open('x') as log:
   result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
  if result.returncode:raise RuntimeError(f'{stage} failed with code {result.returncode}')
 record('complete',next='Inspect original and calibrated candidates. No final freeze or model promotion performed.')
except Exception as e:
 record('failed',error=str(e));raise
