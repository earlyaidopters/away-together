"""Measure fresh localhost requests, separately from browser presentation time.

Run only when generation/training/public inference is idle. A cold claim requires
an explicitly restarted server and --cold-start; this script never restarts it.
All responses, including failures, are retained. No result cache is used.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import time

import requests


def percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lo = int(position)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def run(base_url, output, scans=3, cold_start=False):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    session = requests.Session()
    def read(endpoint):
        response = session.get(base_url + endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    catalogue = read('/api/catalogue')
    status = read('/api/status')
    selection = status['selection']
    if cold_start and status.get('engine_loaded') is not False:
        raise ValueError('Cold timing requires server status to confirm engine_loaded=false; restart the current server first')
    profiles = [{k: p[k] for k in ('id', 'budget', 'requirements')}
                for p in catalogue['profiles']]
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
                'base_url': base_url, 'selection': selection,
                'catalogue_sha256': hashlib.sha256(json.dumps(catalogue, sort_keys=True).encode()).hexdigest(),
                'offers': len(catalogue['offers']), 'profiles': len(profiles),
                'scans': scans, 'cold_start_requested': cold_start,
                'engine_loaded_before_first_request': status.get('engine_loaded'),
                'boundary': 'Client wall time for sequential real HTTP requests; excludes browser rendering and presentation delays.'}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    samples = []
    seen_runs = set()
    def request(offer, phase):
        started = time.perf_counter()
        sample = {'phase': phase, 'offer_id': offer['id']}
        try:
            response = session.post(base_url + '/api/decide',
                                    json={'offer_id': offer['id'], 'profiles': profiles}, timeout=45)
            sample['http_status'] = response.status_code
            sample['response'] = response.json()
            response.raise_for_status()
            receipt = sample['response']
            if receipt['mode'] != 'live' or receipt['run_id'] in seen_runs:
                raise ValueError('Response is not a unique live run')
            seen_runs.add(receipt['run_id'])
            if set(receipt['profiles']) != {p['id'] for p in profiles}:
                raise ValueError('Response does not cover every profile')
            sample['model_ms'] = receipt['elapsed_ms']
        except Exception as error:
            sample['error'] = str(error)
            raise
        finally:
            sample['client_ms'] = (time.perf_counter() - started) * 1000
            samples.append(sample)
            with (output / 'requests.jsonl').open('a') as handle:
                handle.write(json.dumps(sample) + '\n')
        return sample
    report = {'status': 'running', 'scans': []}
    try:
        first = request(catalogue['offers'][0], 'first-request')
        report['first_request'] = {k: first[k] for k in ('client_ms', 'model_ms')}
        report['first_request']['cold_start'] = cold_start
        for scan in range(scans):
            phase = f'warm-scan-{scan + 1}'
            started = time.perf_counter()
            receipts = [request(offer, phase) for offer in catalogue['offers']]
            ranked = []
            for offer, sample in zip(catalogue['offers'], receipts):
                statuses = [p['status'] for p in sample['response']['profiles'].values()]
                ranked.append({'id': offer['id'], 'price': offer['price'],
                               'matches': statuses.count('match'),
                               'declines': statuses.count('decline'),
                               'reviews': statuses.count('review')})
            ranked.sort(key=lambda x: (-x['matches'], x['declines'], x['price'], x['id']))
            report['scans'].append({'phase': phase, 'client_wall_ms': (time.perf_counter() - started) * 1000,
                                    'model_total_ms': sum(r['model_ms'] for r in receipts), 'ranked': ranked})
            print(phase, round(report['scans'][-1]['client_wall_ms']), 'ms', flush=True)
        warm = [s for s in samples if s['phase'].startswith('warm-scan')]
        report['warm_requests'] = {'count': len(warm),
                                   'client_p50_ms': statistics.median(s['client_ms'] for s in warm),
                                   'client_p95_ms': percentile([s['client_ms'] for s in warm], .95),
                                   'model_p50_ms': statistics.median(s['model_ms'] for s in warm)}
        report['status'] = 'completed'
    except Exception as error:
        report.update(status='failed', error=str(error))
        raise
    finally:
        report['requests_recorded'] = len(samples)
        report['failures'] = sum('error' in s for s in samples)
        (output / 'report.json').write_text(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8765')
    parser.add_argument('--out', required=True)
    parser.add_argument('--scans', type=int, default=3)
    parser.add_argument('--cold-start', action='store_true')
    args = parser.parse_args()
    if args.scans < 1:
        parser.error('--scans must be positive')
    run(args.base_url.rstrip('/'), args.out, args.scans, args.cold_start)
