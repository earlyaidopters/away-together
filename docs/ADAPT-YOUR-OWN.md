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
