import json,hashlib
from pathlib import Path

def test_selected_weights_match_frozen_receipt():
    r=json.loads(Path('models/selection.json').read_text());p=Path('models')/r['selected']/'model.safetensors'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'];assert r['head_weight_delta_l2']>0
