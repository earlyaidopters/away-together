"""One documented pre-inference reference repair; no contestant results are read.

Exact replacements reviewed against the original, prespecified latent facts.
All originals are archived before any mutation. This is not model tuning.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('experiments/v2/final/round1-deeper-fp16')
EDITS = {}

def edit(number, old, new):
    EDITS.setdefault(number, []).append((old, new))

edit(7, 'However, arrival and registration', 'For the unselected Birch offer only, arrival and registration')
edit(7, '^2 Automatic check-in at 01:30.', '^2 Birch only: automatic check-in at 01:30.')
edit(8, 'A guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving, though no rules address overnight registration or whether prior contact is necessary generally.', 'The void old policy required a guest reaching reception at 01:30 to obtain permission before arriving. Under the current terms, no rules address overnight registration or whether prior contact is necessary.')
edit(16, '; the hike with a guide requires a separate 38 euro payment.', '.')
edit(16, 'While an alternative policy notes', 'While the December-only policy notes')
edit(31, 'This creates a discrepancy requiring client clarification.', 'That permission requirement belongs only to the unselected Birch offer.')
edit(37, 'so you may face issues at 01:30', 'so the overnight procedure is undocumented')
edit(37, 'Please note the scope: this applies to the selected Alder offer, whereas the distractor belongs to a different, unselected Birch offer. We cannot confirm the pool details beyond this fee structure.', 'The 19 euro pool charge belongs only to the unselected Birch offer. For the selected Alder offer, pool location, price and booking access remain undocumented.')
edit(50, 'Regarding refunds, neither the payment returned nor the method of refund for cancellation is documented. The current selected terms completely replace the old policy, which previously suggested a full return of payment before the cutoff.', 'Regarding current refunds, cancelling before the cutoff still retains a mandatory administration charge of 27 euros. The current selected terms completely replace the old policy, under which neither the payment returned nor the method of refund for cancellation was documented.')
edit(61, 'While the booked accommodation has an operational swimming pool on its premises, the selected Alder offer charges booked guests 19 euros to enter, in addition to the holiday price. Note that the free pool mention belongs to the unselected Birch offer.', 'The selected Alder accommodation has an operational swimming pool on its premises, available during the stay without any separate fee. The unselected Birch offer charges booked guests 19 euros to enter its onsite pool, in addition to the holiday price.')
edit(67, 'However, please note that the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment. This applies specifically to the selected offer, Alder, as the distractor belongs to a different, unselected Birch offer.', 'For your selected Alder offer, the quoted amount pays for a walking excursion on a trail accompanied by a human guide, with nothing further to pay. The different, unselected Birch offer covers accommodation only; taking a hike with a guide under Birch requires a separate 38 euro payment.')
edit(78, 'neither the activity itinerary nor any statement confirming a guided walk is included in the amount quoted.', 'we have not supplied an activity itinerary or information about whether the quoted amount includes a guided walk.')
edit(81, 'The amount quoted covers accommodation only, and neither', 'Neither')
edit(85, 'However, per our unbooked offer policy for the facility, the booked accommodation', 'For the unselected Birch offer only, the accommodation')
edit(91, 'While the quoted amount covers accommodation only, the unbooked offer policy for activity states', 'For selected Alder, the quoted amount covers accommodation only; taking a hike with a guide requires a separate 38 euro payment. By contrast, the unselected Birch activity policy states')
edit(97, 'While the standard policy states the entire payment is returned as money with no deduction before the cancellation cutoff, a mandatory administration charge of 27 euros applies to all cancellations regardless of timing.', 'For selected Alder, the entire payment is returned as money with no deduction before the cancellation cutoff. For unselected Birch, cancelling before the cutoff still retains a mandatory administration charge of 27 euros.')
edit(98, 'However, a mandatory administration charge of 27 euros is retained for cancellations before the cutoff.', 'Under the void old policy, a mandatory administration charge of 27 euros was retained for cancellations before the cutoff.')
edit(98, 'though the voided old policy also mentioned the 27 euro charge', 'including its former 27 euro charge')
edit(100, 'However, please be aware that cancelling before the cutoff still retains a mandatory administration charge of 27 euros. This specific charge applies to your selected stay dates, whereas other policies apply exclusively to December stays.', 'For December stays only, cancelling before the cutoff still retains a mandatory administration charge of 27 euros. That charge does not apply to your selected 8–15 May stay, whose refund terms are undocumented.')
edit(104, ', though a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.', '. Under the void old policy, a guest reaching reception at 01:30 could not check in unless they obtained permission before arriving.')
edit(104, 'These are the only active terms for your stay.', 'The prior-permission requirement described above was an old term and is no longer active.')
edit(106, '; however, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.', ' for your May stay. For December stays only, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.')
edit(106, '^1 Note: The policy regarding 01:30 arrivals applies to other dates as well, but the distractor applies exclusively to December stays, so your May dates are governed by the standard terms above.', '^1 Note: The prior-permission policy applies exclusively to December stays. Overnight registration and prior-contact rules for your May dates are not documented.')
edit(118, 'The accommodation charges booked guests 19 euros to enter its onsite swimming pool, in addition to their holiday price.', 'A swimming area is mentioned but its location, price and booking access conditions are not stated.')
edit(122, 'Before the cancellation cutoff the entire payment is returned as money, with no deduction.', 'Under the now-void old policy, cancellation before the cutoff returned the entire payment as money, with no deduction. Neither the payment returned nor the refund method is documented under the current terms.')
edit(124, 'Arrival at 01:30 requires prior permission.', 'No rules address overnight registration or whether prior contact is necessary.')
edit(139, 'However, the activity itinerary or any statement about a guided walk being included in the amount quoted is not supplied in the offer details.', 'For the unselected Birch offer, neither the activity itinerary nor any statement about a guided walk being included in the amount quoted is supplied.')
edit(151, 'Also, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving, despite the automatic registration claim.', 'For the unselected Birch offer only, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.')
edit(157, '1. The booked accommodation', '1. For the unselected Birch offer only, the accommodation')
edit(158, 'However, the booked accommodation has an operational swimming pool on its premises, available during the stay without any separate fee.', 'The void old policy stated that the booked accommodation had an operational swimming pool on its premises, available during the stay without any separate fee.')
edit(163, 'but this applies strictly to the selected offer.', 'but this applies strictly to the unselected Birch offer.')
edit(170, 'so this fee applies.', 'so that old fee no longer applies; the current refund amount and method remain undocumented.')
edit(176, 'Under these new terms, arrival and registration at 01:30 are available automatically, without any earlier contact or request.', 'Under the current terms, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving. Under the now-void old policy, arrival and registration at 01:30 were available automatically, without any earlier contact or request.')
edit(178, 'For your selected stay of 8–15 May, arrival and registration at 01:30 are available automatically, without any earlier contact or request. The distractor policy regarding December stays does not apply here.', 'For your selected stay of 8–15 May, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving. Automatic arrival and registration at 01:30 without earlier contact or request apply exclusively to December stays.')
edit(201, 'The amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment. ', '')
edit(211, 'The amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.', 'For the unselected Birch offer only, the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.')
edit(235, 'This applies to the selected Alder offer, not the distractor Birch one.', 'That missing activity information concerns the unselected Birch offer only.')
edit(247, 'Note the unbooked offer policy for arrival:', 'For selected Alder, arrival and registration at 01:30 are available automatically, without any earlier contact or request. Note the unselected Birch policy for arrival:')
edit(247, 'This contradicts the standard automatic registration expectation, so explicit client confirmation is required for late arrivals.', 'The Birch permission requirement does not govern the selected Alder booking.')
edit(254, 'This voids the old policy for the facility.', 'This was the old facility policy and is now void.')
edit(264, 'neither an activity itinerary nor any statement confirming a guided walk is included in the amount quoted for your booking.', 'we have not supplied an activity itinerary or information about whether the quoted amount includes a guided walk.')
edit(265, 'Note that cancelling before the cutoff', 'For the unselected Birch offer only, cancelling before the cutoff')
edit(268, 'Arrival and registration at 01:30 are available automatically, without any earlier contact or request.', 'A guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.')
edit(271, 'Arrival: Arrival and registration at 01:30 are available automatically, without any earlier contact or request.', 'Arrival: For selected Alder, no rules address overnight registration or whether prior contact is necessary. For the unselected Birch offer only, arrival and registration at 01:30 are available automatically, without any earlier contact or request.')
edit(287, 'Furthermore, no activity itinerary or statement confirming a guided walk is included in your quoted price.', 'Furthermore, no activity itinerary or information about whether a guided walk is included in your quoted price has been supplied.')
edit(287, '4. No guided walk is included.', '4. Guided-walk inclusion is undocumented.')
edit(295, 'A: Arrival and registration at 01:30 are available automatically, without any earlier contact or request.', 'A: For selected Alder, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving. For unselected Birch only, arrival and registration at 01:30 are available automatically, without any earlier contact or request.')
edit(301, 'Facility: The booked accommodation has an operational swimming pool on its premises, available during the stay without any separate fee. Note that general mentions of a swimming area elsewhere lack specific location or price details, but this specific offer includes it freely.', 'Facility: For selected Alder, a swimming area is mentioned but its location, price and booking access conditions are not stated. For unselected Birch only, the accommodation has an operational swimming pool on its premises, available during the stay without any separate fee.')
edit(307, 'Please note that the quoted amount covers accommodation only; a guided hike requires a separate 38 euro payment.¹', 'For selected Alder, neither the activity itinerary nor any statement about a guided walk being included in the amount quoted is supplied. Neither the payment returned nor the method of refund for cancellation is documented.¹')
edit(307, '¹ The amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment. This offer is distinct from the unselected Birch offer.', '¹ For the different, unselected Birch offer only, the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.')
edit(316, 'Arrival and registration at 01:30 are available automatically, without any earlier contact or request.', 'No rules address overnight registration or whether prior contact is necessary.')
edit(319, 'However, please note that a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving, as no rules address overnight registration otherwise.', 'For selected Alder, no rules address overnight registration or whether prior contact is necessary. For unselected Birch only, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.')
edit(320, '; however, a guest reaching reception at 01:30 cannot check in unless they obtained permission before arriving.', '. Under the void old policy, a guest reaching reception at 01:30 could not check in unless they obtained permission before arriving.')
edit(325, 'However, please be aware that the accommodation charges booked guests 19 euros to enter its onsite swimming pool, in addition to their holiday price.', 'For the unselected Birch offer only, the accommodation charges booked guests 19 euros to enter its onsite swimming pool, in addition to their holiday price.')
edit(325, 'This applies strictly to the selected Alder offer;', 'The included guided excursion applies strictly to the selected Alder offer;')
edit(331, 'The amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.', 'For the unselected Birch offer only, the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.')
edit(331, 'Ensure client understands the hike is not included in their current quote.', 'Guided-walk inclusion in the selected Alder quote remains undocumented.')
edit(337, 'Note that neither the payment returned nor the method of refund for cancellation is documented in our system.', 'For the unselected Birch offer only, neither the payment returned nor the method of refund for cancellation is documented in our system.')
edit(343, 'Regarding arrival, registration at 01:30 is available automatically; no earlier contact or request is necessary.', 'For selected Alder, no rules address overnight registration or whether prior contact is necessary. For unselected Birch only, arrival and registration at 01:30 are available automatically, without any earlier contact or request.')
edit(346, 'While other dates may have different rules, the distractor policy applies exclusively to December stays and does not affect your current booking.', 'For December stays only, no rules address overnight registration or whether prior contact is necessary. Those December terms do not affect your current booking.')
edit(346, 'However, be advised that neither the payment returned nor the method of refund for cancellation is documented.', 'However, cancelling before the cutoff still retains a mandatory administration charge of 27 euros.')
edit(352, 'The amount quoted does not include a guided walk; neither', 'Neither')
edit(356, 'Under these new terms, the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment. This contrasts with the old void policy.', 'Under the void old policy, the amount quoted covered accommodation only; taking a hike with a guide required a separate 38 euro payment. That old policy no longer applies.')
edit(358, 'The amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.', 'For December stays only, the amount quoted covers accommodation only; taking a hike with a guide requires a separate 38 euro payment.')

UNCHANGED = {17, 80, 114, 140, 266, 267, 344}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert not (ROOT/'test.jsonl').exists(), 'Reference changes forbidden after seal'
    rejects = json.loads((ROOT/'rejected-drafts.json').read_text())
    assert set(EDITS) | UNCHANGED == {int(x['spec']['id'].rsplit('-', 1)[1]) for x in rejects}
    assert not set(EDITS) & UNCHANGED
    archive = ROOT/'reference-repair-1'/'originals'
    archive.mkdir(parents=True, exist_ok=False)
    files = sorted(ROOT.glob('drafts-*.json')) + sorted(ROOT.glob('audit-*.json'))
    files += [ROOT/n for n in ['rejected-drafts.json', 'reference-specs.json', 'generation-config.json', 'draft-corpus-receipt.json', 'draft-length-preflight.json']]
    receipt = {}
    for p in files:
        shutil.copy2(p, archive/p.name)
        receipt[p.name] = digest(p)
    (archive.parent/'original-hashes.json').write_text(json.dumps(receipt, indent=2))
    decisions = []
    for x in rejects:
        ident = x['spec']['id']; n = int(ident.rsplit('-', 1)[1]); old = x['document']['text']; new = old
        for before, after in EDITS.get(n, []):
            assert new.count(before) == 1, (ident, before, new.count(before))
            new = new.replace(before, after)
        decisions.append({'id': ident, 'action': 'surgical_fact_repair' if n in EDITS else 'unchanged_auditor_disagreement', 'spec': x['spec'], 'before': old, 'after': new, 'replacements': EDITS.get(n, []), 'rationale': 'Restore prespecified facts and policy scope without changing latent labels or removing distractors.' if n in EDITS else 'Document already matches prespecified facts; original blind auditor confused absent information with a negative policy or treated void terms as current. Re-audit unchanged.'})
    plan = {'created_utc': datetime.now(timezone.utc).isoformat(), 'stage': 'before_any_contestant_predictions', 'all_cases_retained': 360, 'reference_method': 'Agent-reviewed factual corrections against prespecified facts, followed by fresh blind single-document Gemma audits. No human validation. Auditor receives no specs, labels or prior audit.', 'decisions': decisions}
    (archive.parent/'repair-ledger.json').write_text(json.dumps(plan, indent=2))
    revised = {d['id']: d['after'] for d in decisions}
    for p in sorted(ROOT.glob('drafts-*.json')):
        batch = json.loads(p.read_text())
        for d in batch['documents']:
            if d['id'] in revised: d['text'] = revised[d['id']]
        p.write_text(json.dumps(batch, indent=2))
    print(json.dumps({'reviewed': len(decisions), 'repaired': len(EDITS), 'unchanged': len(UNCHANGED), 'archive': str(archive)}))

if __name__ == '__main__': main()
