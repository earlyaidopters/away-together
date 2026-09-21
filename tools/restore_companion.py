"""Restore missing companion files only, verifying paths and hashes before writing."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,zipfile,stat
parser=argparse.ArgumentParser();parser.add_argument('archive');args=parser.parse_args()
root=Path(__file__).resolve().parents[1]/'apps/agency'
with zipfile.ZipFile(args.archive) as z:
    names=z.namelist()
    if len(names)!=len(set(names)):raise ValueError('Duplicate archive names')
    manifest=json.loads(z.read('away-together/MANIFEST.json'))
    if set(names)!={'away-together/'+r['path'] for r in manifest}|{'away-together/MANIFEST.json'}:raise ValueError('Manifest coverage mismatch')
    pending=[]
    for r in manifest:
        rel=PurePosixPath(r['path'])
        if rel.is_absolute() or '..' in rel.parts or '\\' in str(rel):raise ValueError('Unsafe archive path')
        info=z.getinfo('away-together/'+r['path'])
        if stat.S_ISLNK(info.external_attr>>16):raise ValueError('Symlink rejected')
        target=root/rel
        resolved=target.resolve();resolved.relative_to(root.resolve())
        digest=hashlib.sha256();total=0
        with z.open(info) as f:
            for b in iter(lambda:f.read(1024*1024),b''):digest.update(b);total+=len(b)
        if digest.hexdigest()!=r['sha256'] or total!=r['bytes']:raise ValueError('Archive hash mismatch: '+r['path'])
        if target.exists():
            h=hashlib.sha256()
            with target.open('rb') as f:
                for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
            if h.hexdigest()!=r['sha256']:raise ValueError('Existing source differs; preserve it and use matching release: '+r['path'])
        else:pending.append((info,target))
    for info,target in pending:
        target.parent.mkdir(parents=True,exist_ok=True)
        with z.open(info) as src,target.open('xb') as dst:
            for b in iter(lambda:src.read(1024*1024),b''):dst.write(b)
print(f'Restored {len(pending)} missing files; existing files unchanged.')
