import json,time,sys,argparse
from pathlib import Path
import requests,torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from sklearn.metrics import f1_score
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from travel_lab.nli import HYPOTHESES
OUT=Path('experiments/v2/runs');OUT.mkdir(parents=True,exist_ok=True)
ID='MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli'
parser=argparse.ArgumentParser();parser.add_argument('--data',default='data/dev.jsonl');parser.add_argument('--name',default='original-development');args=parser.parse_args()
assert '/' not in args.name and '..' not in args.name
pin=Path('experiments/v2/research/deberta-pin.json')
if pin.exists():
 rev=json.loads(pin.read_text())['revision']
else:
 info=requests.get('https://huggingface.co/api/models/'+ID,timeout=30);info.raise_for_status();rev=info.json()['sha']
 pin.write_text(json.dumps({'id':ID,'revision':rev,'role':'3-way NLI candidate','source':'first-party Hugging Face model card'},indent=2))
print('loading',ID,rev,flush=True);torch.set_num_threads(8)
tok=AutoTokenizer.from_pretrained(ID,revision=rev)
m=AutoModelForSequenceClassification.from_pretrained(ID,revision=rev).float();device='mps' if torch.backends.mps.is_available() else 'cpu';m.to(device).eval()
print('loaded',m.config.id2label,device,flush=True)
rows=[json.loads(x) for x in Path(args.data).read_text().splitlines()]
flat=[(r['id'],q['id'],r['state'],HYPOTHESES[q['id']][0],q['gold']) for r in rows for q in r['questions']]
labels={v.lower():int(k) for k,v in m.config.id2label.items()};order=[labels['entailment'],labels['contradiction'],labels['neutral']]
out=[];start=time.time()
with torch.no_grad():
 for i in range(0,len(flat),8):
  batch=flat[i:i+8];x=tok([r[2] for r in batch],[r[3] for r in batch],return_tensors='pt',padding=True,truncation=False)
  if x['input_ids'].shape[1]>512:raise ValueError('overlong; no silent truncation')
  t=time.perf_counter();z=m(**{k:v.to(device) for k,v in x.items()}).logits[:,order];probs=z.softmax(-1).cpu().tolist();ms=(time.perf_counter()-t)*1000
  out.extend({'id':r[0],'task':r[1],'gold':r[4],'pred':max(range(3),key=lambda j:p[j]),'probabilities':p,'batch_ms':ms} for r,p in zip(batch,probs))
  if i%80==0:print('development',i,len(flat),'seconds',time.time()-start,flush=True)
(OUT/f'deberta-{args.name}.json').write_text(json.dumps(out))
metrics={'accuracy':sum(r['gold']==r['pred'] for r in out)/len(out),'macro_f1':f1_score([r['gold'] for r in out],[r['pred'] for r in out],average='macro'),'n':len(out),'elapsed_s':time.time()-start,'revision':rev,'split':'original dev only; no final scoring'}
metrics['split']=args.data+'; development only; no final scoring'
(OUT/f'deberta-{args.name}-metrics.json').write_text(json.dumps(metrics,indent=2));print(metrics,flush=True)
