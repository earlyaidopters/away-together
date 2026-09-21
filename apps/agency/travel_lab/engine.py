import json,time,threading
from pathlib import Path
import torch
from safetensors.torch import load_file
from .model import CandidateModel,candidate_text,group_logits

class LocalEngine:
    name='local'
    def __init__(self, checkpoint=None):
        torch.set_num_threads(8)
        selection=Path('models/selection.json')
        if not selection.exists() and checkpoint is None:raise RuntimeError('Training has not finished; no selected model exists yet.')
        self.selection=json.loads(selection.read_text()) if selection.exists() else {}
        self.checkpoint=checkpoint or self.selection['selected']
        if checkpoint:
            import hashlib
            self.selection={'selected':checkpoint,'sha256':hashlib.sha256(Path(f'models/{checkpoint}/model.safetensors').read_bytes()).hexdigest(),'temperature':1}
        self.device='mps' if torch.backends.mps.is_available() else 'cpu'
        self.model=CandidateModel();self.model.load_state_dict(load_file(f'models/{self.checkpoint}/model.safetensors'))
        self.model.to(self.device).eval();self.lock=threading.Lock()
        self.temperature=self.selection.get('temperature',1) if checkpoint is None else 1
    def predict(self,state,questions):
        with self.lock,torch.no_grad():
            if self.device=='mps':torch.mps.synchronize()
            start=time.perf_counter();flat=[];sizes=[]
            for q in questions:
                flat.extend(candidate_text(state,q['question'],c) for c in q['candidates']);sizes.append(len(q['candidates']))
            x={k:v.to(self.device) for k,v in self.model.encode(flat).items()}
            logits=group_logits(self.model(**x),sizes)/self.temperature
            probs=logits.softmax(-1).cpu().tolist()
            if self.device=='mps':torch.mps.synchronize()
            elapsed=(time.perf_counter()-start)*1000
        return {'engine':self.checkpoint,'model_sha256':self.selection.get('sha256'),'elapsed_ms':elapsed,'answers':[{'id':q['id'],'choice':max(range(len(q['candidates'])),key=lambda i:p[i]),'probabilities':p[:len(q['candidates'])]} for q,p in zip(questions,probs)],'usage':{'local_model_calls':1,'candidate_encodings':sum(sizes)}}
