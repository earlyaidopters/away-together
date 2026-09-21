"""Summarize completed candidates; never promotes or hides failed experiments."""
import json,hashlib
from pathlib import Path
root=Path('experiments/v2');cal=[json.loads(x) for x in (root/'data/calibration.jsonl').read_text().splitlines()];gold_meets=sum(q['gold']==0 for r in cal for q in r['questions']);records=[]
for path in sorted((root/'models').glob('*/selection.json')):
 s=json.loads(path.read_text());checkpoint=path.parent;actual=hashlib.sha256((checkpoint/'model.safetensors').read_bytes()).hexdigest()
 if actual!=s['sha256']:raise ValueError('Checkpoint hash mismatch: '+str(checkpoint))
 chosen=next(r for r in s['history'] if r['epoch']==s['best_epoch']);accepted=s['calibration_accepted'];error=s['calibration_accepted_error'];coverage=accepted*(1-(error or 0))/gold_meets
 records.append({'checkpoint':str(checkpoint),'sha256':actual,'parent_checkpoint_sha256':s.get('parent_checkpoint_sha256'),'parent_checkpoint':s.get('parent_checkpoint'),'selected_epoch_in_run':s['best_epoch'],'development_accuracy':chosen['dev']['accuracy'],'development_macro_f1':s['dev_best_macro_f1'],'calibration_false_accept_rate':error,'calibration_correct_meets_recall':coverage,'accept_threshold':s['accept_threshold'],'elapsed_seconds_training_and_evaluation':s['seconds'],'all_completed_epochs':s['history'],'final_status':'Not established by this development ledger'})
by_path={r['checkpoint']:r for r in records}
for r in records:
 chain=[];current=r;seen=set()
 while current:
  if current['checkpoint'] in seen:raise ValueError('Cyclic checkpoint lineage')
  seen.add(current['checkpoint']);chain.append(current['checkpoint']);parent=by_path.get(current['parent_checkpoint'])
  if parent and parent['sha256']!=current['parent_checkpoint_sha256']:raise ValueError('Parent hash mismatch')
  current=parent
 r['available_parent_chain']=chain
 r['recorded_ancestry_elapsed_seconds']=sum(x['elapsed_seconds_training_and_evaluation'] for x in records if x['checkpoint'] in chain)
report={'scope':'V2 completed local training experiments only. Excludes V1, data generation/auditing, downloads, and separate serving diagnostics. Elapsed time includes evaluation and selection, not pure training time. Parent-chain sums include discarded epochs incurred while selecting weights. No monetary value assigned to local hardware or electricity.','candidates':records,'total_completed_v2_run_seconds':sum(r['elapsed_seconds_training_and_evaluation'] for r in records),'jev_development':json.loads((root/'runs/jev-development/jev-travel-development-v2-metrics.json').read_text())}
(root/'runs/experiment-ledger.json').write_text(json.dumps(report,indent=2))
print(json.dumps([{k:r[k] for k in ['checkpoint','development_macro_f1','calibration_correct_meets_recall','elapsed_seconds_training_and_evaluation']} for r in records],indent=2))
