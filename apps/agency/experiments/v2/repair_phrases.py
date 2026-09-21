"""Repair rejected writer batches from concrete facts, using a stronger writer.
Originals and their audit remain intact. New prose must pass the blind audit too.
"""
import json,time,hashlib,requests
from pathlib import Path
ROOT=Path('experiments/v2/data')
FACTS={
'refund':{
'meets':['Cancel before the published deadline: all amounts paid go back to the original card; nothing is retained.','An on-time cancellation returns the whole booking payment by bank transfer, with zero deductions.','Before the cancellation cutoff, the deposit AND remaining balance are returned in money, in full.'],
'violates':['Even before the deadline a EUR 30 administration fee is deducted from the refund.','Cancellation gives a travel voucher only; no cash or card reimbursement is offered.','The prepaid rate is non-refundable even if cancellation is early.','On cancellation, the deposit is retained and only the balance is returned.'],
'insufficient_evidence':['The booking can be cancelled, but whether money is returned and how much are not stated.','The listing calls the rate flexible; the refund terms are not provided.','Refund conditions appear in a separate document that is not included here.']},
'arrival':{
'meets':['Check-in operates 24 hours a day, including after midnight, with no prior notification or arrangement.','Overnight walk-in check-in is available automatically; guests do not need to request access in advance.','Guests can arrive after midnight without notice; the staffed desk will register them then.'],
'violates':['Check-in stops at 23:00, and guests arriving later cannot enter until morning.','After midnight guests must use a code that must be requested a day in advance.','The desk operates overnight but arrivals after midnight require advance approval.','The property refuses all check-ins between midnight and 06:00.'],
'insufficient_evidence':['Late arrivals are mentioned, but neither their hours nor any advance-arrangement requirements are given.','The arrival instructions are not provided in the listing.','The property is convenient for late flights, but check-in rules are unspecified.']},
'facility':{
'meets':['The property has its own swimming pool, open during these stay dates, and guests pay nothing extra to use it.','Use of the onsite swimming pool is included for everyone on this booking throughout the stay.','Resident guests swim free in the hotel courtyard pool; it is open for the booked week.'],
'violates':['The onsite swimming pool costs EUR 12 per use, in addition to the room price.','This accommodation has no pool; the only swimming pool is at a separate nearby leisure centre.','The hotel pool is closed for repairs for the entire booked stay.','The booked budget rate expressly excludes the onsite pool; a paid upgrade is needed.'],
'insufficient_evidence':['The property mentions a pool, but says nothing about fees or inclusion in the room rate.','The amenities describe a spa but do not say whether it includes a swimming pool.','A pool is shown in the brochure; its location and guest access conditions are not given.']},
'activity':{
'meets':['A hike accompanied by a guide is included in the quoted holiday price with no extra charge.','The package price pays for one guided countryside hike for each traveller.','Guests join the included guide-led trail walk without buying any extra ticket.'],
'violates':['The guided hike costs EUR 45 extra and is not part of the advertised package price.','Only self-guided walking maps are included; no hike with a guide is provided.','The included guided activity is a bus tour; guided hiking excursions are excluded.','No hikes are offered as part of this package.'],
'insufficient_evidence':['Outdoor excursions are mentioned, but the listing does not say whether a guided hike is included.','Hiking is possible in the area, but this package does not specify its activities or guide arrangements.','The itinerary will be supplied later; guided-hike inclusion and price are not stated.']}}
schema={'type':'object','properties':{'clauses':{'type':'array','items':{'type':'object','properties':{'text':{'type':'string'},'rationale':{'type':'string'}},'required':['text','rationale']}}},'required':['clauses']}
styles=['hotel FAQ','agent email','rate footnote','confirmation','supplier policy','fine print','support response','simple terms','amenities entry','amendment notice','operator statement','comparison table']
for path in sorted(ROOT.glob('phrases-*.json')):
 if 'repair' in path.name:continue
 audit_path=ROOT/'audit'/path.name
 if not audit_path.exists():continue
 audit=json.loads(audit_path.read_text())
 if audit['agreement']==audit['n']:continue
 out=path.with_name(path.stem+'-repair1.json')
 if out.exists():continue
 r=json.loads(path.read_text());facts=FACTS[r['task']][r['label']];items=[{'style':styles[i],'facts_to_preserve_exactly':facts[(i+r['batch'])%len(facts)]} for i in range(12)]
 prompt='''Rewrite each of the 12 factual policy descriptions below into its requested writing style. Preserve EVERY factual condition, negation, fee, location, time and missing-information qualification. Do not make the offer more attractive or change a negative into a positive. These facts are fixed. Use 18-60 words per excerpt. Do not add another policy topic. Return exactly 12 clauses in the same order, with text and a brief explanation of how you preserved the facts.\n'''+json.dumps(items)
 start=time.time();res=requests.post('http://127.0.0.1:11434/api/chat',json={'model':'gemma4:26b','messages':[{'role':'user','content':prompt}],'stream':False,'think':False,'format':schema,'options':{'temperature':.4,'num_predict':3500,'num_ctx':8192},'keep_alive':'30m'},timeout=600);res.raise_for_status();response=res.json();clauses=json.loads(response['message']['content'])['clauses'];assert len(clauses)==12
 record={**r,'clauses':clauses,'writer':'gemma4:26b','writer_model':response.get('model'),'repair_of':path.name,'fact_blueprints':items,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'seconds':time.time()-start,'status':'unverified stronger-writer repair; fresh blind audit required'}
 out.write_text(json.dumps(record,indent=2));print(out.name,round(record['seconds'],1),flush=True)
requests.post('http://127.0.0.1:11434/api/generate',json={'model':'gemma4:26b','keep_alive':0},timeout=120)
