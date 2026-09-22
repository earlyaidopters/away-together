# A–Z tutorial acceptance audit

21 September 2026. Previous goal turn: progress, because it changed authoritative copy and synchronized the page. This turn completes tutorial verification and delivery; it does not redefine the request as a wording-only change.

Authority: 29-scene FILMING-GUIDE.md, explainer/index.html, repository/docs/STEP-BY-STEP.md, repository/prompts/TRAIN-MY-SPECIALIST.md and tools/tutorial.py. Planned duration 18:40, 2,265 spoken words. The latest comprehensive request supersedes the older 5–10-minute summary.

| Explicit requirement | Evidence inspected | Result |
|---|---|---|
| Find an open classifier already useful before our training | choose-model scene; exact author model card and pinned revision; guide step 1 explains task, weights, terms and evaluation criteria | Met |
| Show a benchmark and visual | baseline-development.png and matching JSON; saved 74.75% before / 93.63% after on the same 800 development decisions; separate 66.5% final-test caveat | Met, scoped to development evidence |
| Download the model | download scene; tools/tutorial.py download; actual pinned cache resolution; guide explains files, expected receipt and first-download internet | Met |
| Ask Codex to fine-tune for a specific circumstance | build scene; eight-section prompt; job/input/output/boundary contract; beginner setup prompt | Met |
| Next slide shows our example | exact scene order build → travel-brief → prompt; four explicit refund/arrival/pool/hike rules | Met |
| Provide a substantial sample prompt | 6,981-character full prompt with eight sections; copied in-browser and pasted into a controlled textarea, confirming eight sections and final delivery requirement | Met |
| Underline pertinent parts | underlined bracketed job, input, questions and answers on prompt scene and full prompt page; tested prompt tabs and reset | Met |
| Continue from A to Z with substance | 12 written steps; exact commands and expected outputs; schema, split, baseline, real training, frozen paired test, mistakes, new-input prediction, app/image integration and adaptation boundaries | Met |
| Real usable workflow rather than mocked training | actual eight-decision baseline/train/test/predict receipts in evidence/tutorial-smoke; finite training loss, saved checkpoint, paired rows and a new prediction; no quality claim from the smoke run | Met |
| Preserve supplied demo and test integrity | exclusive workshop, exact overlap/schema validation, changed checkpoint/data/manifest refusal, final-report overwrite refusal; original agency artifact hashes all match the companion | Met |
| Keep persona design and conversational actions | pixel personas/sage/forest style retained; user-approved “Give it three choices.”; no rejected headings in either page source; live pond/button and prompt screenshots inspected | Met |
| Keep website, guide and source together | one private repository; current explainer, guide/PDF, prompt, training tool and smoke receipts synchronized; local source byte comparison and Git source checks | Met locally; remote verified after push |

## Verification scope

- All 29 filming scenes were navigated and captured at 1440×900, 1920×1080, 1366×768 and 390×844. The retained layout receipt contains 116 correct scene positions with no horizontal overflow. It is in output/qa/audience-screens/step-by-step/layout.json. Mobile baseline and prompt fixes were reinspected individually.
- Full prompt and full guide pages were inspected at desktop and 390px. No horizontal overflow. The download deep link lands below the header. Copying was verified by a real paste, not merely the button label. Prompt tab 6 and R reset were exercised.
- 38 local links/assets/anchors on the main page and two companion pages resolve.
- 21 tutorial/audience tests pass, including final-report overwrite, checkpoint mutation, data mutation and rewritten-manifest rejection. Agency Python suite: 62 tests and 4 subtests pass; two dependency deprecation warnings. Agency frontend: 4 tests pass and production build passes.
- Source checker passes with all new files staged; pinned upstream hashes remain unchanged. Production checker: 16 passes, zero errors or warnings. Narration exactly matches the guide.
- All 31 PDF pages rendered and inspected; the final changed image-model spoken page was rerendered and inspected after its two-word expansion. No TTS was requested.
- Context-aware Mindlight review is output/qa/STEP-BY-STEP-REVIEW.md. It identifies real-viewer comprehension and pace as empirical unknowns, not fabricated perfect satisfaction.

## Limits retained

Smoke execution is not a full-training quality benchmark. New-domain app serving needs an adapter and fresh validation; the exact supplied travel/image integration is included for inspection and use. Historical V1/V2 results are not assigned to the new tutorial recipe. No hosted Jev parity, superiority, all-machine compatibility, universal cost claim or human validation is asserted.

Publication, public repository access, final recorded-transcript reconciliation and original-code reuse terms remain launch-stage work. The repository remains private by user instruction. These do not prevent completing this authored, executable A–Z tutorial.
