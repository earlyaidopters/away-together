import json
from pathlib import Path
import pytest

def test_selected_model_reload_serving_parity():
    p=Path('runs/preflight/reload-parity.json')
    if not p.exists():pytest.skip('Reload receipt not yet produced')
    r=json.loads(p.read_text());assert r['recorded_dev']==r['reloaded_dev'];assert r['single_question_serving_matches_batch'];assert not r['weights_changed']
