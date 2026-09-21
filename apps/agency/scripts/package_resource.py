from pathlib import Path
import hashlib,json,zipfile,csv
P=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
rows={}
for lane,n in [('travel-test',300),('travel-challenge',100),('typed-independent',400),('btzsc-independent',300)]:
 a=[json.loads(x) for x in (P/f'runs/evaluation/jev-{lane}.jsonl').read_text().splitlines()]
 b=[json.loads(x) for x in (P/f'runs/evaluation/travel-nli-{lane}.jsonl').read_text().splitlines()]
 assert len(a)==len(b)==n
 assert len({x['id'] for x in a})==n
 assert {x['id'] for x in a}=={x['id'] for x in b}
 rows[lane]={'raw_jev_rows':len(a),'unique_jev_ids':len({x['id'] for x in a}),'local_rows':len(b),'duplicate_ids':0,'malformed_rows':0}
expected=json.loads((P/'models/selection.json').read_text())['sha256'];assert sha(P/'models/travel-nli/model.safetensors')==expected
(P/'output/qa/receipt-audit.json').write_text(json.dumps({'lanes':rows,'scored_jev_requests':1100,'model_hash_verified':expected},indent=2))
roots=['explainer','travel_lab','tests','scripts','config','data','research','production','app/src','app/tests','app/public','app/dist','models/travel-nli','runs/evaluation','runs/demo','runs/preflight','output/benchmarks','output/pdf','output/audio','output/captures','output/thumbnails','output/qa']
files=[]
for root in roots:
 files.extend(q for q in (P/root).rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.suffix not in ['.pyc'])
# Retain development, failed experiments, frozen evaluations and reproduction code.
# Historical large weights are reproducible from scripts. Ship the frozen final
# challenger even if it fails promotion, so the actual result is reproducible.
for root in ['experiments/v2','experiments/next-token','experiments/diffusion']:
 for q in (P/root).rglob('*'):
  if not q.is_file() or '__pycache__' in q.parts or q.suffix=='.pyc':continue
  if q.suffix in ['.safetensors','.bin','.pt','.pth']:continue
  files.append(q)
lessons=P/'experiments/laya/LESSONS.md'
if lessons.exists():files.append(lessons)
# Ship pinned vision source, assets and receipts, not private caches or environments.
vision=P/'experiments/openjev-vision'
if vision.exists():
 for name in ['README.md','pin.json','vendor-source-manifest.json','runtime-requirements.lock.txt','image-generation.json','real-image-observations.json']:
  item=vision/name
  if item.exists():files.append(item)
 source_manifest=vision/'vendor-source-manifest.json'
 if source_manifest.exists():
  for rel,digest in json.loads(source_manifest.read_text()).items():
   item=(vision/'vendor'/rel).resolve();item.relative_to((vision/'vendor').resolve())
   if sha(item)!=digest:raise ValueError('Pinned OpenJev source changed: '+rel)
   files.append(item)
active=P/'models/active-model.json'
frozen_final=P/'experiments/v2/freezes/deeper-fp16-20260921.json'
checkpoint_receipts=[]
if frozen_final.exists():
 freeze=json.loads(frozen_final.read_text())
 checkpoint=(P/freeze['checkpoint']).resolve();checkpoint.relative_to(P)
 for rel,digest in freeze['checkpoint_files'].items():
  item=(checkpoint/rel).resolve();item.relative_to(checkpoint)
  if sha(item)!=digest:raise ValueError('Frozen final checkpoint changed: '+rel)
 for rel,digest in freeze['inference_source_files'].items():
  if sha(P/rel)!=digest:raise ValueError('Frozen final inference source changed: '+rel)
 files.extend(q for q in checkpoint.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.suffix!='.pyc')
 checkpoint_receipts.append({'role':'frozen-final-challenger','freeze_file':str(frozen_final.relative_to(P)),'freeze_sha256':sha(frozen_final),'checkpoint':freeze['checkpoint'],'model_sha256':freeze['model_sha256'],'promotion_implied':False})
(P/'RESOURCE-CHECKPOINTS.json').write_text(json.dumps(checkpoint_receipts,indent=2))
files.append(P/'RESOURCE-CHECKPOINTS.json')
if active.exists():
 pointer=json.loads(active.read_text())
 if pointer['kind']!='deberta-travel-v2':raise ValueError('Unsupported promoted model packaging')
 checkpoint=(P/pointer['checkpoint']).resolve()
 checkpoint.relative_to(P) # Refuse accidental packaging from outside this project.
 freeze_path=(P/pointer['freeze_file']).resolve();freeze_path.relative_to(P)
 if sha(freeze_path)!=pointer['freeze_sha256']:raise ValueError('Promoted freeze changed')
 freeze=json.loads(freeze_path.read_text())
 if freeze['model_sha256']!=pointer['model_sha256']:raise ValueError('Promotion and freeze disagree')
 for rel,digest in freeze['checkpoint_files'].items():
  item=(checkpoint/rel).resolve();item.relative_to(checkpoint)
  if sha(item)!=digest:raise ValueError('Promoted checkpoint changed: '+rel)
 for rel,digest in freeze['inference_source_files'].items():
  if sha(P/rel)!=digest:raise ValueError('Frozen inference source changed: '+rel)
 files.extend(q for q in checkpoint.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.suffix!='.pyc')
 files.extend([active,freeze_path])
for f in ['AGENTS.md','README.md','START-HERE.md','MODEL-CARD.md','THIRD-PARTY-NOTICES.md','ASSET-MANIFEST.json','pyproject.toml','uv.lock','requirements.lock.txt','Dockerfile','Launch Travel Agency.command','Launch Vision.command','app/package.json','app/package-lock.json','app/index.html','app/tsconfig.json','app/vite.config.ts','models/selection.json','models/first-candidate-selection.json','runs/training.jsonl','runs/interventions.jsonl','runs/metadata-correction.json']:
 if (P/f).exists():files.append(P/f)
# Completion contains this ZIP's own hash and is therefore an external receipt.
files=sorted(set(files)-{P/'output/qa/COMPLETION.json'});manifest=[{'path':str(q.relative_to(P)),'bytes':q.stat().st_size,'sha256':sha(q)} for q in files]
resource=P/'output/resource';resource.mkdir(parents=True,exist_ok=True)
next_manifest=resource/'MANIFEST.next.json';next_manifest.write_text(json.dumps(manifest,indent=2))
next_zip=resource/'Away-Together-Complete.building.zip'
with zipfile.ZipFile(next_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for q in files:z.write(q,'away-together/'+str(q.relative_to(P)))
 z.write(next_manifest,'away-together/MANIFEST.json')
with zipfile.ZipFile(next_zip) as z:
 assert z.testzip() is None
current=resource/'Away-Together-Complete.zip'
if current.exists():
 history=resource/'history';history.mkdir(exist_ok=True)
 previous=history/('Away-Together-'+sha(current)+'.zip')
 if not previous.exists():current.rename(previous)
next_zip.replace(current);next_manifest.replace(resource/'MANIFEST.json')
print(json.dumps({'files':len(files),'zip_bytes':current.stat().st_size,'zip_integrity_verified':True,'next':'Run scripts/verify_resource.py for manifest/credential/extraction checks, then offline runtime verification.'}))
