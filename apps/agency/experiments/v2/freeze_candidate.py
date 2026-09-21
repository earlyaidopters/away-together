"""Freeze a development-qualified candidate before generating any final data."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

SOURCES = ['experiments/v2/engine.py', 'experiments/v2/compare_frozen.py', 'experiments/v2/breakdown.py',
           'experiments/v2/paired_report.py', 'travel_lab/nli.py',
           'travel_lab/jev.py', 'travel_lab/evaluate.py', 'travel_lab/metrics.py']

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def verify(freeze):
    folder = Path(freeze['checkpoint'])
    for rel, digest in freeze['checkpoint_files'].items():
        if sha(folder/rel) != digest:
            raise ValueError('Frozen checkpoint changed: '+rel)
    for path, digest in freeze['inference_source_files'].items():
        if sha(path) != digest:
            raise ValueError('Frozen inference code changed: '+path)
    return True

def freeze_candidate(checkpoint, output):
    folder, dest = Path(checkpoint), Path(output)
    if dest.exists():
        raise FileExistsError('Freeze records are immutable: '+str(dest))
    s = json.loads((folder/'selection.json').read_text())
    if s['sha256'] != sha(folder/'model.safetensors'):
        raise ValueError('Selection weight hash does not match checkpoint')
    if s['dev_best_macro_f1'] < .85 or s['calibration_accepted'] < 40:
        raise ValueError('Development or calibration does not qualify for freeze')
    if s['calibration_accepted_error'] is None or s['calibration_accepted_error'] > .05:
        raise ValueError('Calibration false accepts exceed target')
    calibration=[json.loads(line) for line in Path('experiments/v2/data/calibration.jsonl').read_text().splitlines()]
    gold_meets=sum(q['gold']==0 for row in calibration for q in row['questions'])
    accepted_correct=s['calibration_accepted']*(1-s['calibration_accepted_error'])
    if not gold_meets or accepted_correct/gold_meets < .5:
        raise ValueError('Calibration accepts fewer than half of genuinely qualifying decisions')
    for path,digest in s.get('training',{}).get('extra_training_files',{}).items():
        if sha(path)!=digest:raise ValueError('Additional training data changed')
    selected = next(r for r in s['history'] if r['epoch'] == s['best_epoch'])
    record = {
        'schema': 2, 'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'checkpoint': str(folder), 'model_sha256': s['sha256'],
        'selection_sha256': sha(folder/'selection.json'),
        'checkpoint_files': {str(p.relative_to(folder)):sha(p) for p in sorted(folder.rglob('*')) if p.is_file()},
        'inference_source_files': {p:sha(p) for p in SOURCES},
        'development_data_files': {str(p):sha(p) for p in sorted(Path('experiments/v2/data').glob('*dev*.jsonl'))},
        'calibration_data_sha256': sha('experiments/v2/data/calibration.jsonl'),
        'training_data_sha256': sha('experiments/v2/data/train.jsonl'),
        'additional_training_files': s.get('training',{}).get('extra_training_files',{}),
        'selected_development_record': selected,
        'accept_threshold': s['accept_threshold'], 'temperature': s['temperature'],
        'selection_rule': 'Highest combined development macro F1; calibration only for temperature and acceptance threshold.',
        'status': 'Frozen candidate, no final win established',
    }
    verify(record)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('x') as f:
        json.dump(record, f, indent=2)
    return record

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', default='experiments/v2/models/deberta-travel')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    print(json.dumps(freeze_candidate(args.checkpoint, args.output), indent=2))
