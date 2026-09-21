import json,time,uuid,threading
from pathlib import Path
from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from .catalogue import catalogue,verdict
from .active_model import active_selection,load_active_engine
from .reporting import active_report,active_errors
from .vision import inspect_photos,apply_visual_requirements,VISUAL_REQUIREMENTS
app=FastAPI(title='Away Together · local travel lab');engine=None;load_lock=threading.Lock()
class Profile(BaseModel):
    id:str
    budget:float=Field(ge=0,le=1000000)
    requirements:list[str]
    visual_requirements:list[str]=Field(default_factory=list,max_length=6)
class DecisionRequest(BaseModel):
    offer_id:str
    profiles:list[Profile]=Field(max_length=12)
    include_photos:bool=False
    photo_ids:list[str]|None=Field(default=None,max_length=8)
@app.middleware('http')
async def local_only(request:Request,call_next):
    origin=request.headers.get('origin')
    if request.method!='GET' and origin and origin not in ['http://localhost:8765','http://127.0.0.1:8765','http://localhost:5173']:
        from fastapi.responses import JSONResponse
        return JSONResponse({'error':'Origin not allowed'},status_code=403)
    response=await call_next(request);response.headers['Cache-Control']='no-store' if request.url.path.startswith('/api') else 'no-cache';return response
@app.get('/api/status')
def status():
    selection=engine.selection if engine is not None else active_selection();return {'ready':selection is not None,'engine_loaded':engine is not None,'selection':selection,'base_training_seconds':json.loads(Path('models/first-candidate-selection.json').read_text()).get('training_seconds') if Path('models/first-candidate-selection.json').exists() else None,'jev':'fresh post-freeze evaluation; see benchmark report','training_tail':Path('runs/train.log').read_text()[-1400:] if Path('runs/train.log').exists() else ''}
@app.get('/api/catalogue')
def catalog():return catalogue()
@app.post('/api/decide')
def decide(body:DecisionRequest):
    global engine
    c=catalogue();offer=next((o for o in c['offers'] if o['id']==body.offer_id),None)
    if not offer:raise HTTPException(404,'Unknown offer')
    if any(t not in ['refund','arrival','facility','activity'] for p in body.profiles for t in p.requirements):raise HTTPException(422,'Unknown requirement')
    if any(t not in VISUAL_REQUIREMENTS for p in body.profiles for t in p.visual_requirements):raise HTTPException(422,'Unknown visual requirement')
    available={p['id']:p for p in offer['photos']}
    if body.photo_ids is not None and (len(body.photo_ids)!=len(set(body.photo_ids)) or any(i not in available for i in body.photo_ids)):raise HTTPException(422,'Invalid photo selection')
    photos=offer['photos'] if body.photo_ids is None else [available[i] for i in body.photo_ids]
    try:
        started=time.perf_counter()
        with load_lock:
            if engine is None:
                engine=load_active_engine()
        state='\n'.join(f"[{cl['id']}] {cl['text']}" for cl in offer['clauses'])
        result=engine.predict(state,c['questions']);threshold=engine.selection['accept_threshold']
        text_profiles={p.id:verdict(p.model_dump(),offer,result['answers'],threshold) for p in body.profiles}
        vision={'status':'disabled','photos':[],'elapsed_ms':0}
        if body.include_photos and photos:
            try:vision=inspect_photos(photos)
            except Exception:
                vision={'status':'unavailable','photos':[],'elapsed_ms':0,'error':'Image model unavailable. Photo preferences require review; start the local vision service and retry.'}
        elif body.include_photos:vision['status']='no_photos'
        result['text_elapsed_ms']=result['elapsed_ms']
        decisions={p.id:apply_visual_requirements(text_profiles[p.id],p.visual_requirements,vision) for p in body.profiles}
        result.update({'run_id':str(uuid.uuid4()),'offer_id':offer['id'],'utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'mode':'live','profiles':decisions,'text_profiles':text_profiles,'vision':vision,'selected_photo_ids':[p['id'] for p in photos] if body.include_photos else [],'accept_threshold':threshold,'request_profiles':[p.model_dump(exclude_defaults=True) for p in body.profiles],'elapsed_ms':(time.perf_counter()-started)*1000})
        directory=Path('runs/demo');directory.mkdir(exist_ok=True,parents=True);(directory/f"{result['run_id']}.json").write_text(json.dumps(result,indent=2));return result
    except Exception as e:raise HTTPException(503,str(e))
@app.get('/api/runs')
def saved():return [json.loads(p.read_text()) for p in sorted(Path('runs/demo').glob('*.json'),key=lambda p:p.stat().st_mtime,reverse=True)[:20]]
@app.get('/api/report')
def report():
    return active_report()
@app.get('/api/errors')
def errors():
    return active_errors()
@app.get('/api/training')
def training():return [json.loads(x) for x in Path('runs/training.jsonl').read_text().splitlines()] if Path('runs/training.jsonl').exists() else []
app.mount('/reports',StaticFiles(directory='output/benchmarks'),name='reports')
if Path('app/dist').exists():app.mount('/',StaticFiles(directory='app/dist',html=True),name='app')
def main():
    import uvicorn
    import os
    uvicorn.run('travel_lab.serve:app',host=os.getenv('TRAVEL_HOST','127.0.0.1'),port=int(os.getenv('PORT','8765')))
if __name__=='__main__':main()
