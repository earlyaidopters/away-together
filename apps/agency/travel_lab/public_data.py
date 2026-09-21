"""Pinned public test manifests; references stay out of model inputs."""
import json,sys,hashlib
from pathlib import Path
from datasets import load_dataset

def main():
    out=Path('data/public');out.mkdir(parents=True,exist_ok=True)
    workflows=['agent_trace_observability','customer_service','invoice_processing','security_incidents']
    for workflow in workflows:
        ds=load_dataset('LocalLLaMA/typed-decisions',workflow,split='test',revision='ea9306458d6e9563628369a3d1e72e362fb381d2')
        rows=[]
        for row in ds:
            r={k:json.loads(row[k]) if isinstance(row[k],str) else row[k] for k in ['state','questions','gold']};r.update({'id':row['id'],'workflow':workflow});rows.append(r)
        p=out/f'typed-{workflow}.jsonl';p.write_text(''.join(json.dumps(r)+'\n' for r in rows));print(workflow,len(rows),sum(len(r['questions']) for r in rows),flush=True)
    sys.path.insert(0,str(Path('vendor/jev-benchmarks/src').resolve()))
    from jev_benchmarks.config import load_config
    from jev_benchmarks.data import load_examples
    conf=load_config(Path('vendor/jev-benchmarks/configs/pilot-v1.yaml'))
    rows=[x.to_dict() for x in load_examples(conf)]
    (out/'btzsc-pilot.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    manifest={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':len(p.read_text().splitlines())} for p in out.glob('*.jsonl')}
    Path('data/manifests/public.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest),flush=True)
if __name__=='__main__':main()
