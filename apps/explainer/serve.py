"""Loopback-only filming site; forwards only the known local demo endpoint."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_POST(self):
        if self.path!='/api/decide':self.send_error(404);return
        if self.headers.get('Origin') not in [None,'http://localhost:8770','http://127.0.0.1:8770']:self.send_error(403);return
        size=int(self.headers.get('Content-Length','0'))
        if size<1 or size>20000:self.send_error(413);return
        body=self.rfile.read(size)
        try:
            request=Request('http://127.0.0.1:8765/api/decide',data=body,headers={'Content-Type':'application/json'},method='POST')
            with urlopen(request,timeout=300) as r:payload=r.read();status=r.status
        except HTTPError as e:payload=e.read();status=e.code
        except Exception:payload=json.dumps({'error':'Start the local agency on 8765 and vision on 8081.'}).encode();status=503
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(payload)
if __name__=='__main__':
    print('Explainer: http://localhost:8770',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8770),Handler).serve_forever()
