import argparse,json,csv,html
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .metrics import summarise

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',default='overnight-20260920');args=parser.parse_args();out=Path('output/benchmarks');out.mkdir(exist_ok=True,parents=True)
    metrics={}
    for p in Path('runs/evaluation').glob('*-metrics.json'):metrics[p.name.removesuffix('-metrics.json')]=json.loads(p.read_text())
    selection=json.loads(Path('models/selection.json').read_text());lanes={}
    for name in ['travel-test','travel-challenge','typed-independent','btzsc-independent']:
        lanes[name]=metrics.get('travel-nli-'+name,{'status':'not run'})
    lanes['jev-head-to-head']=metrics.get('jev-travel-test',{'status':'not run'})
    lanes['official-typesafe']={'status':'not reproduced','reason':'Official charts are available; complete accessible exact cases/harness not verified. Independent typed-decisions is not official.'}
    summary={'run_id':args.run,'selected_model':selection,'lanes':lanes,'all_models':metrics,'truth_boundaries':['Travel references are synthetic, generated from a small template grammar, not human-reviewed real inventory.','Each split uses one prose family per class/task; lexical family coverage is narrow. Scenario bootstrap intervals are conditional on this corpus and do not measure template-population uncertainty.','All scenarios recombine four three-way policy dimensions: at most 81 semantic combinations per split. Counts do not imply 1200 independent real-world situations.','Independent typed decisions measures agreement with a roughly 4B teacher, not verified truth.','NLI starting weights were previously trained on a classification mixture including AG News, Banking77 and emotion domains. Public pilot results are not claims of untouched zero-shot task transfer.','Jev results, where present, are fresh observational API calls against frozen identical candidate-choice inputs. No Jev outputs inform local training or changes. This standardized adapter is not the official native typed harness.','Local latency includes tokenization and synchronized device inference, excludes loading and visual reveal. Local electricity and hardware are not free.','The final model is frozen before final test scoring; final errors are not used to tune it.']}
    paired={}
    for lane in ['travel-test','travel-challenge','typed-independent','btzsc-independent']:
        lp=Path('runs/evaluation')/f'travel-nli-{lane}.jsonl';jp=Path('runs/evaluation')/f'jev-{lane}.jsonl'
        if lp.exists() and jp.exists():
            local={r['id']:r for r in [json.loads(x) for x in lp.read_text().splitlines()]};remote={r['id']:r for r in [json.loads(x) for x in jp.read_text().splitlines()]};ids=sorted(local.keys()&remote.keys())
            diffs=[]
            for key in ids:
                a=local[key]['decisions'];b=remote[key]['decisions'];diffs.append(sum(d['pred']==d['gold'] for d in a)/len(a)-sum(d['pred']==d['gold'] for d in b)/len(b))
            rng=np.random.default_rng(20260920);arr=np.array(diffs);boot=[np.mean(arr[rng.integers(len(arr),size=len(arr))]) for _ in range(2000)]
            paired[lane]={'matched_scenarios':len(ids),'local_minus_jev_accuracy':float(np.mean(arr)),'paired_scenario_bootstrap_ci95':np.quantile(boot,[.025,.975]).tolist()}
    usage_rows=[]
    for p in Path('runs/evaluation').glob('jev-*.jsonl'):
        usage_rows.extend(json.loads(x).get('raw',{}).get('usage',{}) or {} for x in p.read_text().splitlines())
    tokens=sum(r.get('input_tokens',0) for r in usage_rows)
    warmup_tokens=sum((json.loads(p.read_text()).get('usage') or {}).get('input_tokens',0) for p in Path('runs/evaluation').glob('jev-*-warmup.json'))
    summary['product_gate']={'target_macro_f1':.85,'target_false_accept_rate':.05,'passed':False,'reason':'Held-out travel macro F1 and false-accept rate both miss preregistered goals; use only as an experimental demo.'};summary['paired_comparisons']=paired;summary['jev_cost']={'scored_input_tokens':tokens,'estimated_scored_usd':tokens*.042/1e6,'input_usd_per_million':.042,'source':'classifier.dev/docs, retrieved 20 September 2026','billing_invoice':False,'warmups_excluded_from_scored_cost':True,'warmup_input_tokens':warmup_tokens,'estimated_total_usd_including_warmups':(tokens+warmup_tokens)*.042/1e6,'scored_requests':len(usage_rows),'total_requests_including_warmups':len(usage_rows)+4}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    records=[{'model_lane':k,**{j:v for j,v in m.items() if isinstance(v,(str,int,float)) or v is None}} for k,m in metrics.items()]
    columns=sorted(set(k for r in records for k in r))
    with (out/'metrics.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(records)
    plt.rcParams.update({'font.family':'sans-serif','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'figure.facecolor':'#f3f5f1','axes.facecolor':'#f3f5f1','text.color':'#203d36','axes.labelcolor':'#203d36'})
    models=['base-trained','modernbert-nli-baseline','travel-nli','jev'];labels=['Base encoder fine-tuned','Pretrained NLI baseline','Locally adapted NLI','Jev · fresh API calls'];colors=['#aab3a5','#b6c49e','#2c654e','#d6a956']
    for lane,title in [('travel-test','New wording, held-out travel cases'),('travel-challenge','Harder clauses and injection attempts'),('typed-independent','Independent workflow reference agreement'),('btzsc-independent','Independent classification pilot')]:
        fig,ax=plt.subplots(figsize=(16,9),dpi=120);fig.subplots_adjust(left=.30,right=.94,top=.77,bottom=.23)
        values=[metrics.get(m+'-'+lane,{}).get('accuracy',0)*100 for m in models];ys=np.arange(len(models))
        ax.barh(ys,values,color=colors,height=.5);ax.set_yticks(ys,labels,fontsize=16);ax.set_xlim(0,112);ax.invert_yaxis();ax.set_xticks([0,25,50,75,100],['0%','25%','50%','75%','100%'],fontsize=13);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
        for i,v in enumerate(values):ax.text(v+1.5,i,f'{v:.1f}%',va='center',fontsize=23,fontweight='bold')
        fig.text(.1,.9,title,fontsize=29,fontweight='bold');fig.text(.1,.84,'Measured agreement · failures included in the denominator',fontsize=16,color='#72816a')
        note='Synthetic templates; not real booking inventory. Identical candidate-choice inputs.' if lane.startswith('travel') else ('Agreement with synthetic teacher distributions, not human truth. Independent benchmark.' if lane.startswith('typed') else '300-example pinned pilot. NLI pretraining includes these task domains.')
        fig.text(.1,.12,note,fontsize=13,color='#72816a');fig.text(.1,.075,f'Run: {args.run} · source: raw JSONL predictions',fontsize=11,color='#94a08a')
        fig.savefig(out/f'{lane}.png');fig.savefig(out/f'{lane}.svg');plt.close(fig)
    # Training curve uses recorded development metrics, not training accuracy.
    history=[json.loads(x) for x in Path('runs/training.jsonl').read_text().splitlines()]
    fig,ax=plt.subplots(figsize=(16,9),dpi=120);fig.subplots_adjust(left=.12,right=.92,top=.8,bottom=.2)
    ax.plot(range(len(history)),[100*r['dev']['macro_f1'] for r in history],marker='o',color='#2c654e',linewidth=3);ax.set_xticks(range(len(history)),[r['stage']+'\nepoch '+str(r['epoch']) for r in history],fontsize=11);ax.set_ylabel('Development macro F1 (%)');ax.set_ylim(0,100);ax.grid(alpha=.15)
    fig.text(.12,.9,'Learning the examples isn’t enough.',fontsize=30,fontweight='bold');fig.text(.12,.85,'Development performance across actual checkpoints',fontsize=16,color='#72816a');fig.savefig(out/'training.png');fig.savefig(out/'training.svg');plt.close(fig)
    md=['# Travel Lab: measured results','',f'Run `{args.run}`. Selected checkpoint `{selection["selected"]}`.','', '## Comparison status','', 'Fresh Jev API calls and local predictions use the same frozen state, question and candidate descriptions. Results apply to these inputs and deployment conditions, not universal model quality.','', '## Results','', '| Model / lane | Agreement | Macro F1 by field | p50 ms | Failed decisions |','|---|---:|---:|---:|---:|']
    for k,v in metrics.items():md.append(f'| {k} | {v["accuracy"]:.3f} | {v["macro_f1_by_field"]:.3f} | {v["p50_ms"] or 0:.1f} | {v["failed_decisions"]} |')
    md+=['','## Boundaries','']+['- '+x for x in summary['truth_boundaries']]
    md+=['','## Reproduction','','Use the pinned uv.lock, dataset manifests, model hashes and raw predictions. Every inference receives only state, instructions and candidate descriptions. Gold, oracle and factors are scoring-only fields. Calibration uses the dedicated calibration split.','', '## Costs','','This run used existing local hardware and the existing Jev API account. No GPU rental. Jev cost estimates use reported input tokens at the verified $0.042 per million input tokens; they are not billing invoices. Electricity and machine depreciation were not instrumented, so local inference is not described as free.','', '## Human audit','','No human label review has occurred. A separate 50-case audit packet is provided; reviewer cells are blank.']
    (out/'RESULTS.md').write_text('\n'.join(md)+'\n')
    rows_html=''.join(f'<tr><td>{html.escape(k)}</td><td>{v["accuracy"]:.1%}</td><td>{v["macro_f1_by_field"]:.3f}</td><td>{(v["p50_ms"] or 0):.0f} ms</td></tr>' for k,v in metrics.items())
    doc=f'''<!doctype html><html><meta charset="utf-8"><title>Travel Lab Results</title><style>body{{font:16px system-ui;background:#f3f5f1;color:#203d36;max-width:1100px;margin:50px auto;padding:0 24px}}h1{{font-size:48px;letter-spacing:-2px}}table{{border-collapse:collapse;width:100%;background:white}}td,th{{padding:14px;text-align:left;border-bottom:1px solid #dde3d7}}img{{width:100%;margin:24px 0}}li{{margin-bottom:12px;line-height:1.5}}.notice{{background:#eee3bd;padding:20px;border-radius:8px}}</style><h1>What the model actually did.</h1><p class="notice">A frozen local model versus fresh Jev API calls. Synthetic travel tests and independent public benchmarks are reported separately.</p><table><tr><th>Model / lane</th><th>Agreement</th><th>Macro F1</th><th>Median latency</th></tr>{rows_html}</table>{''.join(f'<img src="{l}.png" alt="{l} measured chart">' for l in ['travel-test','travel-challenge','typed-independent','btzsc-independent','training'])}<h2>Read these results correctly</h2><ul>{''.join('<li>'+html.escape(x)+'</li>' for x in summary['truth_boundaries'])}</ul><p>Raw data: metrics.csv and summary.json. Model receipts: models/selection.json.</p></html>'''
    (out/'index.html').write_text(doc)
    print(json.dumps({'report':str(out/'RESULTS.md'),'lanes':len(metrics)}))
if __name__=='__main__':main()
