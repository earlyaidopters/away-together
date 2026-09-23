"""Score reads against fixed labels. Unclear labels excluded. 'visible' precision matters most: a false 'visible' can create a match."""
import json, sys
from pathlib import Path
HERE = Path(__file__).parent / __import__('os').environ.get('VISION_SET', '')
labels = json.loads((HERE / 'labels.json').read_text())
reads = {r['id']: r for r in map(json.loads, open(HERE / (sys.argv[1] if len(sys.argv) > 1 else 'reads-openjev.jsonl')))}
traits = ['pool', 'ocean', 'mountains', 'garden', 'steps', 'ramp']

def rule_visible(rs, trait, k):  # visible when at least k reads say visible with p>=.8
    return sum(r['answers'][trait]['choice'] == 'visible' and r['answers'][trait]['probabilities']['visible'] >= .8 for r in rs) >= k

rows = [(i, t, labels[i][t], reads[i]['reads']) for i in reads for t in traits if labels[i][t] != 'unclear']
n_reads = min(len(r) for *_, r in rows)
print(f'{len(reads)} images, {len(rows)} labelled trait decisions, {n_reads} reads each')
for name, fn in [('single read (current app)', lambda rs, t: rule_visible(rs[:1], t, 1))] + [(f'{k} of {n_reads} reads visible', (lambda k: lambda rs, t: rule_visible(rs, t, k))(k)) for k in range(1, n_reads + 1)]:
    tp = sum(fn(rs, t) and g == 'visible' for _, t, g, rs in rows); fp = sum(fn(rs, t) and g == 'not_visible' for _, t, g, rs in rows)
    fn_ = sum(not fn(rs, t) and g == 'visible' for _, t, g, rs in rows)
    print(f'  {name:28s} visible precision {tp}/{tp+fp}  recall {tp}/{tp+fn_}  false-visible {fp}')
print('per trait, single read: false visible / missed visible')
for t in traits:
    sub = [(i, g, rs) for i, tt, g, rs in rows if tt == t]
    fpv = [i for i, g, rs in sub if rule_visible(rs[:1], t, 1) and g == 'not_visible']
    miss = [i for i, g, rs in sub if not rule_visible(rs[:1], t, 1) and g == 'visible']
    print(f'  {t:9s} FP {fpv}  missed {miss}')
flips = sum(len({r['answers'][t]['choice'] for r in rs}) > 1 for _, t, _, rs in rows)
print(f'reads disagree on {flips}/{len(rows)} decisions')
