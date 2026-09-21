import hashlib
import json
import zipfile
import pytest
from scripts.verify_resource import verify_archive


def archive(path, extra=None, corrupt=False):
    entries = {name: b'{}' for name in ['travel_lab/serve.py', 'models/selection.json',
               'app/dist/index.html', 'pyproject.toml', 'uv.lock', 'START-HERE.md', 'MODEL-CARD.md']}
    entries.update(extra or {})
    manifest = [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                for name, data in entries.items()]
    if corrupt:
        entries['START-HERE.md'] = b'changed'
    with zipfile.ZipFile(path, 'w') as bundle:
        for name, data in entries.items():
            bundle.writestr('away-together/' + name, data)
        bundle.writestr('away-together/MANIFEST.json', json.dumps(manifest))


def test_exact_manifest_extracts(tmp_path):
    path = tmp_path / 'bundle.zip'
    archive(path)
    report = verify_archive(path, tmp_path / 'extract')
    assert report['files_verified'] == 7
    assert report['runtime_verified'] is False
    assert (tmp_path / 'extract/away-together/START-HERE.md').exists()


def test_changed_bytes_refuse_extraction(tmp_path):
    path = tmp_path / 'bundle.zip'
    archive(path, corrupt=True)
    with pytest.raises(ValueError, match='Manifest mismatch'):
        verify_archive(path, tmp_path / 'extract')
    assert not (tmp_path / 'extract').exists()


def test_credential_findings_do_not_print_values(tmp_path):
    path = tmp_path / 'bundle.zip'
    # Deliberately fake test token, constructed so the test source is not a hit.
    token = b'Bearer ' + b'x' * 40
    archive(path, {'private.txt': token})
    report = verify_archive(path, tmp_path / 'extract')
    assert report['status'] == 'needs-review'
    assert report['findings'] == [{'path': 'private.txt', 'category': 'literal-bearer-token'}]
    assert token.decode() not in json.dumps(report)
    assert not (tmp_path / 'extract').exists()


def test_traversal_refused(tmp_path):
    path = tmp_path / 'bundle.zip'
    archive(path, {'../../escape.txt': b'no'})
    with pytest.raises(ValueError, match='Unsafe archive path'):
        verify_archive(path, tmp_path / 'extract')


@pytest.mark.parametrize('changed_weights', [False, True])
def test_unpromoted_challenger_must_match_its_freeze(tmp_path, changed_weights):
    # A self-consistent ZIP manifest must not hide a changed frozen checkpoint.
    weights = b'original frozen weights'
    freeze = {'checkpoint': 'experiments/final-model',
              'model_sha256': hashlib.sha256(weights).hexdigest(),
              'checkpoint_files': {'model.safetensors': hashlib.sha256(weights).hexdigest()},
              'inference_source_files': {'travel_lab/serve.py': hashlib.sha256(b'{}').hexdigest()}}
    frozen_bytes = json.dumps(freeze).encode()
    receipt = [{'freeze_file': 'experiments/freeze.json',
                'freeze_sha256': hashlib.sha256(frozen_bytes).hexdigest(),
                'checkpoint': freeze['checkpoint'], 'model_sha256': freeze['model_sha256']}]
    path = tmp_path / 'bundle.zip'
    archive(path, {'experiments/freeze.json': frozen_bytes,
                   'experiments/final-model/model.safetensors': b'changed weights' if changed_weights else weights,
                   'RESOURCE-CHECKPOINTS.json': json.dumps(receipt).encode()})
    if changed_weights:
        with pytest.raises(ValueError, match='final checkpoint differs'):
            verify_archive(path, tmp_path / 'extract')
    else:
        result = verify_archive(path, tmp_path / 'extract')
        assert result['frozen_challengers_verified'] == 1
        assert result['active_v2'] is False
