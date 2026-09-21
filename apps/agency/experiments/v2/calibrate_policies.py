"""Optional development-stage per-policy temperature ablation; no label changes."""
import argparse,json,hashlib,shutil,time,sys
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from experiments.v2.engine import DebertaEngine
from travel_lab.nli import HYPOTHESES
p=argparse.ArgumentParser();p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
if args.output.exists():raise FileExistsError('Use a new calibration experiment path')
start=time.time();engine=DebertaEngine(args.checkpoint);source=Path('experiments/v2/data/calibration.jsonl');rows=[json.loads(x) for x in source.read_text().splitlines()]
items=[(r['state'],q['id'],q['gold']) for r in rows for q in r['questions']];zs=[]
with torch.no_grad():
 for i in range(0,len(items),16):
  batch=items[i:i+16];x=engine.encode([r[0] for r in batch],[HYPOTHESES[r[1]][0] for r in batch]);z=engine.model(**x).logits[:,[engine.labels['entailment'],engine.labels['contradiction'],engine.labels['neutral']]];zs.append(z.cpu())
z=torch.cat(zs);y=torch.tensor([r[2] for r in items]);temperatures={};grid=np.linspace(.5,5,46)
for task in HYPOTHESES:
 idx=torch.tensor([i for i,r in enumerate(items) if r[1]==task]);zz=z[idx];yy=y[idx]
 temperatures[task]=float(grid[np.argmin([torch.nn.functional.cross_entropy(zz/t,yy).item() for t in grid])])
ts=torch.tensor([temperatures[r[1]] for r in items])[:,None];probs=(z/ts).softmax(-1);confidence,pred=probs.max(-1)
assert torch.equal(pred,z.argmax(-1)), 'Positive temperatures must preserve all labels'
curve=[];chosen=None
for threshold in np.linspace(.5,.99,50):
 accepted=(pred==0)&(confidence>=threshold);n=int(accepted.sum());bad=int((y[accepted]!=0).sum())
 item={'threshold':float(threshold),'accepted':n,'false_accepts':bad,'false_accept_rate':bad/n if n else None,'correct_meets_recall':(n-bad)/int((y==0).sum())}
 curve.append(item)
 if chosen is None and n>=40 and bad/n<=.03:chosen=item
chosen=chosen or {'threshold':1.01,'accepted':0,'false_accepts':0,'false_accept_rate':None,'correct_meets_recall':0}
shutil.copytree(args.checkpoint,args.output)
s=dict(engine.selection);s.update({'temperature_by_field':temperatures,'accept_threshold':chosen['threshold'],'calibration_accepted':chosen['accepted'],'calibration_accepted_error':chosen['false_accept_rate'],'parent_checkpoint':str(args.checkpoint),'parent_checkpoint_sha256':s['sha256'],'seconds':time.time()-start,'calibration_ablation':{'method':'Four scalar temperatures minimizing calibration NLL; unchanged global acceptance rule with 3% calibration error buffer','calibration_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'curve':curve,'chosen':chosen,'argmax_unchanged':True},'status':'Per-policy calibration development candidate; not final validated'})
(args.output/'selection.json').write_text(json.dumps(s,indent=2));print(json.dumps({'temperatures':temperatures,'selected':chosen,'output':str(args.output)},indent=2))
