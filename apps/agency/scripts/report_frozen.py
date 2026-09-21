"""Build final-candidate receipts and charts without changing any selection."""
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.v2.freeze_candidate import verify
from experiments.v2.paired_report import compare
from travel_lab.metrics import summarise

P = Path(__file__).resolve().parents[1]

def read(path): return json.loads(path.read_text())
def rows(path): return [json.loads(x) for x in path.read_text().splitlines()]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    freeze_path = P/'experiments/v2/freezes/deeper-fp16-20260921.json'
    freeze = read(freeze_path); verify(freeze)
    run = P/'experiments/v2/runs/round1-deeper-fp16'
    corpus = P/'experiments/v2/final/round1-deeper-fp16'
    manifest = read(run/'data-manifest.json')
    assert sha(corpus/'test.jsonl') == manifest['sha256']
    assert sha(corpus/'reference-resolution.json') == manifest['reference_resolution_sha256']
    local = rows(run/'deberta-travel-v2-travel-fresh.jsonl')
    remote = rows(run/'jev-travel-fresh.jsonl')
    report = compare(local, remote)
    assert report == read(run/'paired-report.json')
    evidence = {str(path.relative_to(P)): sha(path) for path in [freeze_path, corpus/'test.jsonl', corpus/'reference-resolution.json', run/'paired-report.json', run/'deberta-travel-v2-travel-fresh.jsonl', run/'jev-travel-fresh.jsonl']}
    public = {}; public_root = P/'experiments/v2/runs/public-deeper-fp16'
    assert read(public_root/'public-protocol.json')['freeze'] == freeze
    for lane, count in [('typed-independent', 400), ('btzsc-independent', 300)]:
        public[lane] = {}
        for engine, key in [('deberta-travel-v2', 'local'), ('jev', 'jev')]:
            raw = public_root/f'{engine}-{lane}.jsonl'
            metrics = public_root/f'{engine}-{lane}-metrics.json'
            if not metrics.exists():
                public[lane][key] = {'status': 'pending'}; continue
            records = rows(raw)
            assert len(records) == count == len({r['id'] for r in records})
            calculated = summarise(records)
            assert calculated == read(metrics)
            public[lane][key] = calculated
            evidence[str(raw.relative_to(P))] = sha(raw)
    miss_rows = []
    documents = {r['id']: r for r in rows(corpus/'test.jsonl')}
    other = {r['id']: r for r in remote}
    for item in local:
        if any(d['pred'] != d['gold'] for d in item['decisions']):
            miss_rows.append({'id': item['id'], 'state': documents[item['id']]['state'], 'local': item['decisions'], 'jev': other[item['id']]['decisions']})
        if len(miss_rows) == 5: break
    summary = {'created_utc': datetime.now(timezone.utc).isoformat(), 'model': 'Frozen DeBERTa travel challenger',
               'active_in_app': False, 'promotion_status': 'Not qualified; not promoted',
               'replication_status': 'Conditional replication not started because the first superiority gate failed.',
               'travel': report, 'public': public, 'misses': miss_rows, 'source_hashes': evidence,
               'reference_scope': read(corpus/'reference-resolution.json')['reference_scope'],
               'public_scope': 'Independent normalized candidate-choice references, not the official native typed harness. Upstream exposure may apply. Failed decisions stay in denominators.',
               'latency_scope': 'Warm local tokenization and synchronized inference versus remote request wall time. Loading, HTTP app calls and browser rendering are separate.',
               'risk_scope': 'Zero observed errors among 393 accepted decisions does not establish zero population risk. Synthetic, model-assisted references lack human validation.'}
    assert report['round_qualifies'] is False and not (P/'models/active-model.json').exists()
    out = P/'output/benchmarks'; out.mkdir(exist_ok=True)
    (out/'frozen-v2-summary.json').write_text(json.dumps(summary, indent=2))
    plt.rcParams.update({'font.family': 'sans-serif', 'figure.facecolor': '#f3f5f1', 'axes.facecolor': '#f3f5f1', 'text.color': '#203d36', 'axes.spines.top': False, 'axes.spines.right': False, 'axes.spines.left': False})
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    fig.subplots_adjust(left=.23, right=.91, top=.74, bottom=.28)
    vals = [100*report[e]['accuracy'] for e in ['local', 'jev']]
    ax.barh([1, 0], vals, color=['#2c654e', '#d6a956'], height=.48)
    ax.set_yticks([1, 0], ['Frozen local model', 'Jev · fresh API'], fontsize=20)
    ax.set_xlim(0, 110); ax.set_xticks([0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'], fontsize=15)
    ax.grid(axis='x', alpha=.15); ax.set_axisbelow(True)
    for y, value in zip([1, 0], vals): ax.text(value+1, y, f'{value:.2f}%', va='center', fontsize=25, fontweight='bold')
    fig.text(.08, .91, 'The stronger model still lost.', fontsize=36, fontweight='bold')
    fig.text(.08, .84, '360 fresh scenarios · 1,440 policy decisions per engine · zero request failures', fontsize=18)
    lo, hi = report['paired_accuracy_difference_ci95']
    fig.text(.08, .17, f'Local minus Jev: {100*report["paired_accuracy_difference"]:.2f} percentage points  |  95% interval: {100*lo:.2f} to {100*hi:.2f}', fontsize=19)
    fig.text(.08, .115, 'Synthetic, agent-reviewed references. Two writer-assisted adjudications; no human validation.', fontsize=14)
    fig.text(.08, .065, 'Source: round1-deeper-fp16 paired report · frozen before generation · all prespecified cases retained', fontsize=12)
    for suffix in ['png', 'svg']: fig.savefig(out/f'frozen-v2-travel.{suffix}')
    plt.close(fig)
    md = ['# Frozen V2 challenger: final evidence', '',
          f'Local agreement **{report["local"]["accuracy"]:.2%}** versus **{report["jev"]["accuracy"]:.2%}** for Jev. The superiority gate failed; the challenger was not promoted.', '',
          f'360 scenarios, 1,440 decisions per engine, no failed decisions. Paired accuracy difference {100*report["paired_accuracy_difference"]:.2f} percentage points; scenario-bootstrap 95% interval [{100*lo:.2f}, {100*hi:.2f}].', '',
          f'Local macro F1 {report["local"]["macro_f1_by_field"]:.4f}; 393 accepted decisions, zero observed accepted errors; correct-meets recall {report["gold_meets_acceptance_recall"]:.2%}. Quality and coverage floors passed. Zero observed errors does not establish zero population risk.', '',
          '## Deployment and replication', '', summary['replication_status'], 'The localhost agency continues to serve the historical V1 model, whose earlier travel accuracy was 66.5%. Do not describe the V2 result or V2 timing as active agency behavior.', '',
          '## Public lanes, reported separately', '', '| Lane | Engine | Agreement | Macro F1 | Failed decisions | Median ms |', '|---|---|---:|---:|---:|---:|']
    for lane, engines in public.items():
        for engine, metrics in engines.items():
            if metrics['status'] == 'pending': md.append(f'| {lane} | {engine} | Pending | | | |')
            else: md.append(f'| {lane} | {engine} | {metrics["accuracy"]:.2%} | {metrics["macro_f1_by_field"]:.4f} | {metrics["failed_decisions"]}/{metrics["decisions"]} | {metrics["p50_ms"]:.1f} |')
    md += ['', summary['public_scope'], '', '## Speed boundaries', '',
           f'Fresh travel median: local {report["local"]["p50_ms"]:.1f} ms; Jev {report["jev"]["p50_ms"]:.1f} ms. Local p95 {report["local"]["p95_ms"]:.1f} ms; Jev {report["jev"]["p95_ms"]:.1f} ms.', summary['latency_scope'], '',
           'The earlier development precision experiment used alternating independently reloaded FP32/FP16 blocks. It found zero changed choices over 2,176 development decisions and roughly halved warm model latency. That optimization was selected before final generation. See experiments/v2/runs/deeper-precision-benchmark/report.json.', '',
           '## Reference provenance', '', summary['reference_scope'], 'All original drafts and audits, 52 factual/wording repairs, seven unchanged re-audits and two non-unanimous adjudications are preserved. Prespecified labels never changed; all 360 cases remained. Qwen was the writer and the two-case second-opinion model, so those judgments are not independent of the writer. No human validation.', '',
           '## Reproduction', '', 'The source hashes are in frozen-v2-summary.json. The complete resource includes the frozen challenger even though it was not promoted. Final and public results did not tune weights, thresholds, input policy or the seed. Repeat scoring incurs Jev API calls; use preserved raw receipts for report reproduction.', '']
    (out/'FROZEN-V2-RESULTS.md').write_text('\n'.join(md))
    print(json.dumps({'travel_report_verified': True, 'public_complete': all(v['status'] != 'pending' for lane in public.values() for v in lane.values()), 'output': str(out/'FROZEN-V2-RESULTS.md')}))

if __name__ == '__main__': main()
