"""Plot completed development evaluations only; never invent pending scores."""
import json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path('experiments/v2');p=root/'runs/deberta-history.json';history=json.loads(p.read_text());out=root/'evidence';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#f5f2ea','axes.labelcolor':'#f5f2ea','xtick.color':'#b7c9ce','ytick.color':'#b7c9ce','axes.facecolor':'#101c23','figure.facecolor':'#101c23'})
fig,axes=plt.subplots(1,2,figsize=(16,9),dpi=110);fig.subplots_adjust(left=.09,right=.94,bottom=.24,top=.72,wspace=.27)
x=[r['epoch'] for r in history]
for ax,metric,title in zip(axes,['accuracy','macro_f1_by_field'],['Accuracy','Macro F1 × 100']):
 for key,label,color in [('dev','Combined development','#8dd9ce'),('authored_robustness_dev','Authored hard cases','#f5b462')]:
  y=[r[key][metric]*100 for r in history];ax.plot(x,y,color=color,marker='o',linewidth=3,markersize=9,label=label)
  ax.text(x[-1]+.035,y[-1],f'{y[-1]:.1f}',color=color,fontsize=17,va='center',fontweight='bold')
 ax.set_ylim(60,100);ax.set_xlim(-.05,max(x)+.3);ax.set_xticks(x,['Pretrained' if i==0 else f'Pass {i}' for i in x]);ax.set_title(title,fontsize=21,loc='left',pad=20,color='#f5f2ea');ax.tick_params(labelsize=14);ax.grid(axis='y',alpha=.12);ax.spines[['top','right']].set_visible(False);ax.spines[['left','bottom']].set_color('#40535b')
 if metric=='macro_f1_by_field':ax.axhline(85,color='#a4b0b6',linestyle='--',alpha=.6);ax.text(.01,85.8,'85 target',color='#a4b0b6',fontsize=13)
axes[0].legend(loc='lower left',frameon=False,labelcolor='#f5f2ea',fontsize=13)
fig.text(.09,.87,'Does travel fine-tuning help?',fontsize=36,fontweight='bold');fig.text(.09,.80,'Completed development measurements from the same held-out inputs.',fontsize=20,color='#b7c9ce')
fig.text(.09,.13,'544 combined scenarios · 144 authored hard cases form a subset of the combined set.',fontsize=15,color='#b7c9ce');fig.text(.09,.085,'Synthetic references. Development selection only. No Jev comparison or final-test claim.',fontsize=15,color='#b7c9ce')
fig.savefig(out/'training-development.png');fig.savefig(out/'training-development.svg');plt.close(fig)
(out/'training-development-source.json').write_text(json.dumps({'history_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'completed_measurements':history,'purpose':'Development receipt, not final validation'},indent=2))
