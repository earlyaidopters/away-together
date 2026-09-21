"""Continue with serving diagnostics once the existing training job completes."""
import json,os,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
root=Path('experiments/v2');parent=root/'runs/recovery-status.json';status=root/'runs/post-training-status.json'
def record(stage,**extra):
 data={'pid':os.getpid(),'stage':stage,'utc':datetime.now(timezone.utc).isoformat(),**extra};status.write_text(json.dumps(data,indent=2));print(data,flush=True)
record('waiting-for-existing-training')
while True:
 prior=json.loads(parent.read_text())
 if prior.get('status')=='failed':record('stopped',reason='Training pipeline failed; inspect its existing logs');sys.exit(1)
 if prior.get('stage')=='development-complete' and prior.get('status')=='complete':break
 try:os.kill(prior['pid'],0)
 except ProcessLookupError:record('stopped',reason='Pipeline missing without terminal success; inspect before running diagnostics');sys.exit(1)
 time.sleep(5)
record('serving-development-diagnostics',status='running')
with (root/'runs/selected-development-diagnostics.log').open('a') as log:
 result=subprocess.run([sys.executable,str(root/'diagnose_development.py')],stdout=log,stderr=subprocess.STDOUT,timeout=3600)
record('diagnostics-complete' if result.returncode==0 else 'diagnostics-failed',exit_code=result.returncode,next='Inspect selected calibration and development breakdowns; no final generation or promotion occurred')
