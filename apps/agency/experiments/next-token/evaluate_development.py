"""Development comparator only. No final evaluation or acceptance qualification."""
import json, sys, hashlib
import torch, transformers
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import NextTokenEngine, ROOT
from travel_lab.evaluate import read, evaluate_lane

engine = NextTokenEngine()
identity = dict(pin=engine.pin, source_sha256=engine.source_sha256,
    evaluator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    runtime={'python': sys.version, 'torch': torch.__version__, 'transformers': transformers.__version__,
             'device': engine.device, 'attention': 'sdpa', 'max_input_tokens': 2048},
    data={s: hashlib.sha256(Path(f'experiments/v2/data/{s}.jsonl').read_bytes()).hexdigest()
          for s in ['dev', 'robustness-dev']}, precision=str(engine.dtype))
digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:12]
out = ROOT / 'runs' / digest
out.mkdir(parents=True, exist_ok=True)
(out / 'provenance.json').write_text(json.dumps(identity, indent=2))
rows = read('experiments/v2/data/dev.jsonl') + read('experiments/v2/data/robustness-dev.jsonl')
parity = []
for row in rows[:2]:
    qs = [{k: q[k] for k in ['id', 'question', 'candidates']} for q in row['questions']]
    batched = engine.predict(row['state'], qs)
    serial = [engine.predict(row['state'], [q])['answers'][0] for q in qs]
    parity.append({'id': row['id'], 'batched': batched, 'serial': serial,
        'max_probability_delta': max(abs(x-y) for a,b in zip(batched['answers'], serial)
            for x,y in zip(a['probabilities'], b['probabilities'])),
        'choices_match': all(a['choice'] == b['choice'] for a,b in zip(batched['answers'], serial))})
(out / 'pretrained-batch-parity.json').write_text(json.dumps(parity, indent=2))
if any(not p['choices_match'] or p['max_probability_delta'] > .002 for p in parity):
    raise ValueError('Actual pretrained batch/serial parity needs investigation before evaluation')
permutations = []
for row in rows[:12]:
    qs = [{k: q[k] for k in ['id', 'question', 'candidates']} for q in row['questions']]
    original = engine.predict(row['state'], qs)
    rotated = [{**q, 'candidates': q['candidates'][1:] + q['candidates'][:1]} for q in qs]
    variant = engine.predict(row['state'], rotated)
    permutations.append({'id': row['id'], 'original': original, 'rotated': variant,
        'same_semantic_choices': [a['choice'] == (b['choice'] + 1) % len(q['candidates'])
            for q, a, b in zip(qs, original['answers'], variant['answers'])]})
(out / 'candidate-order-diagnostic.json').write_text(json.dumps(permutations, indent=2))
print(evaluate_lane(engine, 'travel-development-v2', rows, out, threshold=1.01), flush=True)
