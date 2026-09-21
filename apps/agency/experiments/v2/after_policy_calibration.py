"""Serialized deeper-layer development experiment; never opens final cases."""
import json, os, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone

root = Path('experiments/v2')
runs = root / 'runs'
status = runs / 'deeper-experiment-status.json'
if status.exists():
    raise FileExistsError('Inspect existing controller before relaunch')

def record(stage, **details):
    value = dict(pid=os.getpid(), stage=stage,
                 utc=datetime.now(timezone.utc).isoformat(), **details)
    status.write_text(json.dumps(value, indent=2))
    print(value, flush=True)

try:
    record('waiting-for-policy-calibration')
    while True:
        prior = json.loads((runs / 'policy-calibration-status.json').read_text())
        if prior['stage'] == 'complete':
            break
        if prior['stage'] == 'failed':
            raise RuntimeError('Prior experiment failed; inspect before proceeding')
        os.kill(prior['pid'], 0)
        time.sleep(5)
    parent = root / 'models/deberta-travel-boundary'
    selection = json.loads((parent / 'selection.json').read_text())
    selected = next(x for x in selection['history'] if x['epoch'] == selection['best_epoch'])
    jev = json.loads((runs / 'jev-development/jev-travel-development-v2-metrics.json').read_text())
    if selected['dev']['accuracy'] > jev['accuracy']:
        record('ready-for-review', reason='Parent already exceeds Jev development accuracy')
    else:
        checkpoint = root / 'models/deberta-travel-deeper'
        commands = [
            ('training', [sys.executable, str(root / 'train_deberta.py'),
                '--init-checkpoint', str(parent), '--output', str(checkpoint),
                '--history', str(runs / 'deberta-deeper-history.json'),
                '--extra-training', str(root / 'data/boundary-train.jsonl'),
                '--epochs', '2', '--lr', '1e-6', '--train-layers', '4']),
            ('diagnostics', [sys.executable, str(root / 'diagnose_development.py'),
                '--checkpoint', str(checkpoint)]),
            ('ledger', [sys.executable, str(root / 'experiment_ledger.py')])]
        for stage, command in commands:
            with (runs / f'deeper-experiment-{stage}.log').open('x') as log:
                process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                record(stage, child_pid=process.pid, command=command,
                       reason='Parent development accuracy remains below Jev; test more trainable layers')
                try:
                    code = process.wait(timeout=10800)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    try:
                        process.wait(timeout=30)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    raise
            if code:
                raise RuntimeError(f'{stage} exited with code {code}')
        record('complete', next='Inspect candidate; no final freeze, evaluation or promotion performed')
except Exception as error:
    record('failed', error=str(error))
    raise
