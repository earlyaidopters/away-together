"""Run the prepared boundary-data experiment only if development gates require it."""
import json,os,subprocess,sys,time,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path('experiments/v2');runs=root/'runs';status=runs/'boundary-experiment-status.json'
def record(stage,**kw):
 d={'pid':os.getpid(),'stage':stage,'utc':datetime.now(timezone.utc).isoformat(),**kw}
 status.write_text(json.dumps(d,indent=2));print(d,flush=True)
def run():
 if status.exists():raise FileExistsError('Existing controller state; inspect before relaunch')
 record('waiting-for-continuation')
 while True:
  prior=json.loads((runs/'continuation-status.json').read_text())
  if prior['stage']=='complete':break
  if prior['stage']=='failed':raise RuntimeError('Previous continuation failed')
  try:os.kill(prior['pid'],0)
  except ProcessLookupError:raise RuntimeError('Previous controller missing without terminal success')
  time.sleep(5)
 parent=root/'models/deberta-travel-continued';selection=json.loads((parent/'selection.json').read_text())
 chosen=next(r for r in selection['history'] if r['epoch']==selection['best_epoch'])
 jev=json.loads((runs/'jev-development/jev-travel-development-v2-metrics.json').read_text())
 calibration=[json.loads(x) for x in (root/'data/calibration.jsonl').read_text().splitlines()]
 meets=sum(q['gold']==0 for r in calibration for q in r['questions'])
 err=selection['calibration_accepted_error'];coverage=selection['calibration_accepted']*(1-(err or 0))/meets
 reasons=[]
 if chosen['dev']['accuracy']<=jev['accuracy']:reasons.append('Development accuracy does not exceed Jev')
 if selection['dev_best_macro_f1']<.85:reasons.append('Development macro F1 below gate')
 if err is None or err>.05:reasons.append('Calibration false-accept gate not met')
 if coverage<.5:reasons.append('Calibration qualifying-case coverage below50%')
 record('gate-checked',reasons=reasons,parent_development=chosen['dev'],calibration_meets_coverage=coverage)
 if not reasons:
  record('ready-for-review',next='Inspect completed evidence before freezing; no further training needed by this gate')
  return
 supplemental=root/'data/boundary-train.jsonl';manifest=json.loads((root/'data/boundary-train-manifest.json').read_text())
 if hashlib.sha256(supplemental.read_bytes()).hexdigest()!=manifest['sha256']:raise ValueError('Supplemental data changed')
 checkpoint=root/'models/deberta-travel-boundary'
 commands=[('training',[sys.executable,str(root/'train_deberta.py'),'--init-checkpoint',str(parent),'--output',str(checkpoint),'--history',str(runs/'deberta-boundary-history.json'),'--extra-training',str(supplemental),'--epochs','2','--lr','2e-6']),('diagnostics',[sys.executable,str(root/'diagnose_development.py'),'--checkpoint',str(checkpoint)])]
 for stage,command in commands:
  record(stage,reasons=reasons,command=command)
  with (runs/f'boundary-experiment-{stage}.log').open('x') as log:
   result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=7200)
  if result.returncode:raise RuntimeError(f'{stage} failed with code {result.returncode}')
 record('complete',next='Compare candidate development performance and calibration gates. No final test or promotion performed.')
try:run()
except Exception as e:
 record('failed',error=str(e));raise
