# Build it with Claude or Codex

Use a coding assistant that can work with local files. Give it the prompt and link for each step. Ask it to execute the model and show its output.

## 1. Choose the starting model

```text
Look at this classifier and explain whether it fits my task. Check what it can do and what I need to run it.

https://huggingface.co/MoritzLaurer/ModernBERT-base-zeroshot-v2.0
```

What you should get: A model choice and explanation.

## 2. Download and try it

```text
Download the linked model to my computer. Check my hardware, install what is missing, and run one example. Keep the exact version.

https://huggingface.co/MoritzLaurer/ModernBERT-base-zeroshot-v2.0
```

What you should get: The exact model version and one real example.

## 3. Define your task

```text
Help me define [my task]. My input is [what it reads]. My possible answers are [the labels]. Show me five examples, including one you cannot answer.

https://github.com/earlyaidopters/away-together
```

What you should get: A task definition you can check.

## 4. Give it the complete brief

```text
Use the full specialist prompt below. Replace the bracketed task fields and walk me through every checkpoint.

https://github.com/earlyaidopters/away-together
```

What you should get: The full job, data, training and testing plan.

## 5. Check the examples

```text
Show the text, question and checked answer for each example. Flag unclear labels and keep synthetic examples identified.

https://github.com/earlyaidopters/away-together
```

What you should get: Examples whose answers you understand.

## 6. Separate your test

```text
Split the examples into practice, development and final test. Keep related documents together and keep the final test closed.

https://github.com/earlyaidopters/away-together
```

What you should get: Three separate groups with no exact overlap.

## 7. Train your specialist

```text
Test the original classifier first. Use my checked examples to run a small training check, then train in a separate folder and save the best version. Keep final-test examples out of training, and show me the results and files.

https://github.com/earlyaidopters/away-together
```

What you should get: A saved model and its development results.

## 8. Compare on unseen examples

```text
Compare my trained model and the original on the same untouched examples. Show both sets of answers, the scores and every mistake. Keep the report even if the specialist loses.

https://github.com/earlyaidopters/away-together
```

What you should get: Both models’ predictions and all mistakes.

## 9. Try a new input

```text
Load my saved model and run a new example. Show its selected answer. Change the example and run the model again; do not answer it yourself.

https://github.com/earlyaidopters/away-together
```

What you should get: A real result from your saved model.

## 10. Run the supplied app

```text
Set up this repo locally with the supplied weights, launch the travel app and help me check one holiday.

https://github.com/earlyaidopters/away-together
```

What you should get: The live agency in your browser.

## 11. Add the image model

```text
Connect the included pretrained image service if my machine supports it. Show the picture, the visual questions, its answers and how the app uses them.

https://github.com/earlyaidopters/away-together
```

What you should get: Photo observations connected to traveller requirements.

## 12. Adapt and keep your work

```text
Help me adapt this to [my task]. Keep the model version, examples, training settings, saved model and test results together. Write a guide so I can run it again.

https://github.com/earlyaidopters/away-together
```

What you should get: An understandable project and its limitations.

See [the technical reference](STEP-BY-STEP.md) for commands, prerequisites and troubleshooting.
