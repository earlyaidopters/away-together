"""Selected-checkpoint diagnostics on development only, never final/calibration."""
import json,sys,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from experiments.v2.engine import DebertaEngine
from experiments.v2.breakdown import breakdown
from travel_lab.evaluate import evaluate_lane,read
parser=argparse.ArgumentParser();parser.add_argument('--checkpoint',type=Path,default=Path('experiments/v2/models/deberta-travel'));args=parser.parse_args()
engine=DebertaEngine(args.checkpoint);digest=hashlib.sha256((args.checkpoint/'selection.json').read_bytes()).hexdigest()[:12];out=Path('experiments/v2/runs')/('selected-development-'+digest)
out.mkdir(parents=True,exist_ok=True);parity=[];all_results=[]
for row in read('experiments/v2/data/dev.jsonl')[:12]:
 qs=[{k:v for k,v in q.items() if k not in ['gold','soft_gold']} for q in row['questions']]
 batched=engine.predict(row['state'],qs);single=[engine.predict(row['state'],[q]) for q in qs]
 max_delta=max(abs(x-y) for a,b in zip(batched['answers'],single) for x,y in zip(a['probabilities'],b['answers'][0]['probabilities']))
 choices_match=all(a['choice']==b['answers'][0]['choice'] for a,b in zip(batched['answers'],single))
 parity.append({'id':row['id'],'max_probability_delta':max_delta,'choices_match':choices_match,'batched_ms':batched['elapsed_ms'],'serial_total_ms':sum(s['elapsed_ms'] for s in single),'batched_model_calls':batched['usage']['local_model_calls']})
(out/'batch-parity.json').write_text(json.dumps({'device':engine.device,'cases':parity,'scope':'Twelve development scenarios; first case includes warm-up effects. Final comparison measures actual serving latency.'},indent=2))
if any(not r['choices_match'] or r['max_probability_delta']>1e-4 for r in parity):raise ValueError('Batch parity requires investigation before freeze')
for split in ['dev','robustness-dev']:
 rows=read(f'experiments/v2/data/{split}.jsonl');name='travel-'+split
 evaluate_lane(engine,name,rows,out,engine.selection['accept_threshold'])
 results=read(out/f'{engine.name}-{name}.jsonl');report=breakdown(rows,results)
 all_results.extend(results)
 (out/f'{split}-breakdown.json').write_text(json.dumps(report,indent=2))
 print(split,{k:round(v['accuracy'],4) for k,v in report['groups'].items()},flush=True)
correct=sum(d.get('pred')==d['gold'] for r in all_results for d in r['decisions']);n=sum(len(r['decisions']) for r in all_results)
selected=next(r for r in engine.selection['history'] if r['epoch']==engine.selection['best_epoch'])
reload={'selected_epoch':engine.selection['best_epoch'],'serving_development_accuracy':correct/n,'training_evaluator_development_accuracy':selected['dev']['accuracy'],'matches':abs(correct/n-selected['dev']['accuracy'])<1e-6}
(out/'reload-parity.json').write_text(json.dumps(reload,indent=2))
if not reload['matches']:raise ValueError('Reloaded serving model does not reproduce selected development accuracy')
