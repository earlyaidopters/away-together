from .data import TASKS,CANDIDATES,LABELS
from .nli import HYPOTHESES
from .policy import per_person_total
from .vision import photos_for,VISUAL_REQUIREMENTS
PROFILES=[
('Maya','Wants room to change plans',1600,['refund'],'#ec886a'),('Leo','Lands after midnight',1700,['arrival'],'#6aa9be'),('Priya','Pool, every morning',1450,['facility'],'#b295c9'),('Noah','Here for the trails',1800,['activity'],'#759e77'),
('Sofia','Pool and peace of mind',1900,['facility','refund'],'#dcb267'),('Owen','Late flight, early swim',1800,['arrival','facility'],'#7ea0d4'),('Aisha','Flexible adventure',2100,['activity','refund'],'#d783a4'),('Ben','Keeping it under €1,000',1000,[],'#999a75'),
('Emma','Needs every box ticked',2400,['refund','arrival','facility','activity'],'#b9a385'),('Kai','Just a place to unwind',1350,[],'#77b7ab'),('Zara','Trails after a late flight',1750,['arrival','activity'],'#aaa0ca'),('Hugo','Swim, hike, repeat',1550,['facility','activity'],'#ce8b67')]

def catalogue():
    profiles=[{'id':f'p{i}','name':p[0],'subtitle':p[1],'budget':p[2],'requirements':p[3],'color':p[4],'selected':i<4} for i,p in enumerate(PROFILES)]
    names=['Atlantic hideaway','The flexible escape','Poolside promise','The midnight arrival','Trail week','A little mystery','The voucher catch','The all-in escape']
    patterns=[[0,0,0,1],[0,1,0,0],[1,0,0,2],[0,1,1,0],[1,0,2,0],[2,2,2,2],[1,0,0,0],[0,0,0,0]]
    prices=[1290,1420,990,1140,1190,890,1090,1890]
    offers=[]
    for i in range(40):
        pattern=patterns[i%8]; clauses=[]
        for n,(task,spec) in enumerate(TASKS.items()):
            phrase=spec[['positive','negative','unknown'][pattern[n]]][(i//8)%3]
            clauses.append({'id':f'C{n+1}','task':task,'text':phrase})
        offers.append({'id':f'o{i}','name':names[i%8]+(f' · {i//8+1}' if i>=8 else ''),'destination':['Madeira, Portugal','Kyoto, Japan','Reykjavik, Iceland'][i%3],'nights':7,'price':prices[i%8]+(i//8)*45,'currency':'EUR','price_basis':'per person, taxes included','image':['/madeira.png','/kyoto.png','/iceland.png'][i%3],'clauses':clauses,'synthetic':True})
    for profile in profiles:
        profile['visual_requirements'] = {'p0':['avoid_steps'],'p2':['pool'],'p3':['mountains'],'p9':['garden']}.get(profile['id'],[])
    for offer in offers:
        offer['photos'] = photos_for(offer['destination'])
    return {'profiles':profiles,'offers':offers,'visual_requirements':VISUAL_REQUIREMENTS,'questions':[{'id':task,'question':spec['question'],'candidates':HYPOTHESES[task],'labels':LABELS} for task,spec in TASKS.items()]}

def verdict(profile,offer,answers,threshold):
    reasons=[]
    if offer['currency']!='EUR':return {'status':'review','reasons':['Currency conversion is unavailable.']}
    total=per_person_total(offer['price'],currency=offer['currency'])
    if total>profile['budget']:reasons.append({'task':'budget','status':'decline','text':f"€{offer['price']:,.0f} exceeds the €{profile['budget']:,.0f} budget.",'source':'arithmetic'})
    else:reasons.append({'task':'budget','status':'match','text':f"€{offer['price']:,.0f} fits the €{profile['budget']:,.0f} budget.",'source':'arithmetic'})
    for task in profile['requirements']:
        a=next(x for x in answers if x['id']==task);choice=a['choice'];confidence=a['probabilities'][choice]
        status='decline' if choice==1 else ('review' if choice==2 or confidence<threshold else 'match')
        clause=next(x for x in offer['clauses'] if x['task']==task)
        reasons.append({'task':task,'status':status,'text':clause['text'],'clause_id':clause['id'],'confidence':confidence,'source':'model decision; source field retrieved from structured offer'})
    status='decline' if any(x['status']=='decline' for x in reasons) else ('review' if any(x['status']=='review' for x in reasons) else 'match')
    return {'status':status,'reasons':reasons}
