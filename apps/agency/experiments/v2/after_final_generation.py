"""Score the frozen candidate only after fresh generation and reference audit seal."""
import json,os,subprocess,sys,time
from pathlib import Path
from datetime import datetime,timezone
root=Path('experiments/v2');status=root/'runs/final-round1-status.json'
if status.exists():raise FileExistsError('Inspect existing final controller before relaunch')
def record(stage,**kw):
    d=dict(pid=os.getpid(),stage=stage,utc=datetime.now(timezone.utc).isoformat(),**kw)
    status.write_text(json.dumps(d,indent=2));print(d,flush=True)
try:
    record('waiting-for-generation',generation_pid=57889)
    while True:
        try:os.kill(57889,0)
        except ProcessLookupError:break
        time.sleep(5)
    data=root/'final/round1-deeper-fp16/test.jsonl'
    if not data.exists() or not data.with_suffix('.manifest.json').exists():
        raise RuntimeError('Generation ended without sealed data; inspect audit disagreements/errors before any contestant inference')
    command=[sys.executable,str(root/'compare_frozen.py'),'--freeze',str(root/'freezes/deeper-fp16-20260921.json'),
             '--data',str(data),'--round','round1-deeper-fp16']
    with (root/'runs/final-round1-head-to-head.log').open('x') as log:
        child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT)
        record('frozen-head-to-head',child_pid=child.pid,command=command)
        try:code=child.wait(timeout=7200)
        except subprocess.TimeoutExpired:
            child.terminate()
            try:child.wait(timeout=30)
            except subprocess.TimeoutExpired:child.kill();child.wait()
            raise
    if code:raise RuntimeError(f'Head-to-head failed with code {code}')
    report=json.loads((root/'runs/round1-deeper-fp16/paired-report.json').read_text())
    record('complete',round_qualifies=report['round_qualifies'],next='Review evidence; a qualifying result still requires independent fresh replication. No deployment performed.')
except Exception as error:
    record('failed',error=str(error));raise
