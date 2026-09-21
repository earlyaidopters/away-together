"""Independent public lanes, kept separate from fresh travel qualification."""
import argparse,json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from experiments.v2.freeze_candidate import verify,sha
from experiments.v2.engine import DebertaEngine
from travel_lab.jev import JevEngine
from travel_lab.evaluate import typed,btzsc,evaluate_lane

def main():
 p=argparse.ArgumentParser();p.add_argument('--freeze',required=True);p.add_argument('--out',required=True);p.add_argument('--engine',choices=['both','local','jev'],default='both');a=p.parse_args()
 freeze=json.loads(Path(a.freeze).read_text());verify(freeze)
 manifests=json.loads(Path('data/manifests/public.json').read_text())
 for filename,meta in manifests.items():
  if sha(Path('data/public')/filename)!=meta['sha256']:raise ValueError('Pinned public dataset changed: '+filename)
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 provenance={'freeze':freeze,'datasets':manifests,'scope':'Independent public reference agreement. Typed tasks are normalized to candidate choice; not a reproduction of the vendor native typed API harness. Upstream exposure is documented separately. No public result may tune the frozen model.'}
 path=out/'public-protocol.json'
 if path.exists() and json.loads(path.read_text())!=provenance:raise ValueError('Public run provenance changed')
 path.write_text(json.dumps(provenance,indent=2))
 threshold=json.loads((Path(freeze['checkpoint'])/'selection.json').read_text())['accept_threshold']
 engines=[]
 if a.engine in ['both','local']:engines.append(DebertaEngine(freeze['checkpoint']))
 if a.engine in ['both','jev']:engines.append(JevEngine())
 for name,data in [('typed-independent',list(typed())),('btzsc-independent',list(btzsc()))]:
  for engine in engines:
   print(name,engine.name,evaluate_lane(engine,name,data,out,threshold),flush=True)
if __name__=='__main__':main()
