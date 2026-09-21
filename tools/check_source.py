"""Read-only repository source checks; no model loading or network calls."""
from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parents[1]
assert len(json.loads((root/'apps/explainer/scenes.json').read_text()))==14
pins=root/'apps/agency/experiments/openjev-vision'
for path,expected in json.loads((pins/'vendor-source-manifest.json').read_text()).items():
    assert hashlib.sha256((pins/'vendor'/path).read_bytes()).hexdigest()==expected,path
for path in root.rglob('*'):
    if not path.is_file() or any(p in ['.git','node_modules','.venv','runtime'] for p in path.parts):continue
    assert path.stat().st_size<100_000_000,f'Large artifact belongs in release: {path}'
    if path.suffix in ['.py','.json','.md','.js','.ts','.tsx','.html','.command','.toml']:
        text=path.read_text(errors='replace')
        assert not re.search(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}',text),f'Possible credential: {path}'
        assert not re.search(r'Bearer\s+[A-Za-z0-9_.-]{30,}',text),f'Possible credential: {path}'
print('Source checks passed: scene count, pinned upstream hashes, file size and credential patterns.')
