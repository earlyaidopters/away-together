# Final visual storyboard

Derived from the canonical filming guide. Each scene has its own evidence surface.

## 0:00-0:55: See how a photo changes the answer

Scene `#demo` at localhost:8770. Start with the live persona demo already visible. Deliver the Jev/local/images claim over the app. Run Maya with the stairs photo by 0:10; remove it and run again. Point at review by 0:25. Briefly show the full agency grid. If either request stalls, preserve real elapsed time and cut the wait transparently.

On-screen: See how a photo changes the answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Fresh /api/decide receipts; active V1 plus pretrained vision. Fictional travellers and photos. TypeSafe model documentation checked 21 September 2026: current Jev text-only input; our image support is a separate pretrained integration.

## 0:55-1:40: Follow the build from start to finish

Scene `#why` at localhost:8770. Trace the six steps. Open the full guide briefly, then return to the first step.

On-screen: Follow the build from start to finish.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: docs/STEP-BY-STEP.md; exact tutorial commands and retained app.

## 1:40-2:25: Start with an existing classifier

Scene `#choose-model` at localhost:8770. Open the actual model card. Point to owner, task, weights and pinned revision; use the card as a navigation surface, not a fabricated screenshot.

On-screen: Start with an existing classifier.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Pinned Hugging Face author model card; travel_lab/nli.py NLI_ID and NLI_REV.

## 2:25-3:10: Measure it before you train it

Scene `#baseline` at localhost:8770. Point at the before bar first, then after. Keep development and separate final-test caveat visible. Open the JSON receipt.

On-screen: Measure it before you train it.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: models/selection.json baseline_dev and dev; runs/nli-baseline-dev.json; historical final summary. 800 development judgments.

## 3:10-3:40: Check your computer first

Scene `#setup` at localhost:8770. Show tested M5 Max/128 GB host and separate text/image requirements. Open Start here prerequisites briefly.

On-screen: Check your computer first.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Inspected host, macOS 26.5.2; pinned vision launcher. No unsupported hardware promises.

## 3:40-4:25: Download the model to your computer

Scene `#download` at localhost:8770. Show the source repository in Codex, then run the download command in its terminal. Show actual printed revision and cache path. If cached, say so; do not stage a fresh download.

On-screen: Download the model to your computer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/tutorial.py download; live pinned snapshot_download receipt; docs/STEP-BY-STEP.md.

## 4:25-5:05: Tell Codex exactly what you want

Scene `#build` at localhost:8770. Point at each requirement before showing the full prompt. Keep Codex visibly open on the repository when filming.

On-screen: Tell Codex exactly what you want.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: prompts/TRAIN-MY-SPECIALIST.md; supplied travel hypotheses and task data.

## 5:05-5:50: Write the rules for your travel job

Scene `#travel-brief` at localhost:8770. Underline the label contract and four definitions one by one while explaining. These are real travel requirements from the current model.

On-screen: Write the rules for your travel job.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: travel_lab/nli.py HYPOTHESES; traveller requirements; text/image separation.

## 5:50-6:45: Give Codex the complete brief

Scene `#prompt` at localhost:8770. Click Job, Data, Training and Final test tabs. Open the complete prompt page and show that the download has all eight sections. Underlines identify editable task fields.

On-screen: Give Codex the complete brief.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Exact downloadable eight-part prompt; prepared specification, not historical chat.

## 6:45-7:15: Give it three choices

Scene `#labels` at localhost:8770. Click Cash back, then Hotel credit. Point to the mapping between the teaching labels and actual output labels.

On-screen: Give it three choices.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Teaching exercise; actual NLI labels in data/train.jsonl. Fixed format is not a deterministic-output claim.

## 7:15-7:50: Pair each example with an answer

Scene `#training` at localhost:8770. Open actual train-00000 excerpt. Download the full record. Point at input, question, answer; show the separate held-out file only as data provenance.

On-screen: Pair each example with an answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: assets/training-example.json exact data/train.jsonl record; synthetic, no human labels.

## 7:50-8:30: Keep three separate sets of examples

Scene `#data-split` at localhost:8770. Show three real data files. Point at scenario ID and template family in source records. Do not inspect final answer errors until the model is frozen.

On-screen: Keep three separate sets of examples.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Tutorial prepare validation; travel data provenance and split design.

## 8:30-9:15: Train in a separate working folder

Scene `#workspace` at localhost:8770. Run prepare in the repository root; show created data folder and manifest. Demonstrate that a second prepare refuses the existing folder.

On-screen: Train in a separate working folder.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/tutorial.py prepare; exclusive directory and data hash checks.

## 9:15-9:45: Train it using checked examples

Scene `#practice` at localhost:8770. Play the two-lane HyperFrame. Hold at the wrong guess, checked label and saved-settings update. Point to unchanged settings in the normal-check lane.

On-screen: Train it using checked examples.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Training code and saved checkpoints. Diagram is conceptual, not a measured individual training step.

## 9:45-10:35: Run the baseline, then start training

Scene `#train-run` at localhost:8770. Show real baseline receipt, actual epoch log and saved checkpoint files from the verified tutorial run. Clearly label eight-decision smoke check; do not present it as the historical full training run.

On-screen: Run the baseline, then start training.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/tutorial.py actual baseline, training, checkpoint and freeze outputs. New tutorial recipe differs from historical accumulation recipe.

## 10:35-11:05: Test it on examples it hasn't seen

Scene `#test` at localhost:8770. Show practice and final-test objects. Open the held-out example and explain its split, then return to the diagram.

On-screen: Test it on examples it hasn't seen.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Frozen V2 protocol; 52 document repairs; two writer-assisted adjudications; hashes. V1 held-out download is labeled separately.

## 11:05-11:50: Compare both models on the same test

Scene `#test-run` at localhost:8770. Execute the small verification test if needed; open its saved report. Show rows for both models on the same IDs. Then use historical full-study failure in next scene.

On-screen: Compare both models on the same test.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/tutorial.py test; paired rows, frozen model and data hash enforcement.

## 11:50-12:20: Look at an answer it got wrong

Scene `#failure` at localhost:8770. Show case …0036 arrival excerpt and both saved outputs. Open full JSON to show the input is longer than the excerpt.

On-screen: Look at an answer it got wrong.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: assets/benchmark-case.json; raw frozen local and Jev rows for round1-deeper-fp16-0036, arrival.

## 12:20-12:50: Compare its answers with Jev's

Scene `#results` at localhost:8770. Show common-axis bars; point to text-only scope and distinguish demo V1 from later V2. Do not animate a V1→V2 improvement arrow.

On-screen: Compare its answers with Jev's.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: FROZEN-V2-RESULTS.md; qualification-decision.json; V1 summary. No model or final-test changes.

## 12:50-13:35: Try your saved model on new text

Scene `#predict` at localhost:8770. Download the actual input, run predict, read its returned sentence. Change cash refund to hotel credit and explain the expected change without guaranteeing it.

On-screen: Try your saved model on new text.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/tutorial.py predict; downloadable JSON; actual smoke prediction receipt.

## 13:35-14:05: Connect the models with code

Scene `#map` at localhost:8770. Point to text reader, pretrained photo reader and app rules in order; keep Maya visible when returning to the agency.

On-screen: Connect the models with code.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: travel_lab/vision.py; catalogue.py; active selection.json.

## 14:05-14:40: Add a model that reads images

Scene `#vision` at localhost:8770. Play photo→observation→app. Open photo-lab.html, choose a local image, run it and inspect actual answers and image hash. Keep the service running before filming.

On-screen: Add a model that reads images.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Fresh /api/observe receipt; fixed loopback endpoint; pretrained DiffusionGemma. Generated fictional catalogue photos.

## 14:40-15:10: Check what the photo can tell you

Scene `#boundary` at localhost:8770. Show pond, ask the three questions and reveal the conclusion. Refer back to the missing stairs photo.

On-screen: Check what the photo can tell you.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Generated-image ledger; location-photos.json; image evidence limitations.

## 15:10-15:40: Check each person's requirements

Scene `#rules` at localhost:8770. Play budget/terms/photo gates. In the actual agency open a traveller drawer and show the clause/photo that caused decline or review.

On-screen: Check each person's requirements.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: catalogue.verdict; apply_visual_requirements; live reason drawer; companion local API example.

## 15:40-16:20: Run it before changing it

Scene `#first-run` at localhost:8770. Open Start here. Show source and restored files, run first_run.py, start agency in a spare terminal if needed, inspect service status and run a fresh holiday. No fake installation animation.

On-screen: Run it before changing it.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/first_run.py, tools/restore_companion.py, docs/SETUP.md and live /api/status. Public access separately gated.

## 16:20-16:50: Work out what it costs to run

Scene `#cost` at localhost:8770. Show build/setup and local-running cost columns, then separately labeled historical timings. Point to fresh demo time rather than implying benchmark-equivalent workloads.

On-screen: Work out what it costs to run.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Historical V1 HTTP timing receipts and photo integration scan; no measured total-cost ratio.

## 16:50-17:25: Change one example yourself

Scene `#repurpose` at localhost:8770. Edit support request, choose its human label, add it and download JSONL. Run prepare_task.py on the saved sample. Show held-out separation in the adaptation guide.

On-screen: Change one example yourself.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Real JSONL export; tools/prepare_task.py; docs/ADAPT-YOUR-OWN.md. No completed support-model claim.

## 17:25-18:05: Keep the files that let you run it again

Scene `#handover` at localhost:8770. Show the actual workshop file tree and the README/prompt folder. Explain which files a different domain changes.

On-screen: Keep the files that let you run it again.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: docs/STEP-BY-STEP.md; eight-part prompt completion contract; tutorial output files.

## 18:05-18:40: Start with a working example

Scene `#take-it` at localhost:8770. Open Start here and the question index. Show current access/permission status accurately; use only the delivered link once verified. Keep original creator/model credits visible.

On-screen: Start with a working example.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: One repository stays private until the video goes live. Verify signed-out source and model-download access before adding the description link. Original-code reuse terms still need a decision. Retain all upstream credits.
