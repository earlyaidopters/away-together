"""Render the completed, paired precision experiment without final-win claims."""
import json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

source=Path('experiments/v2/runs/deeper-precision-benchmark/report.json')
s=json.loads(source.read_text())
if not s.get('status','').startswith('Complete'):raise ValueError('Benchmark incomplete')
groups=['float32','float16'];colors=['#99aeb9','#8dd9ce'];labels=['Full precision','Half precision']
times={g:[t for b in s['timing_blocks'] if b['precision']==g for t in b['times_ms']] for g in groups}
medians=[float(np.median(times[g])) for g in groups];tails=[float(np.percentile(times[g],95)) for g in groups]
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#f5f2ea','axes.labelcolor':'#f5f2ea',
 'xtick.color':'#c6d3d8','ytick.color':'#c6d3d8','axes.facecolor':'#101c23','figure.facecolor':'#101c23'})
fig,(ax,bx)=plt.subplots(1,2,figsize=(14,8),dpi=120,gridspec_kw={'width_ratios':[1.45,1]})
fig.subplots_adjust(left=.10,right=.95,top=.71,bottom=.29,wspace=.4)
x=np.arange(2);width=.3
ax.bar(x-width/2,medians,width,color=colors[1],label='Median')
ax.bar(x+width/2,tails,width,color=colors[0],label='95th percentile')
for xx,values in [(x-width/2,medians),(x+width/2,tails)]:
 for pos,value in zip(xx,values):ax.text(pos,value+8,f'{value:.0f} ms',ha='center',fontsize=15)
ax.set_xticks(x,labels,fontsize=15);ax.set_ylabel('Inference latency (ms)',fontsize=14)
ax.set_ylim(0,max(tails)*1.25);ax.grid(axis='y',alpha=.12);ax.set_axisbelow(True)
ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False,labelcolor='#c6d3d8',loc='upper right',fontsize=11)
bx.axis('off');bx.text(0,.85,f'{medians[0]/medians[1]:.2f}×',fontsize=58,fontweight='bold',color=colors[1]);bx.text(0,.69,'faster median inference',fontsize=18)
bx.text(0,.43,str(s['changed_development_decisions']),fontsize=52,fontweight='bold',color='#f5b462')
bx.text(0,.28,'changed decisions',fontsize=18);bx.text(0,.15,'across 2,176 development decisions',fontsize=13,color='#c6d3d8')
fig.text(.10,.89,'Half precision. Same tested decisions.',fontsize=30,fontweight='bold')
fig.text(.10,.81,'Selected DeBERTa travel model · Apple MPS · no text generation',fontsize=17,color='#c6d3d8')
fig.text(.10,.17,'Same 48 documents × 4 timing blocks × 2 repeats; FP32 → FP16 → FP16 → FP32.',fontsize=13,color='#c6d3d8')
fig.text(.10,.12,'Warm inference only. Excludes model loading and app display; larger offer batches were slower.',fontsize=13,color='#c6d3d8')
fig.text(.10,.065,'Development experiment, not a fresh Jev comparison. Final accuracy and calibration qualification pending.',fontsize=12,color='#c6d3d8')
out=Path('experiments/v2/evidence/precision-speed');out.parent.mkdir(exist_ok=True,parents=True)
fig.savefig(out.with_suffix('.png'));fig.savefig(out.with_suffix('.svg'));plt.close(fig)
out.with_suffix('.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'pooled_median_ms':dict(zip(groups,medians)),'pooled_p95_ms':dict(zip(groups,tails)),
 'ratio':medians[0]/medians[1],'scope':'Development only'},indent=2))
print(out.with_suffix('.png'))
