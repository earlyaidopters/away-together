import json
from types import SimpleNamespace
import travel_lab.active_model as active
import travel_lab.serve as service
import experiments.v2.engine as candidate
import experiments.v2.freeze_candidate as freezing


def test_loaded_model_retains_promotion_for_status(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    freeze = tmp_path / 'freeze.json'
    freeze.write_text(json.dumps({'checkpoint': 'selected', 'model_sha256': 'weights'}))
    pointer = {'freeze_file': str(freeze), 'freeze_sha256': 'freeze-hash',
               'checkpoint': 'selected', 'model_sha256': 'weights'}
    selection = {'sha256': 'weights', 'accept_threshold': .89}
    monkeypatch.setattr(active, 'active_selection', lambda: {**selection, 'promotion': pointer})
    monkeypatch.setattr(freezing, 'sha', lambda path: 'freeze-hash')
    monkeypatch.setattr(freezing, 'verify', lambda record: True)
    monkeypatch.setattr(candidate, 'DebertaEngine', lambda path: SimpleNamespace(selection=selection.copy()))
    loaded = active.load_active_engine()
    monkeypatch.setattr(service, 'engine', loaded)
    status = service.status()
    assert status['engine_loaded'] is True
    assert status['selection']['promotion'] == pointer
    assert status['selection']['sha256'] == 'weights'
