"""One blind second opinion for two unresolved reference-auditor errors.

Qwen is also the original writer, so this is NOT independent human validation.
The exact documents remain unchanged. No expected labels enter the request.
"""
import json
import sys
from pathlib import Path
import requests
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.v2.generate_final import WRITER, document_digest, verify_audit_source, unload

ROOT = Path('experiments/v2/final/round1-deeper-fp16/reference-repair-1')

def main():
    expected_ids = {'round1-deeper-fp16-0140', 'round1-deeper-fp16-0235'}
    remaining = json.loads((ROOT/'remaining-disagreements.json').read_text())
    assert {d['id'] for d in remaining} == expected_ids
    ledger = json.loads((ROOT/'repair-ledger.json').read_text())
    docs = {d['id']: {'id': d['id'], 'text': d['after']} for d in ledger['decisions']}
    method = json.loads((ROOT/'audit-method.json').read_text())
    destination = ROOT/'blind-second-opinion'; destination.mkdir(exist_ok=True)
    protocol = {'model': WRITER, 'scope': 'Two fixed remaining disagreements only; documents unchanged; no retries based on answer.', 'independence_limit': 'This model family also wrote the original documents. Second opinion is blind to specs and prior audits, but is not independent of the writer or human validation.', 'prompt_prefix': method['prompt_prefix'], 'options': {'temperature': 0, 'num_predict': 6500, 'num_ctx': 16384}}
    (destination/'protocol.json').write_text(json.dumps(protocol, indent=2))
    for ident in sorted(expected_ids):
        path = destination/(ident+'.json'); batch = [docs[ident]]
        if path.exists(): result = json.loads(path.read_text())
        else:
            response = requests.post('http://127.0.0.1:11434/api/chat', json={'model': WRITER, 'messages': [{'role': 'user', 'content': method['prompt_prefix']+json.dumps(batch)}], 'stream': False, 'think': False, 'format': method['schema'], 'keep_alive': '30m', 'options': protocol['options']}, timeout=900)
            response.raise_for_status()
            result = json.loads(response.json()['message']['content'])
            result['documents_sha256'] = document_digest(batch)
            path.write_text(json.dumps(result, indent=2))
        verify_audit_source(result, batch)
        print('second-opinion', ident, flush=True)
    unload(WRITER)

if __name__ == '__main__': main()
