from pathlib import Path
import json,html
from filming_source import read_scenes,timing
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
P=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleGreen',fontName='Helvetica-Bold',fontSize=29,leading=34,textColor=HexColor('#203d36'),spaceAfter=20))
styles.add(ParagraphStyle(name='LabelGreen',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=HexColor('#2c654e'),spaceBefore=12,spaceAfter=5))
styles.add(ParagraphStyle(name='Spoken',fontName='Helvetica',fontSize=12,leading=18,spaceAfter=9))
styles.add(ParagraphStyle(name='Notes',fontName='Helvetica',fontSize=9,leading=13,textColor=HexColor('#52645e'),spaceAfter=6))
def clean(t):return html.escape(t).replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('→',' / ').replace('≤','&lt;=').replace('–','-').replace('—','-')
def para(t,style='Spoken'):return Paragraph(clean(t),styles[style])
scenes=read_scenes();pace=timing(scenes)
final=json.loads((P/'output/benchmarks/frozen-v2-summary.json').read_text())
assert all(m['status']!='pending' for lane in final['public'].values() for m in lane.values())
flow=[para('Can Astra Build Its Own Jev?','TitleGreen'),para('FILMING GUIDE / 21 SEPTEMBER 2026','LabelGreen'),para('The photo-aware local agency, the frozen text challenger, and the measured results.'),Spacer(1,15)]
img=P/'output/benchmarks/frozen-v2-travel.png'
flow.append(Image(str(img),width=511,height=287.4))
flow += [Spacer(1,16),para('V2 was not promoted.','TitleGreen'),para('The fresh synthetic travel result was 95.28% local versus 98.61% Jev. The app still serves historical V1. Reference repairs and two writer-assisted adjudications are disclosed; no human validation.','Notes'),para(f'{pace["words"]:,} spoken words. {pace["spoken_minutes_at_155_wpm"]:.1f} minutes at 155 WPM, with a planned {pace["planned_minutes"]:.1f}-minute runtime including visual holds. Script-only narration source is supplied; no TTS requested.','Notes'),PageBreak()]
for name,start,end,picture,copy,say,edit,source,rehook in scenes:
 flow+=[para(f'{start} - {end} / {name}','TitleGreen')]
 for label,body,style in [('PICTURE',picture,'Notes'),('SAY',say,'Spoken'),('ON-SCREEN COPY',copy,'Spoken'),('EDITING NOTE',edit,'Notes'),('SOURCE / TRUTH CARD',source,'Notes'),('RE-HOOK',rehook,'Spoken')]:
  if body:
   flow.append(para(label,'LabelGreen'))
   if label in ['SAY','RE-HOOK']:
    flow.append(Paragraph('<br/>'.join(clean(line) for line in body.splitlines()),styles[style]))
   else:flow.append(para(body,style))
 flow.append(PageBreak())
flow+= [para('Before the take','TitleGreen'),para('Start the OpenJev vision service on localhost:8081 and the agency on localhost:8765. Reset with R. Select Four friends. Run Atlantic hideaway fresh. P pauses or resumes the presentation. Escape closes details. Warm both models before recording; cold load is separate from warm request timing.'),para('The charts show saved benchmark results. The agency serves V1, while the final challenger result is V2. Photos, travellers and offers are fictional. Source-clause linkage is structured application logic.'),para('Truth boundaries','LabelGreen'),para('Final references are synthetic and agent-reviewed, with 52 document repairs and two non-unanimous writer-assisted adjudications. All 360 scenarios remain. No human validation. The public workflow lane measures teacher agreement; upstream exposure may apply. Thirty-five workflow decisions failed the frozen context limit and remain in the denominator. Official TypeSafe benchmark scores were not reproduced.','Notes'),para('Measured agency timing','LabelGreen'),para('Active V1: cold first HTTP request 10.1 seconds including loading. Three fresh forty-offer scans took 4.0, 4.2 and 4.5 seconds. Warm HTTP median 105 ms, 121 unique fresh requests, zero failures. These are text-only historical timings, separate from V2 model-only latency. The photo-aware 40-offer integration scan took 40.7 seconds in its recorded run.','Notes'),para('Companion resource','LabelGreen'),para('Show the verified local bundle, including both checkpoints and original audit evidence. Add a public download link only once separately arranged. The OpenJev image branch ran locally; its pinned model is downloaded separately. The earlier text-only diffusion comparison was not executed. No public upload, deployment or messaging is implied.','Notes')]
def footer(c,d):
 c.setFillColor(HexColor('#72816a'));c.setFont('Helvetica',8);c.drawString(42,27,'AWAY TOGETHER / PRIVATE PRODUCTION GUIDE');c.drawRightString(553,27,str(d.page))
SimpleDocTemplate(str(P/'output/pdf/FILMING-GUIDE.pdf'),pagesize=(595,842),leftMargin=42,rightMargin=42,topMargin=40,bottomMargin=42).build(flow,onFirstPage=footer,onLaterPages=footer)
print('PDF created')
