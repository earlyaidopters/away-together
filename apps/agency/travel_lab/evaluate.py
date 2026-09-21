import json,time,random,hashlib,argparse
from pathlib import Path
from .nli import HYPOTHESES
from .metrics import summarise

def read(p):return [json.loads(x) for x in Path(p).read_text().splitlines()]
def travel(split):
    for row in read(f'data/{split}.jsonl'):
        qs=[{**q,'candidates':HYPOTHESES[q['id']]} for q in row['questions']]
        yield {'id':row['id'],'state':row['state'],'questions':qs}
def typed():
    for p in sorted(Path('data/public').glob('typed-*.jsonl')):
        for row in read(p):
            qs=[]
            for key,q in row['questions'].items():
                criteria=q.get('criteria',{'false':'The following statement is false: '+q['instructions'],'true':q['instructions']});labels=list(criteria) if isinstance(criteria,dict) else [str(i) for i in range(len(criteria))]
                candidates=list(criteria.values()) if isinstance(criteria,dict) else criteria
                gold=row['gold'][key];probs=gold['probabilities'];soft=[float(probs[k]) for k in labels]
                qs.append({'id':row['workflow']+'/'+key,'question':q['instructions'],'candidates':candidates,'labels':labels,'gold':labels.index(str(gold['label'])),'soft_gold':soft,'score_levels':[int(x) for x in labels] if q['type']=='score' else None,'native':q,'native_id':key})
            yield {'id':row['id'],'state':json.dumps(row['state'],ensure_ascii=False),'questions':qs,'native_state':row['state']}
def btzsc():
    for row in read('data/public/btzsc-pilot.jsonl'):
        yield {'id':row['example_id'],'state':row['text'],'questions':[{'id':row['dataset'],'question':'Which single label best describes the input text?','candidates':row['labels'],'labels':row['labels'],'gold':row['target_index']}]}

def evaluate_lane(engine,name,items,out,threshold=.8):
    out.mkdir(exist_ok=True,parents=True);path=out/f'{engine.name}-{name}.jsonl';prior=read(path) if path.exists() else [];done={r['id'] for r in prior}
    # Persist input hashes before inference; deterministic random order, no tuning.
    items=list(items);random.Random(20260920).shuffle(items)
    manifest=[{'id':r['id'],'input_sha256':hashlib.sha256(json.dumps({'state':r['state'],'questions':[{k:v for k,v in q.items() if k not in ['gold','soft_gold','score_levels','native']} for q in r['questions']]},sort_keys=True).encode()).hexdigest()} for r in items]
    mp=out/f'{name}-input-manifest.json';encoded=json.dumps(manifest,indent=2)
    if mp.exists() and mp.read_text()!=encoded:raise RuntimeError('Frozen inputs changed')
    mp.write_text(encoded)
    warm=list(travel('dev'))[0]
    warm_result=engine.predict(warm['state'],[{k:v for k,v in q.items() if k in ['id','question','candidates','labels']} for q in warm['questions']])
    (out/f'{engine.name}-{name}-warmup.json').write_text(json.dumps(warm_result,indent=2))
    for i,row in enumerate(items):
        if row['id'] in done:continue
        payload=[{k:v for k,v in q.items() if k in ['id','question','candidates','labels']} for q in row['questions']]
        start=time.perf_counter();error=None;answer={}
        try:
            result=engine.predict(row['state'],payload);answer={a['id']:a for a in result['answers']};elapsed=result['elapsed_ms']
        except Exception as e:error=type(e).__name__+': '+str(e);result={};elapsed=(time.perf_counter()-start)*1000
        decisions=[]
        for q in row['questions']:
            a=answer.get(q['id']);pred=a['choice'] if a else None;p=a['probabilities'] if a else None
            decisions.append({'field':q['id'],'labels':q['labels'],'gold':q['gold'],'pred':pred,'probabilities':p,'soft_gold':q.get('soft_gold'),'score_levels':q.get('score_levels'),'accepted':bool(name.startswith('travel') and a and pred==0 and p[pred]>=threshold),'review':bool(name.startswith('travel') and (not a or pred==2 or (pred==0 and p[pred]<threshold)))})
        receipt={'id':row['id'],'engine':engine.name,'elapsed_ms':elapsed,'error':error,'decisions':decisions,'raw':result}
        with path.open('a') as f:f.write(json.dumps(receipt)+'\n');f.flush()
        if i%50==0:print(engine.name,name,i,len(items),error or 'OK',flush=True)
    rows=read(path);metrics=summarise(rows);(out/f'{engine.name}-{name}-metrics.json').write_text(json.dumps(metrics,indent=2));return metrics

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--engine',choices=['trained','baseline','base-head','jev'],default='trained');args=parser.parse_args()
    if args.engine=='jev':
        from .jev import JevEngine
        engine=JevEngine()
    elif args.engine=='base-head':
        from .engine import LocalEngine
        engine=LocalEngine('travel-v1');engine.name='base-trained'
    else:
        from .nli import NLIEngine
        engine=NLIEngine(trained=args.engine=='trained')
    out=Path('runs/evaluation');threshold=engine.selection.get('accept_threshold',.8)
    for name,items in [('travel-test',travel('test')),('travel-challenge',travel('challenge')),('typed-independent',typed()),('btzsc-independent',btzsc())]:
        print(name,evaluate_lane(engine,name,items,out,threshold),flush=True)
if __name__=='__main__':main()
