"""Generate fictional listing photos for the V3 vision evaluation with Nano Banana (gemini-3.1-flash-image).
Reads GOOGLE_API_KEY from ~/.env without printing it. Resumable; records prompt, model and hash per image."""
import base64, hashlib, json, sys, time
from pathlib import Path
import httpx

HERE = Path(__file__).parent
MODEL = 'gemini-3.1-flash-image'
STYLE = ('Photorealistic travel listing photograph of a FICTIONAL property: {scene}. Wide landscape composition, natural light, '
         'documentary property photography. No people, no text, no logos, no watermark, no collage.')

def api_key():
    for line in (Path.home() / '.env').read_text().splitlines():
        line = line.removeprefix('export ').strip()
        if line.startswith('GOOGLE_API_KEY='):
            return line.split('=', 1)[1].strip().strip('"\'')
    raise SystemExit('GOOGLE_API_KEY missing from ~/.env')

def main():
    key, specs = api_key(), json.loads((HERE / 'specs.json').read_text())
    manifest_path = HERE / 'generation-manifest.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    client = httpx.Client(timeout=180)
    for spec in specs:
        out = HERE / 'images' / f"{spec['id']}.png"
        if out.exists() and spec['id'] in manifest: continue
        prompt = STYLE.format(scene=spec['scene'])
        for attempt in range(3):
            r = client.post(f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent',
                            headers={'x-goog-api-key': key},
                            json={'contents': [{'parts': [{'text': prompt}]}],
                                  'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '3:2'}}})
            if r.status_code == 200:
                parts = r.json()['candidates'][0]['content']['parts']
                data = next((p['inlineData']['data'] for p in parts if 'inlineData' in p), None)
                if data: break
            print(spec['id'], 'attempt', attempt, r.status_code, r.text[:200].replace(key, '***'), flush=True); time.sleep(5)
        else:
            print(spec['id'], 'FAILED', flush=True); continue
        raw = base64.b64decode(data); out.write_bytes(raw)
        manifest[spec['id']] = {'model': MODEL, 'prompt': prompt, 'sha256': hashlib.sha256(raw).hexdigest(),
                                'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        manifest_path.write_text(json.dumps(manifest, indent=1)); print(spec['id'], 'ok', len(raw), flush=True)

if __name__ == '__main__':
    main()
