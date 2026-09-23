"""Like-for-like: score the frozen V1 app model on the same 360 round-1 scenarios V2 was scored on.
Both models were frozen before this corpus existed. No Jev call, no tuning."""
import hashlib, json, random, sys, time
from pathlib import Path
sys.path.insert(0, '.')
from travel_lab.nli import NLIEngine

DATA = Path('experiments/v2/final/round1-deeper-fp16/test.jsonl')
V2 = Path('experiments/v2/runs/round1-deeper-fp16/deberta-travel-v2-travel-fresh.jsonl')
OUT = Path('experiments/v3/runs/v1-round1-deeper-fp16.jsonl')

def main():
    manifest = json.loads(Path('experiments/v2/runs/round1-deeper-fp16/data-manifest.json').read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == manifest['sha256'], 'round-1 corpus changed'
    engine = NLIEngine(); rows = [json.loads(l) for l in DATA.open()]; out = []
    for row in rows:
        qs = [{k: q[k] for k in ('id', 'question', 'candidates')} for q in row['questions']]
        try:
            r = engine.predict(row['state'], qs)
            out.append({'id': row['id'], 'elapsed_ms': r['elapsed_ms'], 'decisions': [{'field': q['id'], 'gold': q['gold'], 'pred': a['choice'], 'probabilities': a['probabilities']} for q, a in zip(row['questions'], r['answers'])]})
        except Exception as ex:
            out.append({'id': row['id'], 'error': repr(ex)[:200], 'decisions': [{'field': q['id'], 'gold': q['gold'], 'pred': None} for q in row['questions']]})
    OUT.write_text(''.join(json.dumps(r) + '\n' for r in out))
    v2 = {r['id']: r for r in map(json.loads, V2.open())}
    acc = lambda rs: sum(d['pred'] == d['gold'] for r in rs for d in r['decisions']) / sum(len(r['decisions']) for r in rs)
    v1a, v2a = acc(out), acc([v2[r['id']] for r in out])
    diff = lambda ids: sum(sum(d['pred'] == d['gold'] for d in v2[i]['decisions']) - sum(d['pred'] == d['gold'] for d in byid[i]['decisions']) for i in ids) / (4 * len(ids))
    byid = {r['id']: r for r in out}; ids = list(byid); rng = random.Random(20260922)
    boots = sorted(diff([rng.choice(ids) for _ in ids]) for _ in range(5000))
    summary = {'corpus': str(DATA), 'corpus_sha256': manifest['sha256'], 'scenarios': len(out), 'v1_failed': sum('error' in r for r in out),
               'v1_accuracy': v1a, 'v2_accuracy': v2a, 'v2_minus_v1': v2a - v1a, 'v2_minus_v1_ci95_scenario_bootstrap': [boots[124], boots[4874]],
               'v1_median_ms': sorted(r['elapsed_ms'] for r in out if 'elapsed_ms' in r)[len(out) // 2],
               'v2_median_ms': sorted(v2[i]['elapsed_ms'] for i in ids)[len(ids) // 2], 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    Path('experiments/v3/runs/v1-vs-v2-round1.json').write_text(json.dumps(summary, indent=1)); print(json.dumps(summary, indent=1))

if __name__ == '__main__':
    main()
