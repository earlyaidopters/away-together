"""Paired scenario-level comparison. No model selection or test filtering."""
import argparse
import json
from pathlib import Path
import numpy as np
from travel_lab.metrics import summarise


def compare(local, remote, seed=20260921):
    def index(rows):
        result = {r['id']: r for r in rows}
        if len(result) != len(rows):
            raise ValueError('Duplicate scenario IDs')
        return result
    a, b = index(local), index(remote)
    if not a or a.keys() != b.keys():
        raise ValueError('Both engines must have the same nonempty scenario set')
    differences = []; accept_counts = []; bad_counts = []
    for key in sorted(a):
        left = {d['field']: d for d in a[key]['decisions']}
        right = {d['field']: d for d in b[key]['decisions']}
        if not left or left.keys() != right.keys():
            raise ValueError('Decision fields differ')
        if len(left) != len(a[key]['decisions']) or len(right) != len(b[key]['decisions']):
            raise ValueError('Duplicate decision fields')
        delta = []
        for field in left:
            x, y = left[field], right[field]
            if x['gold'] != y['gold'] or x['labels'] != y['labels']:
                raise ValueError('Reference labels differ')
            delta.append(int(x.get('pred') == x['gold']) - int(y.get('pred') == y['gold']))
        differences.append(np.mean(delta))
        accepted = [d for d in left.values() if d.get('accepted')]
        accept_counts.append(len(accepted)); bad_counts.append(sum(d['gold'] != 0 for d in accepted))
    differences = np.asarray(differences)
    rng = np.random.default_rng(seed)
    accepts_array=np.asarray(accept_counts);bad_array=np.asarray(bad_counts)
    boot=[];bad_boot=[]
    for _ in range(10000):
        indices=rng.integers(len(differences),size=len(differences));boot.append(float(differences[indices].mean()))
        count=accepts_array[indices].sum()
        if count:bad_boot.append(float(bad_array[indices].sum()/count))
    ci = np.quantile(boot, [.025, .975]).tolist()
    lm, rm = summarise(local), summarise(remote)
    # Operational coverage floor registered before any final generation/scoring.
    gold_meets = sum(d['gold'] == 0 for r in local for d in r['decisions'])
    correct_accepts = lm['accepted'] - lm['false_accepts']
    gates = {
        'positive_paired_accuracy_interval': ci[0] > 0,
        'macro_f1_at_least_085': lm['macro_f1_by_field'] >= .85,
        'false_accept_rate_at_most_005': lm['false_accept_rate'] is not None and lm['false_accept_rate'] <= .05,
        'nonzero_correct_accepts': correct_accepts > 0,
        'gold_meets_acceptance_recall_at_least_half': gold_meets > 0 and correct_accepts/gold_meets >= .5,
    }
    return {'local': lm, 'jev': rm, 'paired_accuracy_difference': float(differences.mean()),
            'paired_accuracy_difference_ci95': ci, 'bootstrap_unit': 'whole scenario, preserving four correlated decisions',
            'bootstrap_seed': seed, 'bootstrap_replicates': 10000,
            'acceptance_coverage': lm['accepted']/lm['decisions'],
            'false_accept_rate_ci95_scenario_bootstrap': np.quantile(bad_boot,[.025,.975]).tolist() if bad_boot else None,
            'uncertainty_note': 'Bootstrap bounds are descriptive for this corpus; zero observed errors can yield a degenerate interval and do not prove zero population risk.',
            'gold_meets_acceptance_recall': correct_accepts/gold_meets if gold_meets else None,
            'gates': gates, 'round_qualifies': all(gates.values()),
            'claim_limit': 'One round only. Fresh replication required. Synthetic references are not human validation; repeated source clauses limit population generalization.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--local', required=True)
    p.add_argument('--jev', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    read = lambda path: [json.loads(line) for line in Path(path).read_text().splitlines()]
    report = compare(read(args.local), read(args.jev))
    Path(args.output).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
