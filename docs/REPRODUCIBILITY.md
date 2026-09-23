# Inspect evidence before rerunning experiments

There are three levels of checking this project. Pick the one you need; reading saved evidence does not require a paid benchmark call.

## 1. Inspect the saved results

Start with [BENCHMARKS](BENCHMARKS.md), [frozen V2 report](../evidence/FROZEN-V2-RESULTS.md), [machine-readable summary](../evidence/frozen-v2-summary.json), [vision verification](../evidence/VISION-VERIFICATION.md) and [photo-toggle receipts](../evidence/vision-causal-checks.json).

The explainer also includes an [actual training record](../apps/explainer/assets/training-example.json), [held-out V1 example](../apps/explainer/assets/held-out-example.json), [real V2 mistake](../apps/explainer/assets/benchmark-case.json) and [source fingerprints](../apps/explainer/assets/teaching-evidence.json). Read the full input rather than relying only on an on-screen excerpt.

The complete companion release preserves checkpoints, raw rows and reference audits. The Git checkout deliberately excludes large model files. Its [restore tool](../tools/restore_companion.py) verifies archive paths and manifest hashes, refuses conflicting source, and adds missing files. A clean restore and second no-op restore were verified; see [receipt](../evidence/audience-revision/audience-clean-restore.json).

## 2. Run the app and source checks

Follow [SETUP](SETUP.md) for installation and the full test commands. For repository-level integrity, from the root:

```bash
npm run check:source
```

This checks scene metadata, pinned upstream file hashes, tracked file sizes and a limited set of credential patterns. It is not a comprehensive security audit, model evaluation or substitute for live inference. Its Git inventory requires a Git checkout; archive users should initialize/import their source into Git before using that inventory check.

Use the [API example](API-EXAMPLE.md) for an actual text request. In the explainer, compare Maya with and without the stairs image. The [photo lab](../apps/explainer/photo-lab.html) is served through localhost:8770 and accepts your own PNG/JPEG; opening its HTML directly does not start the API.

## 3. Reproduce or extend training

Read the preserved [V2 protocol](../apps/agency/experiments/v2/PROTOCOL.md) before running experimental scripts. It defines the test boundaries and promotion gate. Some commands download large assets or call hosted Jev using separately configured credentials and paid usage. Do not run every script in filename order: this directory preserves distinct experiment stages and historical runners, not a single install recipe.

For a new domain, follow [ADAPT-YOUR-OWN](ADAPT-YOUR-OWN.md). Use a new directory, define labels, separate related cases into train/development/test groups, establish a baseline, and freeze before the final comparison. Do not tune the old frozen travel model on its final mistakes. The working support converter prepares records; a support trainer, serving adapter and evaluation still need to be configured.

## What the evidence does not establish

- Broad image accuracy or safe real-world booking decisions.
- Superiority over Jev: the later text challenger lost its frozen comparison.
- Generalization beyond the reported domains. The later V1-to-V2 comparison used the same 360 synthetic travel scenarios; earlier V1 reports use different tests and must not be mixed with it.
- Human-validated reference answers: the travel test is synthetic and agent-reviewed.
- Universal speed, savings, minimum hardware or cross-platform vision support.
- A one-prompt build or an original foundation model.
