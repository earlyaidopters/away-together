"""Explicit model selection; V1 stays active until a validated promotion exists."""
import json
from pathlib import Path

POINTER = Path('models/active-model.json')

def active_selection():
    if not POINTER.exists():
        p=Path('models/selection.json')
        return json.loads(p.read_text()) if p.exists() else None
    pointer=json.loads(POINTER.read_text())
    if pointer.get('kind')!='deberta-travel-v2':
        raise ValueError('Unsupported active model')
    selection=json.loads((Path(pointer['checkpoint'])/'selection.json').read_text())
    if selection['sha256']!=pointer['model_sha256']:
        raise ValueError('Active model selection differs from promotion')
    return {**selection,'promotion':pointer}

def load_active_engine():
    selection=active_selection()
    if selection is None:raise ValueError('No trained model is available')
    if selection.get('promotion'):
        from experiments.v2.freeze_candidate import verify,sha
        from experiments.v2.engine import DebertaEngine
        pointer=selection['promotion'];freeze=json.loads(Path(pointer['freeze_file']).read_text())
        if sha(pointer['freeze_file'])!=pointer['freeze_sha256'] or freeze['checkpoint']!=pointer['checkpoint']:
            raise ValueError('Promotion freeze or checkpoint path changed')
        verify(freeze)
        if freeze['model_sha256']!=pointer['model_sha256']:
            raise ValueError('Promotion and frozen model differ')
        loaded=DebertaEngine(pointer['checkpoint'])
        # Keep promotion provenance after the first request. /api/status reads
        # the loaded engine, so dropping this would revert the UI to V1 claims.
        loaded.selection={**loaded.selection,'promotion':pointer}
        return loaded
    if selection.get('architecture')=='nli':
        from .nli import NLIEngine
        return NLIEngine()
    from .engine import LocalEngine
    return LocalEngine()
