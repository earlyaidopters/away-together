"""Serve receipts for the active model; historical reports never become V2 claims."""
import hashlib
import json
from pathlib import Path


def read_json(path):
    return json.loads(Path(path).read_text())


def read_rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def promoted_evidence():
    path = Path('models/active-model.json')
    if not path.exists():
        return None
    pointer = read_json(path)
    if pointer['kind'] != 'deberta-travel-v2' or len(pointer['evidence']) < 2:
        raise ValueError('Active model has no replicated promotion evidence')
    if digest(pointer['freeze_file']) != pointer['freeze_sha256']:
        raise ValueError('Promotion freeze changed')
    if read_json(pointer['freeze_file'])['model_sha256'] != pointer['model_sha256']:
        raise ValueError('Promotion model differs from freeze')
    for evidence in pointer['evidence']:
        folder = Path(evidence['round'])
        for filename, key in [('data-manifest.json', 'data_manifest_sha256'),
                              ('deberta-travel-v2-travel-fresh.jsonl', 'local_raw_sha256'),
                              ('jev-travel-fresh.jsonl', 'jev_raw_sha256')]:
            if digest(folder / filename) != evidence[key]:
                raise ValueError('Promoted evaluation receipt changed: ' + str(folder / filename))
        if not evidence['recomputed_report']['round_qualifies']:
            raise ValueError('Promoted round does not qualify')
    return pointer


def active_report():
    pointer = promoted_evidence()
    if pointer is None:
        old = Path('output/benchmarks/summary.json')
        result = read_json(old) if old.exists() else {'status': 'Evaluation has not completed. No result is implied.'}
        challenger = Path('output/benchmarks/frozen-v2-summary.json')
        if challenger.exists():
            evidence = read_json(challenger)
            for source, expected in evidence['source_hashes'].items():
                if digest(source) != expected:
                    raise ValueError('Frozen challenger report source changed: ' + source)
            result['challenger'] = evidence
        return result
    lanes = {}
    rounds = []
    for evidence in pointer['evidence']:
        name = Path(evidence['round']).name
        report = evidence['recomputed_report']
        rounds.append({'name': name, **report})
        for engine in ['local', 'jev']:
            lanes[f'{name} / {engine}'] = report[engine]
    public = Path('experiments/v2/runs/public-deeper-fp16')
    protocol = public / 'public-protocol.json'
    if protocol.exists() and read_json(protocol)['freeze'] == read_json(pointer['freeze_file']):
        for engine in ['deberta-travel-v2', 'jev']:
            for lane in ['typed-independent', 'btzsc-independent']:
                path = public / f'{engine}-{lane}-metrics.json'
                lanes[f'public / {lane} / {engine}'] = read_json(path) if path.exists() else {'status': 'Pending'}
    return {'status': 'Replicated synthetic travel qualification', 'model_sha256': pointer['model_sha256'],
            'claim_scope': pointer['claim_scope'], 'rounds': rounds, 'lanes': lanes,
            'legacy_charts_scope': 'Earlier V1 experiments, retained as historical evidence.',
            'public_scope': 'Independent normalized candidate-choice tasks. Not the vendor native typed harness. Upstream exposure may apply.'}


def active_errors(limit=5):
    pointer = promoted_evidence()
    if pointer is None:
        datasets = [(Path('data/test.jsonl'), Path('runs/evaluation/travel-nli-travel-test.jsonl'),
                     Path('runs/evaluation/jev-travel-test.jsonl'))]
    else:
        datasets = []
        for evidence in pointer['evidence']:
            folder = Path(evidence['round'])
            data = Path('experiments/v2/final') / folder.name / 'test.jsonl'
            manifest = read_json(folder / 'data-manifest.json')
            if digest(data) != manifest['sha256']:
                raise ValueError('Promoted reference corpus changed')
            datasets.append((data, folder / 'deberta-travel-v2-travel-fresh.jsonl', folder / 'jev-travel-fresh.jsonl'))
    result = []
    for data, local, remote in datasets:
        if not local.exists():
            continue
        scenarios = {row['id']: row for row in read_rows(data)}
        other = {row['id']: row for row in read_rows(remote)} if remote.exists() else {}
        for row in read_rows(local):
            if any(d['pred'] != d['gold'] for d in row['decisions']):
                result.append({'id': row['id'], 'state': scenarios[row['id']]['state'],
                               'local': row['decisions'], 'jev': other.get(row['id'], {}).get('decisions', []),
                               'label_source': 'Synthetic references, not human review'})
            if len(result) == limit:
                return result
    return result
