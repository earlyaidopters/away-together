# Final visual storyboard

Derived from the canonical filming guide. Each scene has its own evidence surface.

## 0:00-0:50: See how a photo changes the answer

Scene `#demo` at localhost:8770. Start with the live persona demo already visible. Deliver the Jev/local/images claim over the app. Run Maya with the stairs photo by 0:10; remove it and run again. Point at review by 0:25. Briefly show the full agency grid. If either request stalls, preserve real elapsed time and cut the wait transparently.

On-screen: See how a photo changes the answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Fresh /api/decide receipts; active V1 plus pretrained vision. Fictional travellers and photos.

## 0:50-1:20: Pick a job you keep repeating

Scene `#why` at localhost:8770. Follow holiday input → a small decision → a person checking the reason. Point at the review branch.

On-screen: Pick a job you keep repeating.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Task-selection guidance; no universal price or quality claim.

## 1:20-1:50: Ask AI to help you build it

Scene `#build` at localhost:8770. Show the exact prepared specification excerpt, then the saved source and model folders. Identify it as a prepared specification, not a captured chat.

On-screen: Ask AI to help you build it.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: production/ASTRA-BUILD-PROMPT.md; saved source/checkpoint manifests; THIRD-PARTY-NOTICES.md.

## 1:50-2:20: Connect the models with code

Scene `#map` at localhost:8770. Point to text reader, pretrained photo reader and app rules in order; keep Maya visible when returning to the agency.

On-screen: Connect the models with code.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: travel_lab/vision.py; catalogue.py; active selection.json.

## 2:20-2:50: Give it three choices

Scene `#labels` at localhost:8770. Click Cash back, then Hotel credit. Point to the mapping between the teaching labels and actual output labels.

On-screen: Give it three choices.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Teaching exercise; actual NLI labels in data/train.jsonl. Fixed format is not a deterministic-output claim.

## 2:50-3:25: Pair each example with an answer

Scene `#training` at localhost:8770. Open actual train-00000 excerpt. Download the full record. Point at input, question, answer; show the separate held-out file only as data provenance.

On-screen: Pair each example with an answer.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: assets/training-example.json exact data/train.jsonl record; synthetic, no human labels.

## 3:25-3:55: Train it using checked examples

Scene `#practice` at localhost:8770. Play the two-lane HyperFrame. Hold at the wrong guess, checked label and saved-settings update. Point to unchanged settings in the normal-check lane.

On-screen: Train it using checked examples.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Training code and saved checkpoints. Diagram is conceptual, not a measured individual training step.

## 3:55-4:25: Test it on examples it hasn't seen

Scene `#test` at localhost:8770. Show practice and final-test objects. Open the held-out example and explain its split, then return to the diagram.

On-screen: Test it on examples it hasn't seen.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Frozen V2 protocol; 52 document repairs; two writer-assisted adjudications; hashes. V1 held-out download is labeled separately.

## 4:25-4:55: Look at an answer it got wrong

Scene `#failure` at localhost:8770. Show case …0036 arrival excerpt and both saved outputs. Open full JSON to show the input is longer than the excerpt.

On-screen: Look at an answer it got wrong.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: assets/benchmark-case.json; raw frozen local and Jev rows for round1-deeper-fp16-0036, arrival.

## 4:55-5:25: Compare its answers with Jev's

Scene `#results` at localhost:8770. Show common-axis bars; point to text-only scope and distinguish demo V1 from later V2. Do not animate a V1→V2 improvement arrow.

On-screen: Compare its answers with Jev's.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: FROZEN-V2-RESULTS.md; qualification-decision.json; V1 summary. No model or final-test changes.

## 5:25-6:00: Add a model that reads images

Scene `#vision` at localhost:8770. Play photo→observation→app. Open photo-lab.html, choose a local image, run it and inspect actual answers and image hash. Keep the service running before filming.

On-screen: Add a model that reads images.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Fresh /api/observe receipt; fixed loopback endpoint; pretrained DiffusionGemma. Generated fictional catalogue photos.

## 6:00-6:30: Check what the photo can tell you

Scene `#boundary` at localhost:8770. Show pond, ask the three questions and reveal the conclusion. Refer back to the missing stairs photo.

On-screen: Check what the photo can tell you.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Generated-image ledger; location-photos.json; image evidence limitations.

## 6:30-7:00: Check each person's requirements

Scene `#rules` at localhost:8770. Play budget/terms/photo gates. In the actual agency open a traveller drawer and show the clause/photo that caused decline or review.

On-screen: Check each person's requirements.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: catalogue.verdict; apply_visual_requirements; live reason drawer; companion local API example.

## 7:00-7:30: Check your computer first

Scene `#setup` at localhost:8770. Show tested M5 Max/128 GB host and separate text/image requirements. Open Start here prerequisites briefly.

On-screen: Check your computer first.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Inspected host, macOS 26.5.2; pinned vision launcher. No unsupported hardware promises.

## 7:30-8:10: Run it before changing it

Scene `#first-run` at localhost:8770. Open Start here. Show source and restored files, run first_run.py, start agency in a spare terminal if needed, inspect service status and run a fresh holiday. No fake installation animation.

On-screen: Run it before changing it.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: tools/first_run.py, tools/restore_companion.py, docs/SETUP.md and live /api/status. Public access separately gated.

## 8:10-8:40: Work out what it costs to run

Scene `#cost` at localhost:8770. Show build/setup and local-running cost columns, then separately labeled historical timings. Point to fresh demo time rather than implying benchmark-equivalent workloads.

On-screen: Work out what it costs to run.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Historical V1 HTTP timing receipts and photo integration scan; no measured total-cost ratio.

## 8:40-9:15: Change one example yourself

Scene `#repurpose` at localhost:8770. Edit support request, choose its human label, add it and download JSONL. Run prepare_task.py on the saved sample. Show held-out separation in the adaptation guide.

On-screen: Change one example yourself.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: Real JSONL export; tools/prepare_task.py; docs/ADAPT-YOUR-OWN.md. No completed support-model claim.

## 9:15-9:45: Start with a working example

Scene `#take-it` at localhost:8770. Open Start here and the question index. Show current access/permission status accurately; use only the delivered link once verified. Keep original creator/model credits visible.

On-screen: Start with a working example.

Editing: Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

Evidence: One repository stays private until the video goes live. Verify signed-out source and model-download access before adding the description link. Original-code reuse terms still need a decision. Retain all upstream credits.
