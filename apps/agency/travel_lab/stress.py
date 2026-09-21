import json,time,random,os
from pathlib import Path
import torch
from .nli import NLIEngine,HYPOTHESES
from .train import load

def main():
    os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
    start=time.perf_counter();engine=NLIEngine();load_seconds=time.perf_counter()-start;rows=[];rng=random.Random(20260920)
    for r in load('dev')[:24]:
        qs=[{**q,'candidates':HYPOTHESES[q['id']]} for q in r['questions']]
        original=engine.predict(r['state'],qs);permuted=[];orders=[]
        for q in qs:
            order=list(range(3));rng.shuffle(order);orders.append(order);permuted.append({**q,'candidates':[q['candidates'][j] for j in order]})
        # Use exactly the same travel input serialization after candidate permutation.
        # The engine must identify travel hypotheses by set, not list order.
        alternate=engine.predict(r['state'],permuted)
        for a,b,order in zip(original['answers'],alternate['answers'],orders):
            restored=[b['probabilities'][order.index(j)] for j in range(3)]
            rows.append({'scenario':r['id'],'field':a['id'],'same_choice':a['choice']==order[b['choice']],'max_probability_delta':max(abs(x-y) for x,y in zip(a['probabilities'],restored))})
    out={'offline_load_seconds':load_seconds,'offline_inference':True,'questions':len(rows),'choice_consistency':sum(r['same_choice'] for r in rows)/len(rows),'max_probability_delta':max(r['max_probability_delta'] for r in rows),'rows':rows}
    Path('runs/preflight/stress.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='rows'})
if __name__=='__main__':main()
