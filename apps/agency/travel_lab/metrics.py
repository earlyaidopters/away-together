import numpy as np
from sklearn.metrics import f1_score

def summarise(rows):
    decisions=[d for r in rows for d in r['decisions']];total=len(decisions)
    if not total:return {'status':'empty','decisions':0}
    successes=[d for d in decisions if d.get('pred') is not None];correct=sum(d.get('pred')==d['gold'] for d in decisions)
    nll=[];brier=[];confidence=[];right=[];soft_ce=[];soft_brier=[];score_mae=[]
    for d in successes:
        p=np.array(d['probabilities'],float);g=d['gold'];onehot=np.eye(len(p))[g]
        nll.append(-np.log(max(p[g],1e-12)));brier.append(np.sum((p-onehot)**2));confidence.append(float(max(p)));right.append(d['pred']==g)
        if d.get('soft_gold') is not None:
            ref=np.array(d['soft_gold']);soft_ce.append(-np.sum(ref*np.log(np.maximum(p,1e-12))));soft_brier.append(np.sum((p-ref)**2))
        if d.get('score_levels') is not None:
            levels=np.array(d['score_levels']);score_mae.append(abs(np.dot(p,levels)-np.dot(d['soft_gold'],levels)))
    ece=0
    for lo in np.linspace(0,.9,10):
        idx=[i for i,c in enumerate(confidence) if lo<=c<(lo+.1+1e-8 if lo>.89 else lo+.1)]
        if idx:ece+=len(idx)/max(1,len(successes))*abs(np.mean([right[i] for i in idx])-np.mean([confidence[i] for i in idx]))
    # Macro F1 is per decision field, then equally averaged; unrelated label indices are never pooled.
    groups={}
    for d in decisions:groups.setdefault(d['field'],[]).append(d)
    fs=[]
    for group in groups.values():
        labels=list(range(len(group[0]['labels'])))
        fs.append(f1_score([d['gold'] for d in group],[d['pred'] if d.get('pred') is not None else -1 for d in group],labels=labels,average='macro',zero_division=0))
    rates=np.array([sum(d.get('pred')==d['gold'] for d in r['decisions'])/len(r['decisions']) for r in rows]);rng=np.random.default_rng(20260920)
    boot=[float(np.mean(rates[rng.integers(len(rates),size=len(rates))])) for _ in range(2000)]
    latencies=[r['elapsed_ms'] for r in rows if not r.get('error')]
    accepts=[d for d in decisions if d.get('accepted')]
    bad=sum(d['gold']!=0 for d in accepts)
    result={'status':'completed','scenarios':len(rows),'decisions':total,'successful_decisions':len(successes),'failed_decisions':total-len(successes),'accuracy':correct/total,'macro_f1_by_field':float(np.mean(fs)),'all_correct_rate':float(np.mean([all(d.get('pred')==d['gold'] for d in r['decisions']) for r in rows])),'accuracy_ci95_scenario_bootstrap':np.quantile(boot,[.025,.975]).tolist(),'nll_success_only':float(np.mean(nll)) if nll else None,'brier_success_only':float(np.mean(brier)) if brier else None,'ece_success_only':float(ece),'p50_ms':float(np.median(latencies)) if latencies else None,'p95_ms':float(np.quantile(latencies,.95)) if latencies else None,'accepted':len(accepts),'false_accepts':bad,'false_accept_rate':bad/len(accepts) if accepts else None,'review_rate':sum(d.get('review',False) for d in decisions)/total}
    if soft_ce:result.update({'soft_reference_cross_entropy':float(np.mean(soft_ce)),'soft_reference_brier':float(np.mean(soft_brier)),'score_expected_mae':float(np.mean(score_mae)) if score_mae else None})
    return result
