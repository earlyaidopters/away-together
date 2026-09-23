# V3 lab notes (started 22 September 2026)

Goal: research first. Beat or honestly lose to Jev on a fresh round 2, and dial in photo understanding. Mark authorized a fresh Jev round 2 under the existing rules and USD 10 cap (about USD 0.39 reserved so far), and a second promotion rule: the agency app may run a candidate that passes the quality gates and clearly beats V1 even if it does not beat Jev. Any "beats Jev" claim still needs the original superiority gate.

Rules carried over from V2: Jev outputs never enter training, selection, calibration or revisions. Round 1 final data (experiments/v2 final round) is not used for V3 development or selection. Rules are selected on development, thresholds fitted on calibration, then frozen before any fresh final generation.

## Text readers, development evidence (no final data touched)

`probe_development.py` records raw predictions in `runs/predictions-<engine>-<split>.jsonl`. `analyze_text.py` and `combine.py` read them.

| split | V2 frozen | OpenJev text, 1 read | both agree | accuracy when agreeing | either correct |
|---|---:|---:|---:|---:|---:|
| dev (1600 decisions) | 90.87% | 86.62% | 84.8% | 96.02% | 96.13% |
| authored hard dev (576) | 94.97% | 95.14% | 91.7% | 99.43% | 98.96% |
| calibration (1600) | 87.56% | 84.25% | 79.4% | 95.52% | 95.94% |

V2 reproduced its frozen development record exactly (combined 91.96%, hard 94.97%).

Log-linear pooling p ∝ p_V2^0.75 · p_OpenJev^0.25 (weights grid-selected on combined dev only): dev 93.57%, calibration 91.06% versus V2 alone 87.56%. Per-policy weights overfit dev (95.08%) with no calibration gain, so they are rejected.

OpenJev 4-read text sampling changes 6 of 564 early choices versus 1 read; being recorded as a separate configuration.

## Vision evaluation

48 fictional listing photos generated with Nano Banana (`gemini-3.1-flash-image`), eight per feature: four clear positives and four hard look-alikes. Prompts, hashes and timestamps in `vision/generation-manifest.json`; specs in `vision/specs.json`.

Labels for all six features on every photo were fixed by agent visual review before any OpenJev read (`vision/labels.json`, provenance in `vision/labels-with-meta.json`). Not human verified. Several generations deviated from their prompt; labels follow the actual pixels.

Baseline, current app rule (one read, visible with p ≥ .8), 266 labelled decisions:

- visible precision 46/71 (64.8%), recall 46/49, 25 false "visible"
- false visible by feature: mountains 9, garden 8, ocean 4, ramp 2, pool 1, steps 1
- lake and river read as ocean; flat or hilly scenes read as mountains; bare terraces and coastlines read as garden
- pool hard negatives (koi pond, reflecting pool, lake) were correctly rejected
- four reads with different seeds gave identical choices on all 266 decisions, so read agreement is not a usable confidence signal

This 48-photo set is now vision development data. Any rewritten questions or second vision model must be judged on a fresh, separately generated photo test set after the rule is frozen.

## Laya

Pinned inspection notes in `experiments/laya/LESSONS.md`. Repository is Apache-2.0, now at v0.3.6. Its typed-decisions gold came from a roughly 4B-class teacher that its card says is not affiliated with TypeSafe, so Laya weights are not Jev-distilled. `laya-typed-decisions` was trained on typed-decisions, which is our public typed lane; any typed-lane result using it must be reported as exposed.

## Outcome (22 September 2026)

Mark stopped the broader research (Laya fine-tune, ensemble, Jev round 2) in favour of improving the existing app. What shipped:

- V2 now runs the agency under the app rule. Like-for-like on round 1: V1 60.28%, V2 95.28% (+35.0, CI 32.5 to 37.5). Median 99 ms vs 144 ms.
- Startup warm-up of the text model and the photo prefill cache. First check after restart ~120 ms text instead of 8.5 s.
- Rewritten photo questions. Held-out set in vision/holdout (30 photos, wording frozen first, unmentioned look-alikes): false "visible" 10 to 4, precision 72% to 87%, recall unchanged 26/26. Development-set gains are not claimed.

Zero-shot Laya (laya-mlx port, commit 0a85951863) scored 37.1% on dev, choosing the first option 92% of the time; not used. The V2 + OpenJev text pooling result above stays a development finding only; it is not in the app and was never tested on fresh data.
