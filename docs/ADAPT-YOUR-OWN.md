# Adapt one job at a time

Start with a task you can check yourself. “Route a support request to the right team” is narrower than “understand my business.”

## Write the contract before training

```yaml
question: Which team handles this request?
answers: [billing, technical_support, needs_review]
inputs: [request_text]
next_step: suggest_a_queue
```

Define what each answer means, including ambiguous cases. Have people who know the task label realistic examples. Keep an untouched test set. Split related templates/customers/documents together to avoid leaking near-copies into the test.

## Reuse the structure

1. Run the travel example before editing it.
2. Study the question format in apps/agency/config and training scripts in apps/agency/scripts.
3. Create your own labels, examples and task configuration in a new directory. Preserve the original travel experiment.
4. Train and choose settings on development examples. Do not edit the frozen travel engine files to make old scores look better.
5. Freeze your model and evaluate the untouched examples. Compare with a baseline on the same inputs.
6. Map results to application actions, with a review path. Measure mistakes as well as successes.

If images are useful, start by adapting the observation questions in travel_lab/vision.py. Its current six questions are fixed travel traits. A new trait needs a new question, validation, rule mapping and tests. Replacing a photo filename alone does not adapt the model.

Text-only inference and image inference can be used separately. The travel weights are not a ready-made specialist for a new domain. These support/product scenarios are design examples, not completed integrations.

## A useful first test

Take 20 examples you can personally judge. Run the system and inspect every error. This small smoke test helps reveal obvious mistakes; it is not a statistical reliability certificate. Expand evaluation before using results in consequential workflows.

## Work one example through the format

The explainer’s editable support scene downloads `my-support-examples.jsonl`. Each row has `id`, `text`, and your checked `label`. Convert it from the source-kit root:

```bash
python3 tools/prepare_task.py my-support-examples.jsonl --split train --out support-train.jsonl
```

This writes candidate-scoring records with `state`, a question, three candidates, labels and the correct label index. It refuses duplicate IDs, empty data, unsupported labels and existing output files. No model is trained by this conversion.

Collect separate development and untouched test files before training. Keep related customer conversations/templates in the same split; do not put copies of a training example in the test file. Use `--split dev` and `--split test` on those separate input files. The script records your chosen split; it cannot detect semantic leakage automatically.

For a working training path, place the three converted split files in a new data directory, then follow [STEP-BY-STEP](STEP-BY-STEP.md), using `tools/tutorial.py prepare --data path/to/your-data --run workshops/my-support-model`. The tutorial accepts three candidate sentences per question and saves a separate checkpoint. Create a new task configuration for the `route` question and these labels. The travel serving API and calibration rules have fixed travel assumptions; they need an adapter and task-specific evaluation. Preserve the travel experiment. Measure the pretrained baseline before training and compare both on identical held-out inputs. Review every mistake. The support editor and converter are working data-preparation tools, not a trained support integration.
