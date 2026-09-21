"""V2 development-only model selection. Does not open V1/V2 final tests."""
import json,time,random,hashlib,sys,argparse
from pathlib import Path
import torch
import numpy as np
from sklearn.metrics import f1_score
from transformers import AutoModelForSequenceClassification,AutoTokenizer,AutoConfig
from safetensors.torch import save_file,load_file
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from travel_lab.nli import HYPOTHESES
from experiments.v2.preflight import preflight
ROOT=Path('experiments/v2');pin=json.loads((ROOT/'research/deberta-pin.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--epochs',type=int,default=3);parser.add_argument('--lr',type=float,default=2e-6);parser.add_argument('--init-checkpoint',type=Path)
parser.add_argument('--output',type=Path,default=ROOT/'models/deberta-travel')
parser.add_argument('--history',type=Path,default=ROOT/'runs/deberta-history.json')
parser.add_argument('--train-layers',type=int,default=2)
parser.add_argument('--extra-training',type=Path,action='append',default=[])
args=parser.parse_args()
if args.epochs<1 or args.train_layers<1:parser.error('Positive epochs and train-layers required')
if args.output.exists() and any(args.output.iterdir()):parser.error('Output must be new; preserve prior checkpoints')
if args.history.exists():parser.error('History must be new; preserve prior results')
parent_selection=None
if args.init_checkpoint:
 parent_selection=json.loads((args.init_checkpoint/'selection.json').read_text())
 actual=hashlib.sha256((args.init_checkpoint/'model.safetensors').read_bytes()).hexdigest()
 if actual!=parent_selection['sha256']:raise ValueError('Parent checkpoint hash mismatch')
 if parent_selection['base']!=pin['id'] or parent_selection['revision']!=pin['revision']:raise ValueError('Parent base differs from pinned architecture')
torch.manual_seed(20260921);random.seed(20260921);torch.set_num_threads(8);device='mps' if torch.backends.mps.is_available() else 'cpu'
if args.init_checkpoint:
 tok=AutoTokenizer.from_pretrained(args.init_checkpoint/'tokenizer',local_files_only=True)
 m=AutoModelForSequenceClassification.from_config(AutoConfig.from_pretrained(args.init_checkpoint/'config',local_files_only=True))
 m.load_state_dict(load_file(str(args.init_checkpoint/'model.safetensors')))
else:
 tok=AutoTokenizer.from_pretrained(pin['id'],revision=pin['revision'])
 m=AutoModelForSequenceClassification.from_pretrained(pin['id'],revision=pin['revision'])
preflight(tok);m=m.float().to(device)
if args.train_layers>len(m.deberta.encoder.layer):raise ValueError('Too many trainable layers')
labels={v.lower():int(k) for k,v in m.config.id2label.items()};order=[labels['entailment'],labels['contradiction'],labels['neutral']]
def data(split):
 scenarios=[json.loads(x) for x in (ROOT/f'data/{split}.jsonl').read_text().splitlines()]
 return [(r['id'],q['id'],r['state'],HYPOTHESES[q['id']][0],q['gold']) for r in scenarios for q in r['questions']]
def batch(items):
 x=tok([r[2] for r in items],[r[3] for r in items],padding=True,truncation=False,return_tensors='pt')
 if x['input_ids'].shape[1]>512:raise ValueError('Overlong case; no truncation')
 return {k:v.to(device) for k,v in x.items()},torch.tensor([r[4] for r in items],device=device)
def evaluate(rows):
 m.eval();zs=[];ys=[]
 with torch.no_grad():
  for i in range(0,len(rows),16):
   x,y=batch(rows[i:i+16]);zs.append(m(**x).logits[:,order].cpu());ys.extend(y.cpu().tolist())
 z=torch.cat(zs);pred=z.argmax(-1).tolist();by={t:f1_score([r[4] for r in rows if r[1]==t],[v for r,v in zip(rows,pred) if r[1]==t],labels=[0,1,2],average='macro',zero_division=0) for t in HYPOTHESES}
 return {'accuracy':sum(a==b for a,b in zip(pred,ys))/len(ys),'macro_f1_by_field':float(np.mean(list(by.values()))),'fields':by},z,torch.tensor(ys)
initial_classifier=m.classifier.weight.detach().cpu().clone()
train=data('train');extra_hashes={}
existing_texts={r[2] for split in ['train','dev','calibration','robustness-dev'] for r in data(split)}
for path in args.extra_training:
 rows=[json.loads(x) for x in path.read_text().splitlines()]
 if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate additional training IDs')
 for r in rows:
  if r['state'] in existing_texts:raise ValueError('Additional training overlaps existing documents')
  existing_texts.add(r['state'])
  if len(r['questions'])!=4 or {q['id'] for q in r['questions']}!=set(HYPOTHESES):raise ValueError('Additional training schema invalid')
  for q in r['questions']:
   if q['gold'] not in [0,1,2] or q['candidates']!=HYPOTHESES[q['id']]:raise ValueError('Additional training labels invalid')
   if len(tok(r['state'],HYPOTHESES[q['id']][0],truncation=False)['input_ids'])>512:raise ValueError('Overlong additional training')
   train.append((r['id'],q['id'],r['state'],HYPOTHESES[q['id']][0],q['gold']))
 extra_hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
dev=data('dev');robust_dev=data('robustness-dev');dev=dev+robust_dev;out=args.output;out.mkdir(exist_ok=True,parents=True);history=[];start=time.time()
metrics,_,_=evaluate(dev);robust_metrics,_,_=evaluate(robust_dev);best=metrics['macro_f1_by_field'];record={'epoch':0,'dev':metrics,'authored_robustness_dev':robust_metrics,'elapsed':time.time()-start};history.append(record);print(record,flush=True)
save_file({k:v.detach().cpu().contiguous() for k,v in m.state_dict().items()},out/'model.safetensors');best_epoch=0
for p in m.parameters():p.requires_grad=False
for layer in m.deberta.encoder.layer[-args.train_layers:]:
 for p in layer.parameters():p.requires_grad=True
for module in [m.pooler,m.classifier]:
 for p in module.parameters():p.requires_grad=True
opt=torch.optim.AdamW([p for p in m.parameters() if p.requires_grad],lr=args.lr,weight_decay=.01)
for epoch in range(1,args.epochs+1):
 m.train();random.shuffle(train);losses=[]
 for i in range(0,len(train),16):
  x,y=batch(train[i:i+16]);opt.zero_grad();loss=torch.nn.functional.cross_entropy(m(**x).logits[:,order],y);loss.backward();torch.nn.utils.clip_grad_norm_([p for p in m.parameters() if p.requires_grad],1);opt.step();losses.append(loss.item())
  if i%800==0:print('train',epoch,i,len(train),'loss',float(np.mean(losses[-50:])),'elapsed',time.time()-start,flush=True)
 metrics,_,_=evaluate(dev);robust_metrics,_,_=evaluate(robust_dev);record={'epoch':epoch,'dev':metrics,'authored_robustness_dev':robust_metrics,'loss':float(np.mean(losses)),'elapsed':time.time()-start};history.append(record);print(record,flush=True);args.history.write_text(json.dumps(history,indent=2))
 if metrics['macro_f1_by_field']>best:
  best=metrics['macro_f1_by_field'];best_epoch=epoch;save_file({k:v.detach().cpu().contiguous() for k,v in m.state_dict().items()},out/'model.safetensors')
m.load_state_dict(load_file(str(out/'model.safetensors')));cal,z,y=evaluate(data('calibration'));temps=np.linspace(.5,5,46);temp=float(temps[np.argmin([torch.nn.functional.cross_entropy(z/t,y).item() for t in temps])]);p=(z/temp).softmax(-1);conf,pred=p.max(-1);threshold=1.01;accepted_n=0;error_rate=None
for v in np.linspace(.5,.99,50):
 accepted=(pred==0)&(conf>=v)
 if int(accepted.sum())>=40 and float((y[accepted]!=0).float().mean())<=.03:
  threshold=float(v);accepted_n=int(accepted.sum());error_rate=float((y[accepted]!=0).float().mean());break
m.config.save_pretrained(out/'config');tok.save_pretrained(out/'tokenizer')
selection={'selected':'deberta-travel-v2','architecture':'three-way-nli','base':pin['id'],'revision':pin['revision'],'best_epoch':best_epoch,'selected_weight_delta_l2':float((m.classifier.weight.detach().cpu()-initial_classifier).norm()),'trained_candidate_selected':best_epoch>0 or bool(parent_selection and parent_selection.get('trained_candidate_selected')),'parent_checkpoint_sha256':parent_selection['sha256'] if parent_selection else None,'parent_checkpoint':str(args.init_checkpoint) if args.init_checkpoint else None,'training':{'learning_rate':args.lr,'epochs':args.epochs,'trainable_encoder_layers':args.train_layers,'seed':20260921,'optimizer':'AdamW; fresh optimizer state for this run','batch_size':16,'extra_training_files':extra_hashes,'training_decisions':len(train)},'temperature':temp,'accept_threshold':threshold,'calibration':cal,'calibration_accepted':accepted_n,'calibration_accepted_error':error_rate,'dev_best_macro_f1':best,'history':history,'seconds':time.time()-start,'sha256':hashlib.sha256((out/'model.safetensors').read_bytes()).hexdigest(),'status':'development candidate; not final qualified or app selected','final_test_scored':False}
(out/'selection.json').write_text(json.dumps(selection,indent=2));print(json.dumps(selection),flush=True)
