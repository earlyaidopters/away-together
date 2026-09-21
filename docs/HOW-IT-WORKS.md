# The idea in everyday language

Maya wants a refund if she cancels. She also wants to avoid entrance stairs. A nice-looking hotel can still fail either wish.

1. **Read the words.** The text model checks what the written policy supports.
2. **Look at the pictures.** The image model reports visible features such as stairs or a pool.
3. **Use the answers.** Ordinary code checks Maya’s budget and wishes. A failure means decline. Missing evidence means review. All checks passing means a model-based match.

A **classifier** chooses a label. For a simple refund lesson, that could be cash, credit or cannot tell. The actual text engine compares each requirement with the policy and returns meets, violates or insufficient evidence.

A **pretrained model** has already learned patterns before this project starts. Our active reader starts from a pinned ModernBERT NLI model. We give it extra labeled travel practice. That extra training is **fine-tuning**. It changes saved numerical settings called weights.

We keep examples out of training to test whether the result works on new wording. The later V2 challenger used a different starting model, DeBERTa, and a different evaluation corpus. Its score is not the live V1 demo’s score. Higher scores on different exams do not prove an improvement by themselves.

The photo branch uses pretrained OpenJev/DiffusionGemma on MLX. We did not fine-tune this model. **Multimodal** describes the complete application using multiple input types. It does not mean the text reader grew an image input.

## Why review is a real answer

Removing a photo of stairs does not remove the stairs. A photo with a pool does not prove pool entry is free. Unknowns stay unknown. The app preserves evidence links so you can inspect what affected each card.

## Where the code lives

| Piece | File inside apps/agency |
|---|---|
| HTTP request and result | travel_lab/serve.py |
| Traveller budget and policy rules | travel_lab/catalogue.py |
| Pixel input, observations and visual requirements | travel_lab/vision.py |
| Text model selection | travel_lab/active_model.py |
| Gallery and evidence UI | app/src/PhotoEvidence.tsx |
| Photo sets | config/location-photos.json |

The three active silent diagrams in apps/explainer/frames teach training versus use, image observations and rule combination. An older teaching composition is retained as source. They are explanatory animations, not recordings of model internals.


Continue with the [glossary](GLOSSARY.md), [architecture](ARCHITECTURE.md), [setup](SETUP.md) or [troubleshooting](TROUBLESHOOTING.md).
