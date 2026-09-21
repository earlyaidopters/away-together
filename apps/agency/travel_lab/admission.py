import json,time,hashlib
from pathlib import Path
import torch
from .model import CandidateModel,group_logits

def main():
    torch.manual_seed(20260920); torch.set_num_threads(8)
    out=Path('runs/preflight');out.mkdir(parents=True,exist_ok=True)
    t=time.time();m=CandidateModel();m.freeze();m.eval()
    device='mps' if torch.backends.mps.is_available() else 'cpu'
    texts=['Hotel offers cash refunds before arrival. Requirement: cash refund. Decision: meets.','Hotel offers vouchers only. Requirement: cash refund. Decision: violates.']
    x=m.encode(texts)
    with torch.no_grad(): cpu=m(**x)
    m.to(device)
    with torch.no_grad(): gpu=m(**{k:v.to(device) for k,v in x.items()}).cpu()
    parity=(cpu-gpu).abs().max().item(); print('device',device,'parity',parity,flush=True)
    timings={}
    for length in [256,512,1024]:
        inp={'input_ids':torch.full((6,length),100,device=device,dtype=torch.long),'attention_mask':torch.ones((6,length),device=device,dtype=torch.long)}
        m.train();opt=torch.optim.AdamW(m.head.parameters(),lr=.001)
        losses=[];start=time.time()
        for step in range(20):
            opt.zero_grad(); logits=group_logits(m(**inp),[3,3]);loss=torch.nn.functional.cross_entropy(logits,torch.tensor([0,1],device=device));loss.backward();opt.step();losses.append(loss.item())
        if device=='mps':torch.mps.synchronize()
        timings[str(length)]={'seconds_per_update':(time.time()-start)/20,'finite':bool(all(torch.isfinite(torch.tensor(losses))))}
        print(length,timings[str(length)],flush=True)
    torch.save(m.head.state_dict(),out/'head-admission.pt');m.head.load_state_dict(torch.load(out/'head-admission.pt',weights_only=True))
    result={'device':device,'parity_max_abs':parity,'timings':timings,'head_reload':True,'elapsed_seconds':time.time()-t,'torch':torch.__version__}
    (out/'admission.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
if __name__=='__main__':main()
