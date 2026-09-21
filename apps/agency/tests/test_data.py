import json,hashlib
from pathlib import Path

def test_manifest_and_split_integrity():
    manifest=json.loads(Path('data/manifests/travel.json').read_text());ids=set();states=set();families=set()
    for split,s in manifest['splits'].items():
        raw=Path(f'data/{split}.jsonl').read_bytes();assert hashlib.sha256(raw).hexdigest()==s['sha256']
        rows=[json.loads(x) for x in raw.splitlines()];assert len(rows)==s['scenarios']
        f={r['family'] for r in rows};assert not families&f;families|=f
        for r in rows:
            assert r['id'] not in ids;ids.add(r['id']);assert r['state'] not in states;states.add(r['state'])
            assert len(r['questions'])==4
            for q in r['questions']:assert q['gold']==r['oracle'][q['id']];assert f"[{q['evidence']}]" in r['state']
def test_public_manifest_counts():
    manifest=json.loads(Path('data/manifests/public.json').read_text());assert sum(x['rows'] for k,x in manifest.items() if k.startswith('typed-'))==400
    rows=[json.loads(x) for x in Path('data/public/btzsc-pilot.jsonl').read_text().splitlines()]
    assert len(rows)==300;assert len({x['example_id'] for x in rows})==300
    assert len(next(x for x in rows if x['dataset']=='banking77')['labels'])==72
