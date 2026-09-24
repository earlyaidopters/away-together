# Final visual storyboard

Derived from the canonical filming guide. Each scene has its own evidence surface.

## 0:00-1:05: See how a photo changes the answer

Scene `#demo` at localhost:8770. Start with the live persona demo already visible. In the full agency, select The flexible escape · 2 (offer 10 of 40); the #demo scene already uses it. Deliver the Jev/local/images claim over the app. Run Maya with the stairs photo by 0:10; remove it and run again. Point at review by 0:25. Briefly show the full agency grid. If either request stalls, preserve real elapsed time and cut the wait transparently.

On-screen: See how a photo changes the answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Fresh /api/decide receipts; active V2 text model (models/active-model.json, app rule) plus pretrained vision. Fictional travellers and photos. TypeSafe model documentation checked 21 September 2026: current Jev text-only input; our image support is a separate pretrained integration. Opus 5.5 line (22 Sep 2026 session only): same-test accuracy 60.28% to 95.28% (experiments/v3/runs/v1-vs-v2-round1.json); first check after restart 8.5 s to about 0.12 s via startup warm-up; photo false alarms 10 to 4 on a held-out set (experiments/v3/vision/holdout). The original build was done with Codex; do not say Opus built it.

## 1:05-2:05: Build it one step at a time

Scene `#why` at localhost:8770. Point to the four-stage visual path.

On-screen: Build it one step at a time.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: docs/STEP-BY-STEP.md; exact tutorial commands and retained app.

## 2:05-2:50: Start with a model that can classify text

Scene `#choose-model` at localhost:8770. Open the actual model card. Point to owner, task, weights and pinned revision; use the card as a navigation surface, not a fabricated screenshot.

On-screen: Start with a model that can classify text.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Pinned Hugging Face author model card; travel_lab/nli.py NLI_ID and NLI_REV.

## 2:50-3:35: Measure it before you train it

Scene `#baseline` at localhost:8770. Point at the before bar first, then after. Keep development and separate final-test caveat visible. Open the JSON receipt.

On-screen: Measure it before you train it.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: models/selection.json baseline_dev and dev; runs/nli-baseline-dev.json; historical final summary. 800 development judgments.

## 3:35-4:20: Ask AI to get it running

Scene `#download` at localhost:8770. Copy the setup prompt and repository link into Claude Code. Explain the file-to-computer animation, then open the actual agency after setup. The starting model link is available beside the prompt.

On-screen: Ask AI to get it running.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: tools/tutorial.py download; live pinned snapshot_download receipt; docs/STEP-BY-STEP.md. tools/first_run.py; docs/SETUP.md; supplied model versus new tutorial checkpoint.

## 4:20-5:10: Tell it the job you want done

Scene `#build` at localhost:8770. Show the holiday, booking terms and Maya beside the brief. Walk through its four concrete requirements.

On-screen: Tell it the job you want done.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: prompts/TRAIN-MY-SPECIALIST.md; supplied travel hypotheses and task data. travel_lab/nli.py HYPOTHESES; separate visual requirements.

## 5:10-6:05: Give Claude the complete brief

Scene `#prompt` at localhost:8770. Click Job, Data, Training and Final test tabs. Open the complete prompt page and show that the download has all eight sections. Underlines identify editable task fields.

On-screen: Give Claude the complete brief.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Exact downloadable eight-part prompt; prepared specification, not historical chat.

## 6:05-6:35: Give it three choices

Scene `#labels` at localhost:8770. Click Cash back, then Hotel credit. Point to the mapping between the teaching labels and actual output labels.

On-screen: Give it three choices.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Teaching exercise; actual NLI labels in data/train.jsonl. Fixed format is not a deterministic-output claim.

## 6:35-7:10: Pair each example with an answer

Scene `#training` at localhost:8770. Open actual train-00000 excerpt. Download the full record. Point at input, question, answer; show the separate held-out file only as data provenance.

On-screen: Pair each example with an answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: assets/training-example.json exact data/train.jsonl record; synthetic, no human labels.

## 7:10-7:45: Keep some examples for the final test

Scene `#data-split` at localhost:8770. Play the practice, settings and sealed-test folders appearing in order.

On-screen: Keep some examples for the final test.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Tutorial prepare validation; travel data provenance and split design.

## 7:45-8:20: Train it using checked examples

Scene `#practice` at localhost:8770. Play the existing training animation. Copy the training prompt below it when moving to execution.

On-screen: Train it using checked examples.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Training code and saved checkpoints. Diagram is conceptual, not a measured individual training step.

## 8:20-8:55: Test it on examples it hasn’t seen

Scene `#test` at localhost:8770. Play identical unseen examples flowing to both models. Copy the test prompt.

On-screen: Test it on examples it hasn’t seen.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Frozen V2 protocol; 52 document repairs; two writer-assisted adjudications; hashes. V1 held-out download is labeled separately.

## 8:55-9:25: Look at an answer it got wrong

Scene `#failure` at localhost:8770. Show case …0036 arrival excerpt and both saved outputs. Open full JSON to show the input is longer than the excerpt.

On-screen: Look at an answer it got wrong.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: assets/benchmark-case.json; raw frozen local and Jev rows for round1-deeper-fp16-0036, arrival.

## 9:25-9:55: Compare its answers with Jev's

Scene `#results` at localhost:8770. Show three common-axis bars from the same 360 fresh scenarios: first model 60.28%, V2 95.28%, Jev 98.61%. Point to text-only scope. The first-model bar is a same-test comparison; its separate 66.5% test stays out of this chart.

On-screen: Compare its answers with Jev's.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: FROZEN-V2-RESULTS.md; qualification-decision.json; experiments/v3/runs/v1-vs-v2-round1.json (both models frozen before the corpus, no tuning); models/active-model.json basis app-quality-gates.

## 9:55-10:35: Ask it to try a new policy

Scene `#predict` at localhost:8770. Show the cancellation letter and prompt. Paste into a coding assistant for actual saved-model inference; do not substitute the assistant's own answer.

On-screen: Ask it to try a new policy.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: tools/tutorial.py predict; downloadable JSON; actual smoke prediction receipt.

## 10:35-11:05: Connect the models with code

Scene `#map` at localhost:8770. Point to text reader, pretrained photo reader and app rules in order; keep Maya visible when returning to the agency.

On-screen: Connect the models with code.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: travel_lab/vision.py; catalogue.py; active selection.json.

## 11:05-11:45: Show how a picture becomes evidence

Scene `#vision` at localhost:8770. Play photo, pixel grid, feature answers and Maya's requirement in order. The grid illustrates pixel input, not an exact architecture trace. Open photo lab for fresh inference.

On-screen: Show how a picture becomes evidence.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Fresh /api/observe receipt; fixed loopback endpoint; pretrained DiffusionGemma. Generated fictional catalogue photos.

## 11:45-12:15: Check what the photo can tell you

Scene `#boundary` at localhost:8770. Show pond, ask the three questions and reveal the conclusion. Refer back to the missing stairs photo.

On-screen: Check what the photo can tell you.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Generated-image ledger; location-photos.json; image evidence limitations.

## 12:15-12:45: Check each person's requirements

Scene `#rules` at localhost:8770. Play budget/terms/photo gates. In the actual agency open a traveller drawer and show the clause/photo that caused decline or review.

On-screen: Check each person's requirements.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: catalogue.verdict; apply_visual_requirements; live reason drawer; companion local API example.

## 12:45-13:20: See where the costs come from

Scene `#cost` at localhost:8770. Animate the build receipt, local computer and per-check model API fee. No fabricated total or savings percentage.

On-screen: See where the costs come from.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: V2 app timing receipts (experiments/v3/runs/v1-vs-v2-round1.json) and photo integration scan; no measured total-cost ratio.

## 13:20-13:55: Change one example yourself

Scene `#repurpose` at localhost:8770. Edit support request, choose its human label, add it and download JSONL. Run prepare_task.py on the saved sample. Show held-out separation in the adaptation guide.

On-screen: Change one example yourself.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: Real JSONL export; tools/prepare_task.py; docs/ADAPT-YOUR-OWN.md. No completed support-model claim.

## 13:55-14:15: Take the project and make it yours

Scene `#take-it` at localhost:8770. Show the source kit and repository link. End without repeating setup or training steps.

On-screen: Take the project and make it yours.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Copy prompts into a coding assistant with local tools. When showing execution, keep actual results and disclose cut waiting time. Use the 1×, 1.5× or 2× controls for explanatory diagrams.

Evidence: One repository stays private until the video goes live. Verify signed-out source and model-download access before adding the description link. Original-code reuse terms still need a decision. Retain all upstream credits.
