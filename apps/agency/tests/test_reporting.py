import json
from pathlib import Path
import pytest
from travel_lab.reporting import active_report, active_errors, digest


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))
    return path


def promotion_fixture():
    freeze = write('experiments/v2/freezes/test.json', {'model_sha256': 'weights'})
    evidence = []
    for name in ['round-one', 'round-two']:
        data = write(f'experiments/v2/final/{name}/test.jsonl', {'id': name, 'state': 'Complete original document'})
        folder = Path('experiments/v2/runs') / name
        manifest = write(folder / 'data-manifest.json', {'sha256': digest(data)})
        local = write(folder / 'deberta-travel-v2-travel-fresh.jsonl', {'id': name, 'decisions': [{'field': 'refund', 'gold': 0, 'pred': 1}]})
        remote = write(folder / 'jev-travel-fresh.jsonl', {'id': name, 'decisions': [{'field': 'refund', 'gold': 0, 'pred': 0}]})
        evidence.append({'round': str(folder), 'data_manifest_sha256': digest(manifest),
                         'local_raw_sha256': digest(local), 'jev_raw_sha256': digest(remote),
                         'recomputed_report': {'round_qualifies': True, 'local': {'accuracy': .95}, 'jev': {'accuracy': .9}}})
    return write('models/active-model.json', {'kind': 'deberta-travel-v2', 'model_sha256': 'weights',
                 'freeze_file': str(freeze), 'freeze_sha256': digest(freeze), 'evidence': evidence,
                 'claim_scope': 'Synthetic only'})


def test_unpromoted_model_retains_original_report(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    write('output/benchmarks/summary.json', {'status': 'Original failed V1'})
    assert active_report() == {'status': 'Original failed V1'}
    assert active_errors() == []


def test_promoted_reports_and_errors_follow_matching_rounds(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    promotion_fixture()
    report = active_report()
    assert len(report['rounds']) == 2
    assert report['lanes']['round-two / local']['accuracy'] == .95
    assert [r['id'] for r in active_errors()] == ['round-one', 'round-two']
    assert active_errors()[0]['state'] == 'Complete original document'


def test_changed_promoted_receipt_is_rejected(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    promotion_fixture()
    write('experiments/v2/runs/round-one/jev-travel-fresh.jsonl', {'changed': True})
    with pytest.raises(ValueError, match='receipt changed'):
        active_report()


def test_challenger_evidence_is_separate_and_hash_checked(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    write('output/benchmarks/summary.json', {'status': 'Original failed V1'})
    source = write('experiments/final-result.json', {'round_qualifies': False})
    challenger = {'active_in_app': False, 'source_hashes': {str(source): digest(source)}}
    write('output/benchmarks/frozen-v2-summary.json', challenger)
    report = active_report()
    assert report['status'] == 'Original failed V1'
    assert report['challenger'] == challenger
    write(source, {'round_qualifies': True})
    with pytest.raises(ValueError, match='challenger report source changed'):
        active_report()
