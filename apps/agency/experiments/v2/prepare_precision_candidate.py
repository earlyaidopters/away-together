"""Validate unchanged calibration at optimized precision in a NEW candidate."""
import argparse,json,shutil,hashlib,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from experiments.v2.engine import DebertaEngine
from travel_lab.evaluate import read
p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise FileExistsError('Preserve prior candidate')
s=json.loads((a.checkpoint/'selection.json').read_text())
if hashlib.sha256((a.checkpoint/'model.safetensors').read_bytes()).hexdigest()!=s['sha256']:raise ValueError('Parent weight hash mismatch')
shutil.copytree(a.checkpoint,a.output)
s.update(inference_dtype='float16',parent_checkpoint=str(a.checkpoint),parent_checkpoint_sha256=s['sha256'],
         status='Precision candidate pending calibration verification',seconds=0)
(a.output/'selection.json').write_text(json.dumps(s,indent=2));engine=DebertaEngine(a.output)
started=time.time();accepted=bad=meets=correct=0;receipts=[]
for row in read('experiments/v2/data/calibration.jsonl'):
    qs=[{k:q[k] for k in ['id','question','candidates']} for q in row['questions']]
    result=engine.predict(row['state'],qs);receipts.append({'id':row['id'],'result':result})
    for q,answer in zip(row['questions'],result['answers']):
        take=answer['choice']==0 and answer['probabilities'][0]>=s['accept_threshold']
        accepted+=take;bad+=take and q['gold']!=0;meets+=q['gold']==0;correct+=take and q['gold']==0
rate=bad/accepted if accepted else None;coverage=correct/meets
s.update(calibration_accepted=accepted,calibration_accepted_error=rate,seconds=time.time()-started,
         precision_validation={'accepted':accepted,'false_accepts':bad,'correct_meets_recall':coverage,
          'calibration_sha256':hashlib.sha256(Path('experiments/v2/data/calibration.jsonl').read_bytes()).hexdigest(),
          'method':'Unchanged parent temperature and acceptance threshold, evaluated through float16 serving adapter'},
         status='Precision calibration verified; development reload checks and fresh final evaluation pending')
(a.output/'precision-calibration-results.json').write_text(json.dumps(receipts))
(a.output/'selection.json').write_text(json.dumps(s,indent=2))
print(s['precision_validation'],flush=True)
if accepted<40 or rate is None or rate>.05 or coverage<.5:raise ValueError('Optimized precision fails calibration qualification')
