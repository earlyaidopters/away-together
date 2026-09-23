"""App-runs rule (Mark, 22 September 2026): the agency may run a frozen candidate that passed every
registered quality and coverage gate on a fresh round and clearly beats V1 on that same round, even
without beating Jev. This is not a Jev superiority claim; that still requires experiments/v2/promote.py."""
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, '.')
from experiments.v2.freeze_candidate import verify, sha

FREEZE = 'experiments/v2/freezes/deeper-fp16-20260921.json'
ROUND = Path('experiments/v2/runs/round1-deeper-fp16')
V1_COMPARISON = Path('experiments/v3/runs/v1-vs-v2-round1.json')
QUALITY_GATES = ['macro_f1_at_least_085', 'false_accept_rate_at_most_005', 'nonzero_correct_accepts', 'gold_meets_acceptance_recall_at_least_half']

def main():
    freeze = json.loads(Path(FREEZE).read_text()); verify(freeze)
    if json.loads((ROUND / 'freeze.json').read_text()) != freeze: raise SystemExit('Round used a different frozen model')
    report = json.loads((ROUND / 'paired-report.json').read_text())
    failed = [g for g in QUALITY_GATES if not report['gates'][g]]
    if failed: raise SystemExit(f'Quality gates failed: {failed}')
    v1 = json.loads(V1_COMPARISON.read_text())
    if v1['corpus_sha256'] != json.loads((ROUND / 'data-manifest.json').read_text())['sha256'] or v1['v2_minus_v1_ci95_scenario_bootstrap'][0] <= 0:
        raise SystemExit('V2 does not clearly beat V1 on the same round')
    pointer = {'kind': 'deberta-travel-v2', 'basis': 'app-quality-gates', 'checkpoint': freeze['checkpoint'], 'model_sha256': freeze['model_sha256'],
               'freeze_file': FREEZE, 'freeze_sha256': sha(FREEZE), 'promoted_utc': datetime.now(timezone.utc).isoformat(),
               'evidence': [{'round': str(ROUND), 'data_manifest_sha256': sha(ROUND / 'data-manifest.json'),
                             'local_raw_sha256': sha(ROUND / 'deberta-travel-v2-travel-fresh.jsonl'), 'jev_raw_sha256': sha(ROUND / 'jev-travel-fresh.jsonl'),
                             'paired_report_sha256': sha(ROUND / 'paired-report.json'), 'recomputed_report': report}],
               'v1_comparison': {'file': str(V1_COMPARISON), 'sha256': sha(V1_COMPARISON), **v1},
               'quality_gates_passed': QUALITY_GATES, 'superiority_gate_passed': report['gates']['positive_paired_accuracy_interval'],
               'claim_scope': 'Runs the agency because it passed the fresh-round quality and coverage gates and beat V1 on the same 360 scenarios. It did not beat Jev (95.28% vs 98.61%). Synthetic references, not human validation or booking safety.'}
    dest = Path('models/active-model.json')
    if dest.exists():
        old = dest.read_bytes(); archive = dest.parent / 'promotion-history'; archive.mkdir(exist_ok=True)
        (archive / (hashlib.sha256(old).hexdigest() + '.json')).write_bytes(old)
    tmp = dest.with_suffix('.tmp'); tmp.write_text(json.dumps(pointer, indent=2)); tmp.replace(dest)
    print('Active for the app:', pointer['model_sha256'][:12], '| restart the agency server to load it')

if __name__ == '__main__':
    main()
