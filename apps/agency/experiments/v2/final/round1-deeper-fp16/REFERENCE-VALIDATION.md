# Fresh round 1 reference validation

The frozen contestant did not generate or adjudicate these references, and no contestant predictions were inspected before sealing.

All 360 prespecified scenarios remain, comprising 1,440 policy decisions. The original Qwen rendering and six-document Gemma audits are retained in `reference-repair-1/originals/`. The initial audit disagreed with the prespecified facts on 59 documents. Agent review found 52 writer departures or material wording ambiguities and made surgical corrections to restore the original facts, scope and omissions. Seven documents remained unchanged. No latent label changed and no case was dropped.

All 59 reviewed documents received one fresh, blind, single-document Gemma audit with the original prompt and decoding settings. Gemma agreed on 57. It still treated a void old fee as current in case 0140 and applied unselected-offer uncertainty to the selected offer in case 0235. The documents were not simplified to obtain agreement.

One blind Qwen second opinion was obtained for each of those two fixed cases, without giving it prespecified facts, expected labels, prior audits or a reason for selection. It agreed with the original facts and agent scope review. Qwen also wrote the original drafts: this is writer-assisted adjudication, not independent validation. Gemma's dissent is retained. The per-row provenance and sealed manifest explicitly disclose these two adjudications.

These references are synthetic and model-assisted, without human validation. Audit agreement is a consistency check, not proof of real-world correctness or diversity. The repaired test cannot establish real booking safety.

The original generator remains byte-for-byte unchanged. Its direct resume path deliberately refuses the repaired drafts because original batch audits no longer match their text. `experiments/v2/seal_repaired_round1.py` is the supplemental sealer: it verifies original archives, unchanged prespecified facts, every document repair, all raw audits and the frozen model before writing the final corpus. Re-running that sealer verifies the existing seal without changing it. Do not rerun the original generator over the sealed repaired corpus.

After repairs, all 1,440 document-policy tokenizer pairs remain below the 512-token limit (maximum 216). No truncation, prediction-based filtering, reference-clause oracle or contestant-guided adjustment occurred.
