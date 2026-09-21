"""Candidate adapter; deployment remains V1 until fresh evaluation qualifies V2."""
import json,time,threading,math
from pathlib import Path
import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification,AutoConfig
from safetensors.torch import load_file
from travel_lab.nli import HYPOTHESES
class DebertaEngine:
 def __init__(self,checkpoint='experiments/v2/models/deberta-travel'):
  torch.set_num_threads(8);self.device='mps' if torch.backends.mps.is_available() else 'cpu';self.lock=threading.Lock();folder=Path(checkpoint)
  self.selection=json.loads((folder/'selection.json').read_text());self.model=AutoModelForSequenceClassification.from_config(AutoConfig.from_pretrained(folder/'config',local_files_only=True)).float()
  self.model.load_state_dict(load_file(str(folder/'model.safetensors')))
  self.inference_dtype=self.selection.get('inference_dtype','float32')
  if self.inference_dtype not in ['float32','float16']:raise ValueError('Unsupported inference precision')
  self.model.to(device=self.device,dtype={'float32':torch.float32,'float16':torch.float16}[self.inference_dtype]).eval();self.tokenizer=AutoTokenizer.from_pretrained(folder/'tokenizer',local_files_only=True)
  self.labels={v.lower():int(k) for k,v in self.model.config.id2label.items()};self.temperature=self.selection['temperature'];self.temperature_by_field=self.selection.get('temperature_by_field',{})
  if any(k not in HYPOTHESES or not math.isfinite(v) or v<=0 for k,v in self.temperature_by_field.items()):raise ValueError('Invalid per-policy temperatures')
  self.name='deberta-travel-v2'
 def encode(self,a,b):
  x=self.tokenizer(a,b,padding=True,truncation=False,return_tensors='pt')
  if x['input_ids'].shape[1]>512:raise ValueError(f"Input requires {x['input_ids'].shape[1]} tokens, limit 512; refused rather than truncate")
  return {k:v.to(self.device) for k,v in x.items()}
 def predict(self,state,questions):
  with self.lock,torch.no_grad():
   if self.device=='mps':torch.mps.synchronize()
   start=time.perf_counter();answers=[];calls=0
   tasks=[next((t for t,h in HYPOTHESES.items() if len(q['candidates'])==3 and set(q['candidates'])==set(h)),None) for q in questions]
   native=[(i,t) for i,t in enumerate(tasks) if t];native_probabilities={}
   for offset in range(0,len(native),16):
    batch=native[offset:offset+16]
    z=self.model(**self.encode([state]*len(batch),[HYPOTHESES[t][0] for _,t in batch])).logits
    temperatures=torch.tensor([[getattr(self,'temperature_by_field',{}).get(t,self.temperature)] for _,t in batch],device=z.device,dtype=z.dtype)
    ps=(z[:,[self.labels['entailment'],self.labels['contradiction'],self.labels['neutral']]]/temperatures).softmax(-1).cpu().tolist();calls+=1
    for (index,task),p in zip(batch,ps):
     h=HYPOTHESES[task];native_probabilities[index]=[p[h.index(c)] for c in questions[index]['candidates']]
   # No clause selection/oracle metadata: each premise is the full state.
   for index,q in enumerate(questions):
    if index in native_probabilities:
     p=native_probabilities[index]
    else:
     scores=[]
     for i in range(0,len(q['candidates']),8):
      cs=q['candidates'][i:i+8];z=self.model(**self.encode([state+'\nDecision question: '+q['question']]*len(cs),cs)).logits
      scores.append(z[:,self.labels['entailment']]-torch.logsumexp(z[:,[self.labels['contradiction'],self.labels['neutral']]],dim=-1));calls+=1
     p=torch.cat(scores).softmax(-1).cpu().tolist()
    answers.append({'id':q['id'],'choice':max(range(len(p)),key=lambda i:p[i]),'probabilities':p})
   if self.device=='mps':torch.mps.synchronize()
   elapsed=(time.perf_counter()-start)*1000
  return {'engine':self.name,'elapsed_ms':elapsed,'model_sha256':self.selection['sha256'],'answers':answers,'usage':{'local_model_calls':calls},'upstream_revision':self.selection['revision'],'inference_dtype':getattr(self,'inference_dtype','float32')}
