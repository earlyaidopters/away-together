"""Descriptive subgroup results; never selects or drops final cases."""
from collections import defaultdict

def breakdown(inputs,results):
 source={r['id']:r for r in inputs};groups=defaultdict(list)
 if len(source)!=len(inputs) or len({r['id'] for r in results})!=len(results):raise ValueError('Duplicate IDs')
 if source.keys()!={r['id'] for r in results}:raise ValueError('Input/result sets differ')
 for row in results:
  item=source[row['id']];meta=item.get('composition',item.get('provenance',{}));family=meta.get('family','unspecified');focus=meta.get('focus',meta.get('authored_reference_task'))
  for d in row['decisions']:
   groups['policy/'+d['field']].append(d);groups['family/'+family].append(d)
   if d['field']==focus:groups['focused_policy/'+family].append(d)
 report={}
 for key,ds in groups.items():
  recalls={};confusion={};accepted=[d for d in ds if d.get('accepted')]
  for gold,label in enumerate(ds[0]['labels']):
   cases=[d for d in ds if d['gold']==gold];recalls[label]=sum(d.get('pred')==gold for d in cases)/len(cases) if cases else None
   confusion[label]={p:sum(('failure' if d.get('pred') is None else d['labels'][d['pred']])==p for d in cases) for p in [*ds[0]['labels'],'failure']}
  report[key]={'decisions':len(ds),'accuracy':sum(d.get('pred')==d['gold'] for d in ds)/len(ds),'label_recall':recalls,'confusion':confusion,'accepted':len(accepted),'false_accepts':sum(d['gold']!=0 for d in accepted),'false_accept_rate':sum(d['gold']!=0 for d in accepted)/len(accepted) if accepted else None}
 return {'groups':report,'interpretation':'Descriptive overlapping subgroups, not separate superiority tests. Focused-policy groups contain only the policy deliberately subjected to that case’s complication; family groups contain all four policies.'}
