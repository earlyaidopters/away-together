"""Resumable development pipeline, separate from shipped V1 and final tests."""
import os,time,json,subprocess,sys,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--writer-pid',type=int);args=p.parse_args();root=Path('experiments/v2');status=root/'runs/pipeline-status.json'
def record(stage,**kw):
 status.write_text(json.dumps({'stage':stage,'pid':os.getpid(),'updated_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),**kw},indent=2));print(stage,kw,flush=True)
if args.writer_pid:
 record('waiting-for-existing-writer',writer_pid=args.writer_pid)
 while True:
  try:os.kill(args.writer_pid,0)
  except ProcessLookupError:break
  time.sleep(5)
for script in ['generate_phrases','audit_phrases','build_development','train_deberta']:
 record(script,status='running')
 with (root/f'runs/{script}-pipeline.log').open('a') as log:
  result=subprocess.run([sys.executable,str(root/f'{script}.py')],stdout=log,stderr=subprocess.STDOUT,timeout=14400)
 if result.returncode:
  record(script,status='failed',exit_code=result.returncode);sys.exit(result.returncode)
 record(script,status='complete')
record('development-complete',status='complete',next='Inspect broad-development/calibration results. No final evaluation or app replacement has occurred.')
