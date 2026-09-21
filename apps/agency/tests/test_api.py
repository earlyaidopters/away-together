from fastapi.testclient import TestClient
import travel_lab.serve as service

class FakeEngine:
    selection={'accept_threshold':.8}
    def predict(self,state,questions):
        assert 'oracle' not in state
        return {'engine':'TEST ONLY','elapsed_ms':1,'answers':[{'id':q['id'],'choice':0,'probabilities':[.9,.05,.05]} for q in questions]}
def test_api_receipt_and_origin_guard(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path);monkeypatch.setattr(service,'engine',FakeEngine());client=TestClient(service.app)
    body={'offer_id':'o0','profiles':[{'id':'p0','budget':1600,'requirements':['refund']}]}
    r=client.post('/api/decide',json=body);assert r.status_code==200
    data=r.json();assert data['request_profiles']==body['profiles'];assert data['profiles']['p0']['status']=='match'
    assert client.post('/api/decide',json=body,headers={'Origin':'https://unrelated.example'}).status_code==403
    body['profiles'][0]['requirements']=['invented'];assert client.post('/api/decide',json=body).status_code==422
