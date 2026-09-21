import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path('experiments/v2');out=root/'evidence';out.mkdir(exist_ok=True)
a=json.loads((root/'runs/deberta-original-development-metrics.json').read_text());b=json.loads((root/'runs/deberta-robustness-development-metrics.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#f5f2ea','axes.facecolor':'#101c23','figure.facecolor':'#101c23'})
fig=plt.figure(figsize=(16,9),dpi=100);ax=fig.add_axes([.12,.30,.76,.40])
vals=[a['accuracy']*100,b['accuracy']*100];colors=['#8dd9ce','#f5b462']
ax.barh([1,0],vals,color=colors,height=.42)
for y,val,n in [(1,vals[0],a['n']),(0,vals[1],b['n'])]:
 ax.text(2,y,f'{val:.1f}%',va='center',fontsize=37,fontweight='bold',color='#101c23')
ax.set_xlim(0,100);ax.set_ylim(-.6,1.6);ax.set_xticks([]);ax.set_yticks([])
for s in ax.spines.values():s.set_visible(False)
ax.text(0,1.35,'ORIGINAL SIMPLE DEVELOPMENT · 800 DECISIONS',fontsize=15,fontweight='bold')
ax.text(0,.35,'HARDER POLICY DEVELOPMENT · 576 DECISIONS',fontsize=15,fontweight='bold')
fig.text(.12,.86,'Easy tests hid a weakness',fontsize=40,fontweight='bold')
fig.text(.12,.79,'Same pretrained DeBERTa model. No travel fine-tuning yet.',fontsize=21,color='#b7c9ce')
fig.text(.12,.22,'Wrong package  /  Conflicting policies  /  Dates  /  Misleading instructions',fontsize=18,color='#f5b462')
fig.text(.12,.13,'Development evidence only. Synthetic, repeated templates; not human-validated.',fontsize=15,color='#b7c9ce')
fig.text(.12,.085,'This is not a final test or a head-to-head Jev result.  •  21 September 2026',fontsize=15,color='#b7c9ce')
fig.savefig(out/'development-reality-check.png');fig.savefig(out/'development-reality-check.svg');plt.close(fig)
(out/'development-reality-check.json').write_text(json.dumps({'original':a,'harder':b,'claim':'Pretrained model accuracy fell on more complex development inputs; comparison is between datasets, not models.','synthetic':True,'final_test':False},indent=2))
