"""Reproduce and launch the pinned Apple Silicon image backend on localhost:8081."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import urllib.request
import venv

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'experiments/openjev-vision'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--setup',action='store_true');parser.add_argument('--background',action='store_true');args=parser.parse_args()
    if platform.system()!='Darwin' or platform.machine()!='arm64':
        raise SystemExit('This launcher requires Apple Silicon. See experiments/openjev-vision/README.md for scope.')
    pin=json.loads((BASE/'pin.json').read_text());python=BASE/'runtime/bin/python';vendor=BASE/'vendor'
    if args.setup:
        if not python.exists():venv.EnvBuilder(with_pip=True).create(BASE/'runtime')
        if not (vendor/'openjev/api.py').exists():
            subprocess.run(['git','clone',pin['repository'],str(vendor)],check=True)
            subprocess.run(['git','-C',str(vendor),'checkout',pin['commit']],check=True)
        # Source archive ships the exact pinned vendor tree; git metadata is excluded.
        if (vendor/'.git').exists():
            actual=subprocess.check_output(['git','-C',str(vendor),'rev-parse','HEAD'],text=True).strip()
            if actual!=pin['commit']:raise SystemExit('Vendor checkout differs from the pinned revision')
        for name,digest in json.loads((BASE/'vendor-source-manifest.json').read_text()).items():
            if hashlib.sha256((vendor/name).read_bytes()).hexdigest()!=digest:
                raise SystemExit('Pinned OpenJev source differs: '+name)
        subprocess.run([str(python),'-m','pip','install','-c',str(BASE/'runtime-requirements.lock.txt'),'-e',str(vendor)+'[mlx]'],check=True)
        from huggingface_hub import snapshot_download
        model=snapshot_download(pin['model'],revision=pin['model_revision'])
        (BASE/'model-path.txt').write_text(model+'\n')
    if not python.exists() or not (BASE/'model-path.txt').exists():
        raise SystemExit('Run .venv/bin/python scripts/start_vision.py --setup --background first. The model download is about 16 GB.')
    try:
        with urllib.request.urlopen('http://127.0.0.1:8081/v1/models',timeout=3) as response:
            if response.status==200:print('Vision service already responding on localhost:8081');return
    except Exception:pass
    env=dict(os.environ);env.update(OPENJEV_BACKEND='mlx',OPENJEV_MLX_MODEL=(BASE/'model-path.txt').read_text().strip(),OPENJEV_HOST='127.0.0.1',OPENJEV_PORT='8081',HF_HUB_OFFLINE='1')
    command=[str(python),'-m','openjev']
    if args.background:
        with (BASE/'server.log').open('a') as log:
            child=subprocess.Popen(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        (BASE/'server-pid.json').write_text(json.dumps({'pid':child.pid,'port':8081}))
        print('Starting vision service:',child.pid,'Log:',BASE/'server.log')
    else:subprocess.run(command,cwd=ROOT,env=env,check=True)

if __name__=='__main__':main()
