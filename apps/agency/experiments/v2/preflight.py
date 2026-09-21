"""Validate the exact development corpus before spending time training."""
import json,hashlib
from pathlib import Path
from travel_lab.nli import HYPOTHESES

def preflight(tokenizer,root=Path('experiments/v2')):
 report={'splits':{},'source_overlap':{},'max_tokens_allowed':512};sources={};texts={}
 for split in ['train','dev','calibration','robustness-dev']:
  path=root/f'data/{split}.jsonl';rows=[json.loads(line) for line in path.read_text().splitlines()]
  ids=[r['id'] for r in rows]
  if len(set(ids))!=len(ids):raise ValueError('Duplicate IDs in '+split)
  sources[split]=set();texts[split]=set();lengths=[];overlong=[]
  for row in rows:
   texts[split].add(row['state'])
   fields={q['id'] for q in row['questions']}
   if fields!=set(HYPOTHESES) or len(row['questions'])!=4:raise ValueError('Missing/duplicate travel fields')
   for q in row['questions']:
    if q['gold'] not in [0,1,2] or q['candidates']!=HYPOTHESES[q['id']]:raise ValueError('Invalid reference schema')
    n=len(tokenizer(row['state'],HYPOTHESES[q['id']][0],truncation=False)['input_ids']);lengths.append(n)
    if n>512:overlong.append({'id':row['id'],'field':q['id'],'tokens':n})
   if split!='robustness-dev':
    src=list(row['provenance'].values())+row.get('composition',{}).get('extra_sources',[])
    sources[split].update((s['source'],s['index']) for s in src)
  report['splits'][split]={'scenarios':len(rows),'unique_full_documents':len(texts[split]),'unique_source_clauses':len(sources[split]),'max_tokens':max(lengths),'overlong':overlong,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 for a,b in [('train','dev'),('train','calibration'),('dev','calibration'),('train','robustness-dev')]:
  common=sources[a]&sources[b];same=texts[a]&texts[b];report['source_overlap'][a+'/'+b]={'clauses':len(common),'full_documents':len(same)}
  if common or same:raise ValueError('Split contamination: '+a+'/'+b)
 (root/'runs/data-preflight.json').write_text(json.dumps(report,indent=2))
 if any(v['overlong'] for v in report['splits'].values()):raise ValueError('Overlong documents: inspect runs/data-preflight.json; no truncation or silent removal permitted')
 return report
