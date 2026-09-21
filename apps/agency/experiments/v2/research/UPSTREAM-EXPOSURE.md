# V2 candidate provenance

Research checked 21 September 2026. Candidate, not yet selected for deployment.

The pinned DeBERTa NLI model card lists supervised training on MultiNLI, FEVER-NLI, ANLI, LingNLI and WANLI, and declares MIT licensing. It is already a trained inference classifier; our work adapts it to travel requirements rather than training language understanding from scratch.

Source: https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli/blob/b3546ea6b0346eb6f8d5d68b13c7dc6d0376b3d7/README.md

This disclosure does not establish that public pilot test rows were absent from all upstream pretraining. The broader language-model pretraining corpus is not exhaustively audited here. The ModernBERT V1 exposure findings in research/UPSTREAM-EXPOSURE.md apply to that distinct checkpoint, not automatically to V2.

The public suite remains a separate generalization observation. Native typed API benchmarks and our normalized candidate-choice interface are not interchangeable. Report task-specific reference agreement, uncertainty, latency and model history without claiming universal superiority.
