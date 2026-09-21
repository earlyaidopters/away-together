import json
import pytest
from scripts.benchmark_agency import run


class Response:
    status_code = 200
    def __init__(self, body):
        self.body = body
    def raise_for_status(self):
        pass
    def json(self):
        return self.body


class Session:
    def __init__(self, replay=False):
        self.count = 0
        self.replay = replay
    def get(self, url, **kwargs):
        if url.endswith('/api/status'):
            return Response({'selection': {'sha256': 'test-only'}, 'engine_loaded': True})
        return Response({'offers': [{'id': 'expensive', 'price': 200}, {'id': 'cheap', 'price': 100}],
                         'profiles': [{'id': 'traveller', 'budget': 250, 'requirements': ['refund']}]})
    def post(self, url, **kwargs):
        self.count += 1
        return Response({'mode': 'live', 'run_id': 'reused' if self.replay else str(self.count),
                         'elapsed_ms': 1, 'profiles': {'traveller': {'status': 'match'}}})


def test_live_scan_measures_requests_and_ranks(monkeypatch, tmp_path):
    session = Session()
    monkeypatch.setattr('scripts.benchmark_agency.requests.Session', lambda: session)
    report = run('http://test', tmp_path / 'run', scans=2)
    assert session.count == 5  # First request plus two complete fresh scans.
    assert report['warm_requests']['count'] == 4
    assert report['scans'][0]['ranked'][0]['id'] == 'cheap'
    assert report['first_request']['cold_start'] is False
    assert report['failures'] == 0


def test_reused_receipt_fails_and_preserves_evidence(monkeypatch, tmp_path):
    monkeypatch.setattr('scripts.benchmark_agency.requests.Session', lambda: Session(replay=True))
    folder = tmp_path / 'run'
    with pytest.raises(ValueError, match='unique live run'):
        run('http://test', folder, scans=1)
    report = json.loads((folder / 'report.json').read_text())
    assert report['status'] == 'failed'
    assert report['failures'] == 1
    assert report['requests_recorded'] == 2
    assert len((folder / 'requests.jsonl').read_text().splitlines()) == 2


def test_warm_server_cannot_be_claimed_cold(monkeypatch, tmp_path):
    session = Session()
    monkeypatch.setattr('scripts.benchmark_agency.requests.Session', lambda: session)
    with pytest.raises(ValueError, match='engine_loaded=false'):
        run('http://test', tmp_path / 'run', cold_start=True)
    assert session.count == 0
