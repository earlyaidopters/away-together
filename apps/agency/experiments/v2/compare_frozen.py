"""Fresh final scoring gate. Requires an explicit frozen candidate and dataset.
This entry point does not generate data, select checkpoints or tune thresholds.
"""
import argparse,json,hashlib,sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from experiments.v2.engine import DebertaEngine
from travel_lab.jev import JevEngine
from travel_lab.evaluate import evaluate_lane,read
from experiments.v2.paired_report import compare
from experiments.v2.freeze_candidate import verify
from experiments.v2.breakdown import breakdown
p=argparse.ArgumentParser();p.add_argument('--freeze',required=True);p.add_argument('--data',required=True);p.add_argument('--round',required=True);args=p.parse_args()
freeze=json.loads(Path(args.freeze).read_text());candidate=Path(freeze['checkpoint']);dataset=Path(args.data)
verify(freeze)
assert freeze['frozen_at_utc']
assert hashlib.sha256((candidate/'model.safetensors').read_bytes()).hexdigest()==freeze['model_sha256'],'weights changed after freeze'
assert hashlib.sha256((candidate/'selection.json').read_bytes()).hexdigest()==freeze['selection_sha256'],'calibration/selection changed after freeze'
manifest=json.loads(dataset.with_suffix('.manifest.json').read_text())
assert manifest['sha256']==hashlib.sha256(dataset.read_bytes()).hexdigest()
assert datetime.fromisoformat(manifest['created_utc'])>datetime.fromisoformat(freeze['frozen_at_utc']),'Final corpus must be created after model freeze'
assert manifest['purpose']=='fresh-final-evaluation'
assert manifest['freeze_sha256']==hashlib.sha256(Path(args.freeze).read_bytes()).hexdigest(),'Dataset belongs to another frozen candidate'
rows=read(dataset);assert len(rows)>=300 and len({r['id'] for r in rows})==len(rows)
assert all(len(r['questions'])==4 for r in rows)
out=Path('experiments/v2/runs')/args.round;out.mkdir(exist_ok=True,parents=True)
for filename,obj in [('freeze.json',freeze),('data-manifest.json',manifest)]:
 previous=out/filename
 if previous.exists():
  assert json.loads(previous.read_text())==obj,'Cannot resume a round with changed model or data'
(out/'freeze.json').write_text(json.dumps(freeze,indent=2));(out/'data-manifest.json').write_text(json.dumps(manifest,indent=2))
local=DebertaEngine(str(candidate));evaluate_lane(local,'travel-fresh',rows,out,local.selection['accept_threshold'])
# The shared Jev adapter's V1 gate is supplemented by the V2 checks above.
remote=JevEngine();evaluate_lane(remote,'travel-fresh',rows,out,.8)
report=compare(read(out/f'{local.name}-travel-fresh.jsonl'),read(out/f'{remote.name}-travel-fresh.jsonl'))
(out/'paired-report.json').write_text(json.dumps(report,indent=2))
for engine in [local,remote]:
 (out/f'{engine.name}-breakdown.json').write_text(json.dumps(breakdown(rows,read(out/f'{engine.name}-travel-fresh.jsonl')),indent=2))
print('Frozen head-to-head saved',out,flush=True)
