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
styles.add(ParagraphStyle(name='HookLines',fontName='Helvetica',fontSize=12,leading=15,spaceAfter=4))
styles.add(ParagraphStyle(name='Notes',fontName='Helvetica',fontSize=9,leading=13,textColor=HexColor('#52645e'),spaceAfter=6))
def clean(t):return html.escape(t).replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('→',' / ').replace('≤','&lt;=').replace('–','-').replace('—','-')
def para(t,style='Spoken'):return Paragraph(clean(t),styles[style])
scenes=read_scenes();pace=timing(scenes)
final=json.loads((P/'output/benchmarks/frozen-v2-summary.json').read_text())
assert all(m['status']!='pending' for lane in final['public'].values() for m in lane.values())
flow=[para('Can Astra Build Its Own Jev?','TitleGreen'),para('FILMING GUIDE / 21 SEPTEMBER 2026','LabelGreen'),para('The photo-aware local agency, the frozen text challenger, and the measured results.'),Spacer(1,15)]
img=P/'output/benchmarks/frozen-v2-travel.png'
flow.append(Image(str(img),width=511,height=287.4))
flow += [Spacer(1,16),para('V2 runs the demo. It did not beat Jev.','TitleGreen'),para('Same 360 fresh synthetic travel scenarios: first model 60.28%, V2 95.28%, Jev 98.61%. The app runs V2 under the app rule (quality gates passed, clearly beats V1), not as a Jev win. Reference repairs and two writer-assisted adjudications are disclosed; no human validation.','Notes'),para(f'{pace["words"]:,} spoken words. {pace["spoken_minutes_at_155_wpm"]:.1f} minutes at 155 WPM, with a planned {pace["planned_minutes"]:.1f}-minute runtime including visual holds. Script-only narration source and a separate audio guide are supplied.','Notes'),PageBreak()]
import re
common_edit=max(set(e for *_,e,_,_ in scenes),key=lambda e:sum(x[6]==e for x in scenes))
flow+=[para('How to use this guide','TitleGreen'),para('Each scene page shows what is on screen, then exactly what to say. Screenshots come from the live filming site at 1440 x 900.'),para('EDITING NOTE FOR EVERY SCENE','LabelGreen'),para(common_edit,'Notes'),PageBreak()]
for name,start,end,picture,copy,say,edit,source,rehook in scenes:
 head=[para(f'{start} - {end} / {name}','TitleGreen')]
 found=re.search(r'Scene `#([\w-]+)`',picture);shot=P/'output/qa/scene-shots'/f'{found.group(1)}.jpg' if found else None
 if shot and shot.exists():
  # What is on screen for this beat, captured at 1440x900 from the live filming site.
  head+=[Image(str(shot),width=400,height=250),para(f'On screen: localhost:8770/#{found.group(1)}','Notes')]
 # Read on camera line by line: one sentence per line, words unchanged.
 lines=[x for x in re.split(r'(?<=[.?!])\s+',' '.join(say.split())) if x]
 head+=[para('SAY','LabelGreen')]+[Paragraph(clean(line),styles['HookLines']) for line in lines]
 flow.append(KeepTogether(head))
 for label,body,style in [('PICTURE',picture,'Notes'),('ON-SCREEN COPY',copy,'Spoken'),('EDITING NOTE',edit if edit!=common_edit else '','Notes'),('SOURCE / TRUTH CARD',source,'Notes'),('RE-HOOK',rehook,'Spoken')]:
  if body:
   flow.append(para(label,'LabelGreen'))
   if label in ['SAY','RE-HOOK']:
    flow.append(Paragraph('<br/>'.join(clean(line) for line in body.splitlines()),styles[style]))
   else:flow.append(para(body,style))
 flow.append(PageBreak())
flow+= [para('Before the take','TitleGreen'),para('Start the OpenJev vision service on localhost:8081 and the agency on localhost:8765. Reset with R. Select Four friends. Choose The flexible escape · 2 (holiday 10 of 40) and run it fresh. P pauses or resumes the presentation. Escape closes details. The agency warms both models when it starts; wait about 20 seconds after launch before the first take.'),para('The charts show saved benchmark results. The agency serves V2; the results chart compares it with the first model and Jev on the same test. Photos, travellers and offers are fictional. Source-clause linkage is structured application logic.'),para('Truth boundaries','LabelGreen'),para('Final references are synthetic and agent-reviewed, with 52 document repairs and two non-unanimous writer-assisted adjudications. All 360 scenarios remain. No human validation. The public workflow lane measures teacher agreement; upstream exposure may apply. Thirty-five workflow decisions failed the frozen context limit and remain in the denominator. Official TypeSafe benchmark scores were not reproduced.','Notes'),para('Measured agency timing','LabelGreen'),para('Active V1: cold first HTTP request 10.1 seconds including loading. Three fresh forty-offer scans took 4.0, 4.2 and 4.5 seconds. Warm HTTP median 105 ms, 121 unique fresh requests, zero failures. These are text-only historical timings, separate from V2 model-only latency. The photo-aware 40-offer integration scan took 40.7 seconds in its recorded run.','Notes'),para('Companion resource','LabelGreen'),para('Show the verified local bundle, including both checkpoints and original audit evidence. Add a public download link only once separately arranged. The OpenJev image branch ran locally; its pinned model is downloaded separately. The earlier text-only diffusion comparison was not executed. No public upload, deployment or messaging is implied.','Notes')]
def footer(c,d):
 c.setFillColor(HexColor('#72816a'));c.setFont('Helvetica',8);c.drawString(42,27,'AWAY TOGETHER / PRIVATE PRODUCTION GUIDE');c.drawRightString(553,27,str(d.page))
SimpleDocTemplate(str(P/'output/pdf/FILMING-GUIDE.pdf'),pagesize=(595,842),leftMargin=42,rightMargin=42,topMargin=40,bottomMargin=42).build(flow,onFirstPage=footer,onLaterPages=footer)
print('PDF created')
