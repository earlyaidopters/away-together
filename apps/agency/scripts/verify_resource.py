"""Verify and safely extract the companion archive without executing its code.

Checks exact manifest coverage, streamed hashes, unsafe paths and credential
patterns. Reports only paths/categories, never matched secret values. Follow
with offline serving/inference from the extracted directory when GPU is idle.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile


TEXT_SUFFIXES = {'.py', '.json', '.jsonl', '.md', '.txt', '.yaml', '.yml', '.toml', '.js', '.ts', '.tsx', '.html', '.csv', '.log', '.command'}
PATTERNS = {
    'private-key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'literal-bearer-token': re.compile(rb'Bearer\s+[A-Za-z0-9_\-\.]{30,}'),
    'api-key-shaped-value': re.compile(rb'\bsk-(?:proj-)?[A-Za-z0-9_\-]{24,}'),
    'aws-access-key': re.compile(rb'\bAKIA[A-Z0-9]{16}\b'),
}


def verify_archive(archive, destination):
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError('Use a new extraction directory; existing evidence is preserved')
    findings = []
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive entries')
        for info in bundle.infolist():
            path = PurePosixPath(info.filename)
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != 'away-together' or '\\' in info.filename:
                raise ValueError('Unsafe archive path')
            if stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Archive symlinks are not supported')
            if any(part in {'.env', '.venv', '.git', 'node_modules', '.aws', '.ssh'} for part in path.parts):
                findings.append({'path': info.filename, 'category': 'private-or-runtime-directory'})
        manifest = json.loads(bundle.read('away-together/MANIFEST.json'))
        indexed = {entry['path']: entry for entry in manifest}
        if len(indexed) != len(manifest):
            raise ValueError('Duplicate manifest entries')
        expected = {'away-together/' + path for path in indexed} | {'away-together/MANIFEST.json'}
        if set(names) != expected:
            raise ValueError('Manifest does not exactly cover the archive')
        for path, entry in indexed.items():
            digest = hashlib.sha256()
            total = 0
            tail = b''
            matches = set()
            scan = PurePosixPath(path).suffix in TEXT_SUFFIXES
            with bundle.open('away-together/' + path) as handle:
                while block := handle.read(1024 * 1024):
                    digest.update(block)
                    total += len(block)
                    if scan:
                        text = tail + block
                        matches.update(name for name, pattern in PATTERNS.items() if pattern.search(text))
                        tail = text[-512:]
            if total != entry['bytes'] or digest.hexdigest() != entry['sha256']:
                raise ValueError('Manifest mismatch: ' + path)
            findings.extend({'path': path, 'category': name} for name in sorted(matches))
        if findings:
            return {'status': 'needs-review', 'files_verified': len(indexed), 'findings': findings,
                    'extracted': False, 'scan_limit': 'Pattern scan only; does not prove absence of every possible secret.'}
        destination.mkdir(parents=True)
        bundle.extractall(destination)
    project = destination / 'away-together'
    required = ['travel_lab/serve.py', 'models/selection.json', 'app/dist/index.html',
                'pyproject.toml', 'uv.lock', 'START-HERE.md', 'MODEL-CARD.md']
    for relative in required:
        if not (project / relative).is_file():
            raise ValueError('Required delivery file missing: ' + relative)
    pointer_path = project / 'models/active-model.json'
    checkpoint_list = project / 'RESOURCE-CHECKPOINTS.json'
    checkpoints = json.loads(checkpoint_list.read_text()) if checkpoint_list.exists() else []
    for record in checkpoints:
        frozen = (project / record['freeze_file']).resolve()
        frozen.relative_to(project.resolve())
        if hashlib.sha256(frozen.read_bytes()).hexdigest() != record['freeze_sha256']:
            raise ValueError('Packaged final freeze differs from checkpoint receipt')
        freeze = json.loads(frozen.read_text())
        if record['checkpoint'] != freeze['checkpoint'] or record['model_sha256'] != freeze['model_sha256']:
            raise ValueError('Checkpoint receipt disagrees with freeze')
        checkpoint = (project / record['checkpoint']).resolve()
        checkpoint.relative_to(project.resolve())
        for relative, expected_hash in freeze['checkpoint_files'].items():
            target = (checkpoint / relative).resolve()
            target.relative_to(checkpoint)
            if indexed[str(target.relative_to(project.resolve()))]['sha256'] != expected_hash:
                raise ValueError('Packaged final checkpoint differs from freeze')
        for relative, expected_hash in freeze['inference_source_files'].items():
            if indexed[relative]['sha256'] != expected_hash:
                raise ValueError('Packaged frozen inference source differs from freeze')
    if pointer_path.exists():
        pointer = json.loads(pointer_path.read_text())
        freeze_path = (project / pointer['freeze_file']).resolve()
        freeze_path.relative_to(project.resolve())
        if hashlib.sha256(freeze_path.read_bytes()).hexdigest() != pointer['freeze_sha256']:
            raise ValueError('Packaged active freeze changed')
        freeze = json.loads(freeze_path.read_text())
        checkpoint = (project / pointer['checkpoint']).resolve()
        checkpoint.relative_to(project.resolve())
        for relative, expected_hash in freeze['checkpoint_files'].items():
            entry = indexed[str((checkpoint / relative).relative_to(project.resolve()))]
            if entry['sha256'] != expected_hash:
                raise ValueError('Packaged active checkpoint differs from freeze')
        for relative, expected_hash in freeze['inference_source_files'].items():
            if indexed[relative]['sha256'] != expected_hash:
                raise ValueError('Packaged inference source differs from freeze')
    return {'status': 'verified-and-extracted', 'files_verified': len(indexed), 'findings': [],
            'project': str(project.resolve()), 'active_v2': pointer_path.exists(),
            'frozen_challengers_verified': len(checkpoints),
            'scan_limit': 'Pattern scan only; does not prove absence of every possible secret.',
            'runtime_verified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive')
    parser.add_argument('--extract-to', required=True)
    parser.add_argument('--report', required=True)
    args = parser.parse_args()
    report = verify_archive(args.archive, args.extract_to)
    Path(args.report).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if report['status'] != 'verified-and-extracted':
        raise SystemExit(1)
