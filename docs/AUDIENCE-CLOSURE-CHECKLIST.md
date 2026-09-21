# Audience-gap closure checklist

Status: 26 of 27 checks meet the defined 10/10 acceptance rubric. Q23 remains 6/10. Goal remains active.

A 10 means the scoped question is clearly answered in the correct scene, supported by an appropriate visual/resource, accurate to the evidence, and verified. Each dimension scores 0–2. It does not mean perfect model accuracy, guaranteed audience understanding, or every feature requested in unrelated videos has been built. Answering “not tested” can close a compatibility question; it does not establish compatibility.

Basis: 405 retrieved comments from the latest ten regular videos; 35 replies were not recovered. Owner replies and praise are retained in the disposition CSV but not counted as distinct audience objections. Repeated concerns map to consolidated questions.

| ID | Question / acceptance item | Score | Satisfied | Main scene | Evidence |
|---|---|---:|---|---|---|
| Q01 | Why use this instead of ChatGPT or Jev? | 10/10 | Yes | why | Baseline-first guidance; no universal superiority promise. |
| Q02 | What did Mark build, and what came from elsewhere? | 10/10 | Yes | build | Prepared specification downloadable; THIRD-PARTY-NOTICES retained; provenance stated in spoken guide. |
| Q03 | Why use AI for a price check? | 10/10 | Yes | rules | Budget stays arithmetic; actual API example returned model policy reason separately. |
| Q04 | Are fixed answers always correct or deterministic? | 10/10 | Yes | labels | Three-choice interaction; uncalibrated probability and no determinism guarantee disclosed. |
| Q05 | Is fine-tuning the same as writing a prompt? | 10/10 | Yes | practice | Training vs normal request diagram; runtime/layout/contrast checks at 0, 9, 18 seconds passed. |
| Q06 | Do I have to train before trying the demo? | 10/10 | Yes | first-run | Fresh uv sync --frozen; prerequisite checker passed; existing saved weights selected. |
| Q07 | Where did the examples come from? | 10/10 | Yes | test | Actual training and held-out record downloads with source hashes; synthetic/reference repair limits spoken. |
| Q08 | How many examples should I use? | 10/10 | Yes | repurpose | 20-case smoke test explicitly not a training minimum; split leakage guidance in adaptation doc. |
| Q09 | How do I adapt the support example? | 10/10 | Yes | repurpose | Editor add/reset verified; converter maps labels to candidate index; invalid/duplicate data tests passed. |
| Q10 | What did the benchmark compare? | 10/10 | Yes | results | Frozen 360-case/1440-decision comparison; V2 95.28 vs Jev 98.61; loss and text-only scope shown. |
| Q11 | Why does the live app use V1? | 10/10 | Yes | results | Active V1 and later V2 separated; historical different-corpus 66.5 is not a same-test gain. |
| Q12 | How do I know a test was fair? | 10/10 | Yes | failure | Actual failed 01:30 case with full-input downloadable receipt. |
| Q13 | Does this make pictures or read them? | 10/10 | Yes | vision | Local photo endpoint runs on supplied pixels; stairs and pond fresh receipts; nine fictional shared images disclosed. |
| Q14 | Can hosted Jev recognize images? | 10/10 | Yes | vision | Explicit distinction: local demonstration does not establish current hosted Jev image support. |
| Q15 | Do my photo files leave my computer? | 10/10 | Yes | vision | Fixed loopback endpoint and no filename upload verified by regression test; browser native file-picker verified. |
| Q16 | What can I conclude from a photograph? | 10/10 | Yes | boundary | Pond boundary reveal and access/price/safety limits in guide. |
| Q17 | What does a green card mean? | 10/10 | Yes | rules | Rules diagram and decline/review distinction; no booking or autonomous approval. |
| Q18 | Does it replace a general assistant? | 10/10 | Yes | why | Narrow task scope and unsupported phone/always-on/helpdesk promises removed. |
| Q19 | Does it work on Windows, Linux or my phone? | 10/10 | Yes | setup | Tested host clearly separated from minimum requirements; Windows/Linux and small-memory unvalidated. |
| Q20 | What does it cost? | 10/10 | Yes | cost | Build and run costs separated; total build bill and universal price ratio not measured. |
| Q21 | How fast is it? | 10/10 | Yes | cost | Cold request, warm HTTP and forty-offer photo run visibly separated by workload. |
| Q22 | What happens after sleep or a failure? | 10/10 | Yes | first-run | Live status checker verified; restart instructions and no fake answer on outage regression test. |
| Q23 | Can I download, modify or sell this? | 6/10 | No | take-it | Private source kit and release prepared. This same repository becomes public at video go-live. Public download verification and final reuse terms are launch-stage checks. |
| Q24 | How do I connect the decision to another app? | 10/10 | Yes | rules | Actual API example executed successfully: match plus budget/policy reasons. Support adapter limits explicit. |
| Q25 | Keep the explanation concrete and conversational | 10/10 | Yes | all | Published-transcript voice fingerprint; no-ai-slop pass; 1,512 spoken words with concrete travel nouns and short conclusions. |
| Q26 | Preserve persona look and readable filming surfaces | 10/10 | Yes | demo | Pixel Maya, sage/forest palette and rounded cards retained. All 18 scenes captured at 1440×900, 1920×1080, 1366×768 and 390×844; no horizontal overflow. |
| Q27 | Keep guide, diagrams and narration synchronized | 10/10 | Yes | all | 20-page PDF rendered and visually inspected. 18 scenes / 1,512 words / 12:10. Production check: 16 pass, 0 warning, 0 error. |

## Remaining requirement

Q23 requires an authorized viewer-accessible delivery, explicit original-code reuse terms, retained third-party terms, and an unauthenticated download/restore check. Current private instructions are honest but do not satisfy public viewer access. Approved delivery: one repository, private now and public at video go-live. Do not create a second repository. Public access verification and final component reuse terms are deferred to launch; do not publish now.

## Verification receipts

- `output/qa/audience-photo-live.json`: fresh stairs and pond observations.
- `output/qa/audience-screens/`: all scenes at four viewport sizes; animation states and live-upload screenshot.
- `output/qa/audience-practice-check.json`, `audience-rules-check.json`: runtime/layout/contrast pass; one non-blocking Studio nesting warning each. Embedded filming diagrams are the intended use, not a Studio timeline delivery.
- `scripts/test_audience_revision.py`: 11 tests passed.
- Repository agency: 38 tests passed; frontend: four tests passed and production build passed.
- Fresh dependency install and first-run prerequisite check passed; documented API snippet returned real status/reasons.
- PDF: 20 rendered pages inspected, no clipped paragraphs; narration and timings derived from the canonical guide.

The checklist is an editorial/engineering acceptance review, not a fresh human focus group.
