"""Promote only a replicated, frozen travel win. Run after reviewing evidence.
The localhost server must be restarted afterward to load the new selection.
"""
import argparse,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
from experiments.v2.freeze_candidate import verify,sha
from experiments.v2.paired_report import compare

def read(path):return [json.loads(x) for x in Path(path).read_text().splitlines()]

def promote(freeze_path,round_paths):
 if len(round_paths)<2:raise ValueError('Fresh replication is required')
 if len(set(map(str,round_paths)))!=len(round_paths):raise ValueError('Repeated run directory is not replication')
 freeze=json.loads(Path(freeze_path).read_text());verify(freeze);evidence=[];seen_inputs=set()
 for path in map(Path,round_paths):
  if json.loads((path/'freeze.json').read_text())!=freeze:raise ValueError('Round used a different frozen model')
  manifest=json.loads((path/'data-manifest.json').read_text())
  if manifest['freeze_sha256']!=sha(freeze_path):raise ValueError('Final data belongs to another freeze')
  inputs=json.loads((path/'travel-fresh-input-manifest.json').read_text());hashes={r['input_sha256'] for r in inputs}
  if len(inputs)<300 or len(hashes)!=len(inputs):raise ValueError('Insufficient or duplicate fresh inputs')
  if hashes&seen_inputs:raise ValueError('Replication repeats inputs from a previous round')
  seen_inputs.update(hashes)
  local=path/'deberta-travel-v2-travel-fresh.jsonl';jev=path/'jev-travel-fresh.jsonl'
  a,b=read(local),read(jev)
  if any(not r.get('error') and r.get('raw',{}).get('model_sha256')!=freeze['model_sha256'] for r in a):raise ValueError('Raw results came from another checkpoint')
  if {r['id'] for r in a}!={r['id'] for r in inputs}:raise ValueError('Evaluation does not cover frozen input manifest')
  report=compare(a,b)
  if not report['round_qualifies']:raise ValueError('Round fails preregistered gates: '+str(path))
  evidence.append({'round':str(path),'data_manifest_sha256':sha(path/'data-manifest.json'),'local_raw_sha256':sha(local),'jev_raw_sha256':sha(jev),'recomputed_report':report})
 pointer={'kind':'deberta-travel-v2','checkpoint':freeze['checkpoint'],'model_sha256':freeze['model_sha256'],'freeze_file':str(freeze_path),'freeze_sha256':sha(freeze_path),'promoted_utc':datetime.now(timezone.utc).isoformat(),'evidence':evidence,'claim_scope':'Replicated synthetic travel reference agreement only; not universal superiority or booking safety.'}
 dest=Path('models/active-model.json');dest.parent.mkdir(exist_ok=True)
 if dest.exists():
  old=dest.read_bytes();archive=dest.parent/'promotion-history';archive.mkdir(exist_ok=True);(archive/(hashlib.sha256(old).hexdigest()+'.json')).write_bytes(old)
 temporary=dest.with_suffix('.tmp');temporary.write_text(json.dumps(pointer,indent=2));temporary.replace(dest)
 return pointer

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--freeze',required=True);p.add_argument('--round',action='append',required=True);a=p.parse_args();result=promote(a.freeze,a.round);print('Promoted',result['model_sha256'],'Restart localhost server to load it.')
