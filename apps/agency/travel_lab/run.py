"""Resumable local experiment controller. Logs/stage receipts survive interruption."""
import argparse,datetime,fcntl,json,os,subprocess,sys,time
from pathlib import Path

def atomic(path,data):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2));os.replace(tmp,path)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',default='config/run.yaml');parser.add_argument('--resume',default='overnight-20260920');parser.add_argument('--adopt-training',action='store_true');parser.add_argument('--skip-jev',action='store_true');args=parser.parse_args()
    folder=Path('runs')/args.resume;folder.mkdir(parents=True,exist_ok=True)
    lock=(folder/'controller.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    p=folder/'state.json';state=json.loads(p.read_text()) if p.exists() else {'run_id':args.resume,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deadline_epoch':time.time()+36000,'stages':{},'paid_calls':0,'infrastructure':'local M5 Max; external allowed by user if beneficial'}
    atomic(p,state)
    def stage(name,command):
        if state['stages'].get(name,{}).get('status')=='complete':return
        if time.time()>state['deadline_epoch']-5400:raise TimeoutError('Reserved reporting window reached; resumable checkpoint saved')
        state['stages'][name]={'status':'running','command':command,'started':time.time()};atomic(p,state)
        with (folder/f'{name}.log').open('a') as log:
            result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=max(1,state['deadline_epoch']-time.time()-5400))
        state['stages'][name].update({'status':'complete' if result.returncode==0 else 'failed','finished':time.time(),'exit_code':result.returncode});atomic(p,state)
        if result.returncode:raise RuntimeError(f'{name} failed; inspect {folder/name}.log')
    if args.adopt_training:
        state['stages']['training']={'status':'adopting existing training job'};atomic(p,state)
        while not Path('models/travel-nli/model.safetensors').exists() or not Path('models/selection.json').exists() or json.loads(Path('models/selection.json').read_text()).get('architecture')!='nli':
            if time.time()>state['deadline_epoch']-5400:raise TimeoutError('Training did not finish within execution window')
            time.sleep(5)
        state['stages']['training']={'status':'complete','adopted':True,'selection_sha256':__import__('hashlib').sha256(Path('models/selection.json').read_bytes()).hexdigest()};atomic(p,state)
    else:
        if not Path('data/manifests/travel.json').exists():stage('data',[sys.executable,'-m','travel_lab.data'])
        if not Path('runs/preflight/admission.json').exists():stage('admission',[sys.executable,'-m','travel_lab.admission'])
        if not Path('models/first-candidate-selection.json').exists():stage('train-base',[sys.executable,'-m','travel_lab.train'])
        if not Path('models/selection.json').exists() or json.loads(Path('models/selection.json').read_text()).get('architecture')!='nli':stage('train-nli',[sys.executable,'-m','travel_lab.train_nli'])
    stage('tests',[sys.executable,'-m','pytest','-q'])
    if not Path('data/manifests/public.json').exists():stage('public-data',[sys.executable,'-m','travel_lab.public_data'])
    for engine in ['trained','baseline','base-head']:stage('evaluate-'+engine,[sys.executable,'-m','travel_lab.evaluate','--engine',engine])
    if not args.skip_jev:stage('evaluate-jev',[sys.executable,'-m','travel_lab.evaluate','--engine','jev'])
    stage('report',[sys.executable,'-m','travel_lab.report','--run',args.resume])
    state['status']='independent experiments complete; app QA and filming package tracked separately';atomic(p,state)
if __name__=='__main__':main()
