"""Development-only risk/coverage receipt, using saved serving predictions."""
import argparse,json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
selection=json.loads((args.checkpoint/'selection.json').read_text());paths=sorted(args.results.glob('deberta-travel-v2-travel-*.jsonl'))
if not paths:raise ValueError('No development serving results')
rows=[json.loads(line) for path in paths for line in path.read_text().splitlines()]
if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate cases')
if any(r.get('raw',{}).get('model_sha256')!=selection['sha256'] for r in rows):raise ValueError('Checkpoint mismatch')
ds=[d for r in rows for d in r['decisions']];gold=sum(d['gold']==0 for d in ds)
def point(t):
 accepted=[d for d in ds if d.get('pred')==0 and max(d['probabilities'])>=t]
 errors=sum(d['gold']!=0 for d in accepted)
 return {'threshold':t,'accepted':len(accepted),'false_accepts':errors,'false_accept_rate':errors/len(accepted) if accepted else None,'correct_meets_recall':(len(accepted)-errors)/gold}
curve=[point(i/100) for i in range(50,100)];selected=point(selection['accept_threshold']);shown=[r for r in curve if r['false_accept_rate'] is not None]
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#f5f2ea','axes.labelcolor':'#f5f2ea','xtick.color':'#b7c9ce','ytick.color':'#b7c9ce','axes.facecolor':'#101c23','figure.facecolor':'#101c23'})
fig,ax=plt.subplots(figsize=(14,8),dpi=120);fig.subplots_adjust(left=.13,right=.92,top=.74,bottom=.25)
ax.axvspan(50,100,color='#77cabc',alpha=.07);ax.axhspan(0,5,color='#77cabc',alpha=.08)
ax.plot([r['correct_meets_recall']*100 for r in shown],[r['false_accept_rate']*100 for r in shown],color='#8dd9ce',linewidth=3)
if selected['false_accept_rate'] is not None:
 x=selected['correct_meets_recall']*100;y=selected['false_accept_rate']*100;ax.scatter([x],[y],s=120,color='#f5b462',zorder=5)
 ax.annotate(f'Current threshold {selected["threshold"]:.2f}\n{x:.1f}% qualifying cases accepted\n{y:.1f}% of accepts incorrect',(x,y),xytext=(.08,.75),textcoords='axes fraction',color='#f5b462',fontsize=14,arrowprops={'arrowstyle':'->','color':'#f5b462'},bbox={'facecolor':'#101c23','edgecolor':'none','pad':8})
ax.axvline(50,color='#b7c9ce',linestyle='--',alpha=.7);ax.axhline(5,color='#b7c9ce',linestyle='--',alpha=.7)
ax.set_xlim(0,100);ax.set_ylim(0,max(20,max(r['false_accept_rate']*100 for r in shown)+3));ax.set_xlabel('Qualifying cases correctly accepted (%)',fontsize=16,labelpad=13);ax.set_ylabel('Incorrect share of accepted decisions (%)',fontsize=14,labelpad=12);ax.grid(alpha=.1);ax.spines[['top','right']].set_visible(False)
fig.text(.13,.88,'Being cautious is only half the job.',fontsize=30,fontweight='bold');fig.text(.13,.81,'Target: accept at least half of valid matches, with no more than 5% false accepts.',fontsize=16,color='#b7c9ce')
fig.text(.13,.11,f'{len(rows)} development scenarios · {len(ds)} decisions · {gold} reference meets',fontsize=14,color='#b7c9ce');fig.text(.13,.06,'Synthetic, repeated clauses. Descriptive development curve; final-test qualification remains pending.',fontsize=13,color='#b7c9ce')
args.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(args.output.with_suffix('.png'));fig.savefig(args.output.with_suffix('.svg'));plt.close(fig)
args.output.with_suffix('.json').write_text(json.dumps({'scope':'development only','checkpoint_sha256':selection['sha256'],'inputs':{str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},'selected':selected,'curve':curve},indent=2));print(json.dumps(selected))
