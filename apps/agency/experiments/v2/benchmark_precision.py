"""Development-only precision/speed comparison. Run with no competing GPU job."""
import argparse, gc, hashlib, json, platform, random, sys, time
from pathlib import Path
import numpy as np
import torch, transformers
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.v2.engine import DebertaEngine
from travel_lab.evaluate import read
from sklearn.metrics import f1_score
from travel_lab.nli import HYPOTHESES

p = argparse.ArgumentParser()
p.add_argument('--checkpoint', required=True, type=Path)
p.add_argument('--output', required=True, type=Path)
a = p.parse_args()
if a.output.exists(): raise FileExistsError('Preserve prior benchmark; use a new output')
a.output.mkdir(parents=True)
rows = read('experiments/v2/data/dev.jsonl') + read('experiments/v2/data/robustness-dev.jsonl')
sample = random.Random(20260921).sample(rows, 48)
selection = json.loads((a.checkpoint / 'selection.json').read_text())
def payload(row):
    return [{k:q[k] for k in ['id','question','candidates']} for q in row['questions']]
def load(precision):
    engine = DebertaEngine(a.checkpoint)
    if engine.device != 'mps': raise RuntimeError('This experiment targets local MPS')
    if precision == 'float16': engine.model.half()
    for row in sample[:6]: engine.predict(row['state'], payload(row))
    return engine
def release(engine):
    del engine
    gc.collect()
    torch.mps.empty_cache()

report = {'scope':'Development precision experiment; no final claim or deployment',
    'checkpoint':str(a.checkpoint), 'model_sha256':selection['sha256'],
    'selection_sha256':hashlib.sha256((a.checkpoint/'selection.json').read_bytes()).hexdigest(),
    'benchmark_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'engine_sha256':hashlib.sha256(Path('experiments/v2/engine.py').read_bytes()).hexdigest(),
    'runtime':{'torch':torch.__version__,'transformers':transformers.__version__,
               'platform':platform.platform(),'python':sys.version},
    'data_sha256':{s:hashlib.sha256(Path(f'experiments/v2/data/{s}.jsonl').read_bytes()).hexdigest()
                   for s in ['dev','robustness-dev']},
    'timing_protocol':'FP32,FP16,FP16,FP32; independent reload from original weights each block; six warmups; 48 fixed documents twice per block. Timings exclude checkpoint load. No result caching.',
    'timing_blocks':[], 'precision_quality':{}, 'offer_batching':{}}
for block, precision in enumerate(['float32','float16','float16','float32']):
    engine = load(precision)
    times=[]
    for repeat in range(2):
        for row in sample:
            result=engine.predict(row['state'],payload(row)); times.append(result['elapsed_ms'])
    entry={'block':block,'precision':precision,'p50_ms':float(np.median(times)),
           'p95_ms':float(np.percentile(times,95)),'times_ms':times}
    report['timing_blocks'].append(entry)
    print({k:v for k,v in entry.items() if k!='times_ms'},flush=True)
    del engine
    gc.collect();torch.mps.empty_cache()
    (a.output/'report.json').write_text(json.dumps(report,indent=2))

predictions={}
for precision in ['float32','float16']:
    engine=load(precision); predictions[precision]=[]; by_field={}; accepted=bad=gold_meets=correct_meets=0
    with (a.output/(precision+'-development.jsonl')).open('x') as file:
        for i,row in enumerate(rows):
            result=engine.predict(row['state'],payload(row))
            file.write(json.dumps({'id':row['id'],'result':result})+'\n')
            for q,answer in zip(row['questions'],result['answers']):
                probs=answer['probabilities']
                if not all(np.isfinite(probs)):raise ValueError('Non-finite probabilities')
                pred=answer['choice'];gold=q['gold']
                predictions[precision].append(pred)
                by_field.setdefault(q['id'],[]).append((gold,pred))
                gold_meets+=gold==0
                take=pred==0 and probs[pred]>=selection['accept_threshold']
                accepted+=take;bad+=take and gold!=0;correct_meets+=take and gold==0
            if i%100==0:print(precision,i,len(rows),flush=True)
    pairs=[pair for group in by_field.values() for pair in group]
    report['precision_quality'][precision]={'accuracy':sum(g==p for g,p in pairs)/len(pairs),
        'macro_f1_by_field':float(np.mean([f1_score([g for g,p in group],[p for g,p in group],labels=[0,1,2],average='macro',zero_division=0) for group in by_field.values()])),
        'accepted':accepted,'false_accepts':bad,'false_accept_rate':bad/accepted if accepted else None,
        'correct_meets_recall':correct_meets/gold_meets,
        'scope':'Development only; chosen checkpoint calibration reused unchanged. Calibration/final must be revalidated before using a different precision.'}
    # Same 48 full documents, with four native policy decisions per document.
    # This measures a potential bulk implementation, not current HTTP behavior.
    baseline=[answer['choice'] for row in sample
              for answer in engine.predict(row['state'],payload(row))['answers']]
    batching=[]
    for offers_per_batch in [1,4,8]:
        timings=[];changes=[]
        for repeat in range(3):
            torch.mps.synchronize();start=time.perf_counter();preds=[]
            with torch.inference_mode():
                for offset in range(0,len(sample),offers_per_batch):
                    items=[(row['state'],q['id']) for row in sample[offset:offset+offers_per_batch] for q in row['questions']]
                    encoded=engine.encode([state for state,field in items],[HYPOTHESES[field][0] for state,field in items])
                    logits=engine.model(**encoded).logits[:,[engine.labels['entailment'],engine.labels['contradiction'],engine.labels['neutral']]]
                    preds.extend(logits.argmax(-1).cpu().tolist())
            torch.mps.synchronize();timings.append((time.perf_counter()-start)*1000)
            changes.append(sum(x!=y for x,y in zip(baseline,preds)))
        batching.append({'offers_per_batch':offers_per_batch,'policy_pairs_per_batch':offers_per_batch*4,
            '48_offer_elapsed_ms':timings,'median_ms_per_offer':float(np.median(timings))/len(sample),
            'median_offers_per_second':len(sample)*1000/float(np.median(timings)),
            'changed_choices_vs_serving':changes,
            'scope':'Experimental full-document bulk forward loop; excludes HTTP, disk receipts, probability calibration and UI; includes tokenization and CPU choice transfer.'})
    report['offer_batching'][precision]=batching
    del engine
    gc.collect();torch.mps.empty_cache()
    (a.output/'report.json').write_text(json.dumps(report,indent=2))
report['changed_development_decisions']=sum(x!=y for x,y in zip(predictions['float32'],predictions['float16']))
report['status']='Complete; inspect speed/quality tradeoff before changing production inference'
(a.output/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['precision_quality'],indent=2),flush=True)
