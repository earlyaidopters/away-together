"""Seal the documented repaired corpus, with truthful per-case audit provenance.

Original generator/source, all raw audits, all latent labels and frozen model
remain unchanged. This supplemental sealer records two non-unanimous reference
adjudications explicitly instead of representing them as unanimous Gemma audits.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.v2.freeze_candidate import verify, sha
from experiments.v2.generate_final import document_digest, verify_audit_source, WRITER, AUDITOR
from travel_lab.data import TASKS, LABELS
from travel_lab.nli import HYPOTHESES

ROOT = Path('experiments/v2/final/round1-deeper-fp16')
FREEZE = Path('experiments/v2/freezes/deeper-fp16-20260921.json')

def read(path): return json.loads(path.read_text())

def main():
    freeze = read(FREEZE); verify(freeze)
    path = ROOT/'test.jsonl'; manifest_path = ROOT/'test.manifest.json'
    if path.exists() or manifest_path.exists():
        manifest = read(manifest_path)
        assert sha(path) == manifest['sha256']
        assert sha(ROOT/'reference-resolution.json') == manifest['reference_resolution_sha256']
        print('Existing sealed corpus verified; no changes made.'); return
    repair = ROOT/'reference-repair-1'; original = repair/'originals'
    for name, digest in read(repair/'original-hashes.json').items():
        assert sha(original/name) == digest, ('Archived source changed', name)
    specs = read(ROOT/'reference-specs.json'); config = read(ROOT/'generation-config.json')
    assert sha(ROOT/'reference-specs.json') == sha(original/'reference-specs.json')
    assert config == read(original/'generation-config.json')
    assert config['generator_sha256'] == sha('experiments/v2/generate_final.py')
    assert config['freeze_sha256'] == sha(FREEZE)
    ledger = read(repair/'repair-ledger.json')
    decisions = {d['id']: d for d in ledger['decisions']}
    assert len(decisions) == 59
    second_ids = {'round1-deeper-fp16-0140', 'round1-deeper-fp16-0235'}
    assert {d['id'] for d in read(repair/'remaining-disagreements.json')} == second_ids
    docs = {}; original_answers = {}
    for draft in sorted(ROOT.glob('drafts-*.json')):
        batch = read(draft)['documents']; old_batch = read(original/draft.name)['documents']
        old_audit = read(original/draft.name.replace('drafts-', 'audit-'))
        verify_audit_source(old_audit, old_batch)
        assert [d['id'] for d in batch] == [d['id'] for d in old_batch]
        for old, new in zip(old_batch, batch):
            assert new['id'] not in docs
            if new['id'] in decisions:
                decision = decisions[new['id']]
                assert old['text'] == decision['before'] and new['text'] == decision['after']
            else: assert old == new
            docs[new['id']] = new
        original_answers.update({a['id']: a for a in old_audit['answers']})
    assert len(docs) == 360 and set(docs) == {s['id'] for s in specs}
    adopted = {}; provenance = {}; nonunanimous = []
    for spec in specs:
        ident = spec['id']; gold = {t: LABELS[spec['gold'][t]] for t in TASKS}
        answer = original_answers[ident]
        method = {'initial_auditor': AUDITOR, 'resolution': 'initial-blind-audit'}
        if ident in decisions:
            response = read(repair/'blind-single-document-audits'/(ident+'.json'))
            verify_audit_source(response, [docs[ident]])
            answer = response['answers'][0]
            method.update(resolution=decisions[ident]['action'], repair_ledger='reference-repair-1/repair-ledger.json', single_document_auditor=AUDITOR)
        if ident in second_ids:
            assert answer['labels'] != gold
            response = read(repair/'blind-second-opinion'/(ident+'.json'))
            verify_audit_source(response, [docs[ident]])
            second = response['answers'][0]
            assert second['labels'] == gold
            nonunanimous.append({'id': ident, 'gemma_dissent': answer, 'blind_second_opinion': second,
                                'adjudication_basis': 'Prespecified facts and agent review of unchanged document scope, supported by blind second opinion.',
                                'independence_limit': 'Second-opinion model also wrote original drafts; not independent human validation.'})
            answer = second
            method.update(resolution='agent-adjudication-supported-by-blind-writer-second-opinion', second_opinion_model=WRITER, gemma_unanimous=False)
        assert answer['labels'] == gold, ('Unresolved reference disagreement', ident)
        adopted[ident] = answer; provenance[ident] = method
    rows = [{'id': s['id'], 'state': docs[s['id']]['text'],
             'questions': [{'id': t, 'question': TASKS[t]['question'], 'candidates': HYPOTHESES[t], 'labels': LABELS, 'gold': s['gold'][t]} for t in TASKS],
             'provenance': {'family': s['family'], 'focus': s['focus'], 'writer': WRITER,
                            'not_human_validated': True, **provenance[s['id']]}} for s in specs]
    resolution = {'created_utc': datetime.now(timezone.utc).isoformat(), 'scenarios': 360,
                  'original_disagreements': 59, 'documents_repaired_against_prespecified_facts': 52,
                  'reviewed_documents_unchanged': 7, 'single_document_gemma_agreements': 57,
                  'nonunanimous_adjudications': nonunanimous, 'excluded_scenarios': 0,
                  'classifier_predictions_consulted': False, 'human_validated': False,
                  'ledger_sha256': sha(repair/'repair-ledger.json'),
                  'original_hash_manifest_sha256': sha(repair/'original-hashes.json'),
                  'supplemental_sealer_sha256': sha(__file__),
                  'reference_scope': 'Synthetic fact-first references with agent factual repairs, blind Gemma audits and two openly recorded writer-assisted adjudications.'}
    # Preserve original rejected-drafts.json and raw batch audits. Adopted answers
    # live separately; original generator deliberately cannot silently resume here.
    (repair/'adopted-answers.json').write_text(json.dumps(adopted, indent=2))
    (ROOT/'reference-resolution.json').write_text(json.dumps(resolution, indent=2))
    content = ''.join(json.dumps(r)+'\n' for r in rows)
    with path.open('x') as f: f.write(content)
    manifest = {'purpose': 'fresh-final-evaluation', 'created_utc': resolution['created_utc'],
                'sha256': sha(path), 'scenarios': len(rows), 'generation': config,
                'reference_provenance': resolution['reference_scope']+' No human validation. All prespecified cases retained; no classifier-based selection.',
                'families': sorted({s['family'] for s in specs}), 'freeze_sha256': sha(FREEZE),
                'reference_resolution_sha256': sha(ROOT/'reference-resolution.json')}
    with manifest_path.open('x') as f: json.dump(manifest, f, indent=2)
    verify(freeze)
    print(json.dumps({'sealed': str(path), 'scenarios': len(rows), 'decisions': len(rows)*4, 'sha256': sha(path), 'nonunanimous_reference_adjudications': len(nonunanimous)}))

if __name__ == '__main__': main()
