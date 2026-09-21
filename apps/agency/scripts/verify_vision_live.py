"""Live integration smoke checks, not an image-quality benchmark."""
import json
from pathlib import Path
import time
import httpx

ROOT=Path(__file__).resolve().parents[1]
def main():
    out=ROOT/'output/qa/vision-full-scan.json'
    with httpx.Client(base_url='http://127.0.0.1:8765',timeout=300) as client:
        catalogue=client.get('/api/catalogue').json()
        profiles=[{key:p[key] for key in ['id','budget','requirements','visual_requirements']} for p in catalogue['profiles']]
        rows=[];start=time.perf_counter()
        for offer in catalogue['offers']:
            response=client.post('/api/decide',json={'offer_id':offer['id'],'profiles':profiles,'include_photos':True})
            response.raise_for_status();r=response.json()
            assert r['vision']['status']=='completed'
            assert {p['photo_id'] for p in r['vision']['photos']}=={p['id'] for p in offer['photos']}
            assert set(r['profiles'])=={p['id'] for p in profiles}
            rows.append({'offer_id':offer['id'],'run_id':r['run_id'],'elapsed_ms':r['elapsed_ms'],'vision_ms':r['vision']['elapsed_ms'],'statuses':{key:v['status'] for key,v in r['profiles'].items()}})
            out.write_text(json.dumps({'status':'running','rows':rows},indent=2))
            print(offer['id'],round(r['elapsed_ms']),flush=True)
        assert len({r['run_id'] for r in rows})==40
        out.write_text(json.dumps({'status':'passed','scope':'40 live integration requests with three fictional photos each, not a general accuracy test. OpenJev may reuse prompt prefills; each request executes decision inference.','client_wall_seconds':time.perf_counter()-start,'rows':rows},indent=2))
        print('40 fresh photo-aware requests passed')
if __name__=='__main__':main()
