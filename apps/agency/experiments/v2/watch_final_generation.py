"""Wait for an identified generator, then score only a sealed frozen corpus.

Uses exclusive status/log paths, preserving previous failures. Never repairs
references, retries generation, promotes models or claims a win.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def identity(pid):
    result = subprocess.run(['ps', '-p', str(pid), '-o', 'lstart=', '-o', 'command='],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generation-pid', type=int, required=True)
    parser.add_argument('--freeze', required=True)
    parser.add_argument('--round', required=True)
    parser.add_argument('--status', required=True)
    parser.add_argument('--log', required=True)
    args = parser.parse_args()
    if not args.round.replace('-', '').isalnum():
        parser.error('Invalid round name')
    root = Path('experiments/v2')
    with (root / 'runs' / f'{args.round}-controller.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        status = Path(args.status)
        with status.open('x') as handle:
            handle.write('{}')
        def record(stage, **details):
            payload = {'pid': os.getpid(), 'stage': stage,
                       'utc': datetime.now(timezone.utc).isoformat(), **details}
            temporary = status.with_suffix('.tmp')
            temporary.write_text(json.dumps(payload, indent=2))
            temporary.replace(status)
            print(json.dumps(payload), flush=True)
        child = None
        try:
            original = identity(args.generation_pid)
            if original is None or 'generate_final.py' not in original or f'--round {args.round}' not in original:
                raise RuntimeError('PID is not the expected live generator; inspect state before restarting')
            if Path(args.log).exists():
                raise FileExistsError('Use a new head-to-head log path')
            record('waiting-for-generation', generation_pid=args.generation_pid,
                   generation_identity=original)
            while True:
                current = identity(args.generation_pid)
                if current is None:
                    break
                if current != original:
                    raise RuntimeError('Generator PID was reused; refusing to infer completion')
                time.sleep(5)
            data = root / 'final' / args.round / 'test.jsonl'
            if not data.exists() or not data.with_suffix('.manifest.json').exists():
                raise RuntimeError('Generation ended without sealed data; resolve infrastructure or blind-reference audit before contestant scoring')
            command = [sys.executable, str(root / 'compare_frozen.py'), '--freeze', args.freeze,
                       '--data', str(data), '--round', args.round]
            with Path(args.log).open('x') as log:
                child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                record('frozen-head-to-head', child_pid=child.pid, command=command)
                code = child.wait(timeout=7200)
            if code:
                raise RuntimeError(f'Head-to-head failed with code {code}')
            report = json.loads((root / 'runs' / args.round / 'paired-report.json').read_text())
            record('complete', round_qualifies=report['round_qualifies'],
                   next='Review evidence. Independent fresh replication required before promotion.')
        except BaseException as error:
            if child is not None and child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
            record('failed', error=str(error))
            raise


if __name__ == '__main__':
    main()
