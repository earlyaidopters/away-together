"""Derive scene and narration exports from the canonical editable Markdown."""
import argparse
import hashlib
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
SOURCE = P/'production/FILMING-GUIDE.md'
FIELDS = ['Picture', 'Say', 'On-screen copy', 'Editing note', 'Source or truth card']

def read_scenes():
    text = SOURCE.read_text()
    result = []
    for title, body in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', text, re.M|re.S):
        match = re.fullmatch(r'(.+) \((\d+:\d{2})-(\d+:\d{2})\)', title)
        if not match: raise ValueError('Scene needs exact start/end times: '+title)
        blocks = re.findall(r'^\*\*([^\n]+?):\*\*\s*\n(.*?)(?=^\*\*|\Z)', body, re.M|re.S)
        values = {key: value.strip() for key, value in blocks}
        if len(values) != len(blocks): raise ValueError('Duplicate scene label')
        if any(not values.get(key) for key in FIELDS): raise ValueError('Missing guide field: '+title)
        name, start, end = match.groups()
        result.append([name, start, end, values['Picture'], values['On-screen copy'], values['Say'], values['Editing note'], values['Source or truth card'], values.get('Re-hook', '')])
    if not result: raise ValueError('No scenes found')
    return result

def seconds(value):
    minutes, seconds = map(int, value.split(':')); return minutes*60+seconds

def timing(scenes):
    records = []; end = 0
    for name, start, stop, picture, copy, say, edit, source, rehook in scenes:
        assert seconds(start) == end, 'Scene timing gap or overlap'
        end = seconds(stop); duration = end-seconds(start)
        words = len((say+' '+rehook).split())
        if duration <= 0 or words/duration*60 > 180: raise ValueError('Invalid or rushed scene: '+name)
        records.append({'scene': name, 'words': words, 'planned_seconds': duration, 'planned_wpm': words/duration*60, 'spoken_seconds_at_155_wpm': words/155*60, 'visual_hold_seconds_at_155_wpm': duration-words/155*60})
    count = sum(r['words'] for r in records)
    return {'words': count, 'spoken_minutes_at_155_wpm': count/155, 'planned_minutes': end/60,
            'holds_minutes': end/60-count/155, 'tts_generated': False, 'scenes': records,
            'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'spoken_labels': ['Say', 'Re-hook']}

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('stage', choices=['scenes', 'narration']); args = parser.parse_args()
    scenes = read_scenes(); report = timing(scenes)
    if args.stage == 'scenes':
        (P/'production/scenes.json').write_text(json.dumps(scenes, indent=2))
        lines = ['# Final visual storyboard', '', 'Derived from the canonical filming guide. Each scene has its own evidence surface.', '']
        for name, start, end, picture, copy, say, edit, source, rehook in scenes:
            lines += [f'## {start}-{end}: {name}', '', picture, '', f'On-screen: {copy}', '', f'Editing: {edit}', '', f'Evidence: {source}', '']
        (P/'production/VISUAL-STORYBOARD.md').write_text('\n'.join(lines))
    else:
        pdf = P/'output/pdf/FILMING-GUIDE.pdf'
        if not pdf.exists() or pdf.stat().st_mtime < SOURCE.stat().st_mtime:
            raise ValueError('Render the current PDF before exporting narration')
        directory = P/'output/audio'; directory.mkdir(exist_ok=True)
        narration = '\n\n'.join(block for scene in scenes for block in [scene[5], scene[8]] if block)+'\n'
        assert len(narration.split()) == report['words']
        (directory/'narration-source.txt').write_text(narration)
        report['narration_sha256'] = hashlib.sha256(narration.encode()).hexdigest()
        (directory/'timing-report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'stage': args.stage, 'scenes': len(scenes), 'words': report['words'], 'planned_minutes': report['planned_minutes'], 'spoken_minutes_at_155_wpm': report['spoken_minutes_at_155_wpm']}))

if __name__ == '__main__': main()
