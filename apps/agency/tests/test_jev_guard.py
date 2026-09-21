from pathlib import Path
import pytest

def test_no_api_call_before_model_freeze(monkeypatch,tmp_path):
    from travel_lab.jev import JevEngine
    monkeypatch.chdir(tmp_path)
    with pytest.raises(RuntimeError,match='Freeze the independent model'):JevEngine()
