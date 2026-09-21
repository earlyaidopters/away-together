# Contributions and provenance

## Mark Kashef / Prompt Advisers

Product concept, traveller personas and requirements, experiment direction, task/data design, training and evaluation workflow, local agency application, multimodal integration, evidence presentation, plain-English teaching sequence and companion resource. AI coding assistants were used in implementation and review.

## Upstream building blocks

- ModernBERT NLI starting checkpoint: MoritzLaurer/ModernBERT-base-zeroshot-v2.0, revision in apps/agency/models/selection.json.
- Later DeBERTa-based text challenger: source and pins in the companion frozen experiment.
- OpenJev: razorback16/openjev, commit e04794ab36e4f7e6040c2547baecdb2737ce2e79. Apache 2.0 license is retained with its vendored source.
- Vision weights: mlx-community/diffusiongemma-26B-A4B-it-4bit, revision a7a81407613811e8ba63af92ac0d852b809e191f. Downloaded separately under upstream model terms.
- PyTorch, Transformers, MLX/MLX-VLM, FastAPI, React, Vite, GSAP and HyperFrames support execution, application and visual teaching.
- Poppins font license is retained beside the font. Listing photos are AI-generated fictional examples.

This project is independent of TypeSafe/Jev. Comparison does not imply affiliation or endorsement. Original project authorship does not replace the authorship or licenses of its dependencies. See ../THIRD-PARTY-NOTICES.md.
