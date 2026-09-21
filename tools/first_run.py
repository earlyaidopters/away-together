"""Inspect prerequisites and run the existing agency. Never installs or retrains silently."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,urllib.request
ROOT=Path(__file__).resolve().parents[1];AGENCY=ROOT/'apps/agency'
def check():
    checks={}
    for name in ['uv','node','npm']:checks[name]=shutil.which(name) is not None
    checks['text_weights']=(AGENCY/'models/selection.json').exists()
    if checks['text_weights']:
        selection=json.loads((AGENCY/'models/selection.json').read_text());selected=selection.get('selected','');checks['text_weights']=bool(selected) and (AGENCY/'models'/selected/'model.safetensors').is_file()
    if checks['node']:
        checks['node_22_plus']=int(subprocess.check_output(['node','--version'],text=True).strip().lstrip('v').split('.')[0])>=22
    checks['built_frontend']=(AGENCY/'app/dist/index.html').exists()
    checks['environment']=(AGENCY/'.venv/bin/python').exists() or (AGENCY/'.venv/Scripts/python.exe').exists()
    return checks
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--start',action='store_true');p.add_argument('--probe',action='store_true');a=p.parse_args()
    if a.probe:
        try:
            with urllib.request.urlopen('http://127.0.0.1:8765/api/status',timeout=5) as r:d=json.load(r)
            print(json.dumps({'service':'agency','reachable':True,'model_selected':bool(d.get('ready'))}));sys.exit(0)
        except Exception:print('Agency is unavailable. Start it in a separate terminal; see docs/SETUP.md.');sys.exit(1)
    state=check();print(json.dumps(state,indent=2))
    if not all(state.values()):
        print('Complete the missing steps in docs/SETUP.md. Downloads and environment installation are explicit steps.');sys.exit(1)
    if a.start:raise SystemExit(subprocess.call(['uv','run','uvicorn','travel_lab.serve:app','--host','127.0.0.1','--port','8765'],cwd=AGENCY))
    print('Prerequisites present. Run with --start, then open http://localhost:8765 and check a holiday.')
