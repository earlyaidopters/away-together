import copy
import json
import httpx
import pytest
from fastapi.testclient import TestClient
import travel_lab.serve as service
from travel_lab.vision import apply_visual_requirements,inspect_photos,TRAITS,photos_for

def photo_result(trait='steps', visible=True):
    answers={k:{'choice':'not_visible','probabilities':{'visible':.01,'not_visible':.98,'unclear':.01}} for k in TRAITS}
    answers[trait]={'choice':'visible' if visible else 'unclear','probabilities':{'visible':.98 if visible else .2,'not_visible':.01,'unclear':.01 if visible else .79}}
    return {'photos':[{'photo_id':'evidence','url':'/photos/madeira-path.png','answers':answers}]}

def test_stairs_change_match_to_decline_and_have_photo_source():
    base={'status':'match','reasons':[{'task':'budget','status':'match'}]}
    out=apply_visual_requirements(base,['avoid_steps'],photo_result())
    assert out['status']=='decline'
    assert out['reasons'][-1]['photo_ids']==['evidence']
    assert base['status']=='match' and len(base['reasons'])==1

@pytest.mark.parametrize('requirement',['pool','avoid_steps','ramp'])
def test_missing_or_failed_vision_is_never_a_match(requirement):
    for evidence in [{'photos':[],'status':'unavailable'},photo_result(visible=False)]:
        assert apply_visual_requirements({'status':'match','reasons':[]},[requirement],evidence)['status']=='review'

def test_visible_pool_cannot_override_paid_access_decline():
    base={'status':'decline','reasons':[{'task':'facility','status':'decline','text':'Pool costs extra'}]}
    out=apply_visual_requirements(base,['pool'],photo_result('pool'))
    assert out['status']=='decline' and out['reasons'][-1]['status']=='match'

def test_real_image_bytes_but_no_filename_or_caption_sent():
    photo=photos_for('Madeira, Portugal')[1]
    def respond(request):
        body=json.loads(request.content)
        assert body['images'][0].startswith('data:image/png;base64,')
        assert 'Madeira' not in body['state'] and photo['id'] not in request.content.decode()
        assert 'gold' not in body and 'expected' not in body
        return httpx.Response(200,json={'answers':photo_result()['photos'][0]['answers']})
    result=inspect_photos([photo],client=httpx.Client(transport=httpx.MockTransport(respond)))
    assert len(result['photos'][0]['sha256'])==64

def test_malformed_model_output_refused():
    client=httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200,json={'answers':{}})))
    with pytest.raises(ValueError):inspect_photos(photos_for('Madeira, Portugal')[:1],client=client)

class TextEngine:
    selection={'accept_threshold':.8}
    def predict(self,state,questions):
        return {'engine':'test','elapsed_ms':1,'answers':[{'id':q['id'],'choice':0,'probabilities':[.99,.005,.005]} for q in questions]}

def test_api_selects_only_requested_photo_and_preserves_text(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path);monkeypatch.setattr(service,'engine',TextEngine())
    def inspect(photos):
        assert [p['id'] for p in photos]==['madeira-path']
        return {'status':'completed','elapsed_ms':1,**photo_result()}
    monkeypatch.setattr(service,'inspect_photos',inspect)
    body={'offer_id':'o0','profiles':[{'id':'p0','budget':1600,'requirements':['refund'],'visual_requirements':['avoid_steps']}],'include_photos':True,'photo_ids':['madeira-path']}
    client=TestClient(service.app);r=client.post('/api/decide',json=body)
    assert r.status_code==200
    assert r.json()['text_profiles']['p0']['status']=='match'
    assert r.json()['profiles']['p0']['status']=='decline'
    body['photo_ids']=['kyoto-entrance']
    assert client.post('/api/decide',json=body).status_code==422

def test_vision_outage_returns_review_not_silent_text_success(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path);monkeypatch.setattr(service,'engine',TextEngine())
    def unavailable(photos):raise httpx.ConnectError('offline')
    monkeypatch.setattr(service,'inspect_photos',unavailable)
    body={'offer_id':'o0','include_photos':True,'profiles':[{'id':'p0','budget':1600,'requirements':[],'visual_requirements':['pool']}]}
    r=TestClient(service.app).post('/api/decide',json=body)
    assert r.status_code==200 and r.json()['vision']['status']=='unavailable'
    assert r.json()['profiles']['p0']['status']=='review'

def test_scan_reuses_one_live_photo_read_only_for_the_same_photos(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path);monkeypatch.setattr(service,'engine',TextEngine());monkeypatch.setattr(service,'vision_runs',{})
    calls=[]
    def inspect(photos):
        calls.append([p['id'] for p in photos]);return {'status':'completed','elapsed_ms':1,**photo_result()}
    monkeypatch.setattr(service,'inspect_photos',inspect)
    client=TestClient(service.app)
    read=client.post('/api/vision',json={'offer_id':'o0','photo_ids':['madeira-path']}).json()
    assert read['status']=='completed' and calls==[['madeira-path']]
    body={'offer_id':'o0','profiles':[{'id':'p0','budget':1600,'requirements':['refund'],'visual_requirements':['avoid_steps']}],'include_photos':True,'photo_ids':['madeira-path'],'vision_run_id':read['run_id']}
    r=client.post('/api/decide',json=body)
    assert r.status_code==200 and len(calls)==1
    assert r.json()['vision']['reused_from_run']==read['run_id']
    assert r.json()['profiles']['p0']['status']=='decline'
    body['photo_ids']=['madeira-overview','madeira-path']
    assert client.post('/api/decide',json=body).status_code==422
    body['vision_run_id']='expired'
    assert client.post('/api/decide',json=body).status_code==409

def test_photo_read_outage_is_reported_not_raised(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path)
    def unavailable(photos):raise httpx.ConnectError('offline')
    monkeypatch.setattr(service,'inspect_photos',unavailable)
    r=TestClient(service.app).post('/api/vision',json={'offer_id':'o0'})
    assert r.status_code==200 and r.json()['status']=='unavailable' and 'run_id' not in r.json()
