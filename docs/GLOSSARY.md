# Terms you can understand without studying machine learning

| Term | Plain meaning | In this project |
|---|---|---|
| Classifier | A system that chooses from a list of answers | Meets, violates, or insufficient evidence |
| Label | The answer attached to an example | A policy explicitly refusing cash refunds violates a cash-refund requirement |
| Pretrained model | A model that learned patterns before this project | ModernBERT is the starting text reader |
| Weights | Saved numbers that determine how a model behaves | Downloaded/restored files, separate from the app code |
| Fine-tuning | Changing those numbers through extra practice | Training on labeled travel examples |
| Prompt | Instructions and information for one request | Asking whether entrance stairs are visible |
| Inference | Using the saved model to answer a new request | Checking a holiday; this does not retrain it |
| NLI | Checking whether text supports, contradicts or leaves a statement unresolved | Does this policy support a full cash refund? |
| Train / development / test | Practice examples / examples for choosing settings / the final exam | Keep related documents together so near-copies do not cross splits |
| Checkpoint | A saved version of a model | Active V1 and frozen V2 are different checkpoints |
| Freeze | Stop changing the contestant before testing it | Model, settings and inputs have recorded hashes |
| Multimodal | Using more than one kind of input | The app combines text judgments with photo observations |
| API | A way for one program to request something from another | POST /api/decide returns a structured decision |
| Endpoint / port | A named service address / a numbered local service entrance | Agency on 8765; vision on 8081; explainer on 8770 |
| JSON / JSONL | Structured data / one structured record per line | API replies / exported labeled examples |
| Confidence | A model score, not necessarily a reliable probability | The image threshold is a heuristic, not a guarantee |
| Synthetic data | Examples created for the experiment | These are not verified real-hotel facts |
| Benchmark | A defined test with specified inputs and scoring | The text-only V2 comparison is not vision accuracy |
| Hash | A fingerprint that detects changed file contents | Restore verifies files before writing them |

You can follow the walkthrough without memorizing these terms. Start with [the everyday explanation](HOW-IT-WORKS.md), then use this page when an unfamiliar word appears.
