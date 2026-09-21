# Build your own decision system

Transcript-informed 5–10 minute revision. Eighteen filming surfaces. Exact Say blocks; companion holds deeper setup and troubleshooting. No TTS requested.

## Watch the photo change it (0:00-0:50)

**Picture:**
Scene `#demo` at localhost:8770. Start with the live persona demo already visible. Deliver the Jev/local/images claim over the app. Run Maya with the stairs photo by 0:10; remove it and run again. Point at review by 0:25. Briefly show the full agency grid. If either request stalls, preserve real elapsed time and cut the wait transparently.

**Say:**
I took the idea behind Jev and built a local version for this travel job. And I added image understanding. Watch Maya. The terms fit what she wants, but this photo shows entrance stairs. Her card turns red. Remove the photo, check again, and it asks us to review. It knows less. This runs on my computer. Mine checks holidays. Yours could check a job you repeat every day. I'll show you how the pieces work and how to run my example, even if you've never trained a model.

**On-screen copy:**
Watch the photo change it.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Fresh /api/decide receipts; active V1 plus pretrained vision. Fictional travellers and photos.

**Re-hook:**


## Give one job a home (0:50-1:20)

**Picture:**
Scene `#why` at localhost:8770. Follow holiday input → a small decision → a person checking the reason. Point at the review branch.

**Say:**
Say you keep asking AI whether a policy fits what a customer wants. You can give that check a home inside your app. It reads the evidence, picks an answer, and shows you why. That's the idea we're borrowing from Jev. You choose the job and the possible answers. Start with ordinary rules and an existing model. Training takes work, so test whether you need it.

**On-screen copy:**
Give one job a home.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Task-selection guidance; no universal price or quality claim.

**Re-hook:**


## Astra helped build the system (1:20-1:50)

**Picture:**
Scene `#build` at localhost:8770. Show the exact prepared specification excerpt, then the saved source and model folders. Identify it as a prepared specification, not a captured chat.

**Say:**
I asked Astra to help build the travel system, train it and test it. This is the specification. There were follow-ups, fixes and multiple experiments. Once built, the saved models answer these holiday questions without calling Astra. I put the task, app and experiments together. Other people built the foundation models and OpenJev. You'll find their credits in the project.

**On-screen copy:**
Astra helped build the system.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
production/ASTRA-BUILD-PROMPT.md; saved source/checkpoint manifests; THIRD-PARTY-NOTICES.md.

**Re-hook:**


## Three parts. One decision (1:50-2:20)

**Picture:**
Scene `#map` at localhost:8770. Point to text reader, pretrained photo reader and app rules in order; keep Maya visible when returning to the agency.

**Say:**
There are three pieces. A model reads the terms. Another looks at the pictures. Code checks those answers against Maya's wishes and budget. I trained the text reader for travel and connected an already trained image reader. Multimodal means we're using words and pictures. Price comparisons stay in ordinary code. You don't need AI to tell you whether twelve hundred is more than a thousand.

**On-screen copy:**
Three parts. One decision.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
travel_lab/vision.py; catalogue.py; active selection.json.

**Re-hook:**


## Give it three choices (2:20-2:50)

**Picture:**
Scene `#labels` at localhost:8770. Click Cash back, then Hotel credit. Point to the mapping between the teaching labels and actual output labels.

**Say:**
This policy offers hotel credit. Maya wants a cash refund, so it fails her requirement. A clear cash refund passes. If the policy doesn't say, we can't tell. Those are our three labels. A classifier picks a label. That gives our app a short answer it can use. It can still pick the wrong one.

**On-screen copy:**
Give it three choices.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Teaching exercise; actual NLI labels in data/train.jsonl. Fixed format is not a deterministic-output claim.

**Re-hook:**


## An example has three parts (2:50-3:25)

**Picture:**
Scene `#training` at localhost:8770. Open actual train-00000 excerpt. Download the full record. Point at input, question, answer; show the separate held-out file only as data provenance.

**Say:**
We started with ModernBERT, a model that already understands language patterns. To make it better at this job, we gave it travel examples. Each has three parts. What it reads, what we ask, and the checked answer. This actual record says to contact the booking office. So we can't establish the refund rule. Our examples are made up. For your job, check the labels carefully. Wrong answers teach the wrong lesson.

**On-screen copy:**
An example has three parts.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
assets/training-example.json exact data/train.jsonl record; synthetic, no human labels.

**Re-hook:**


## Practice. Check. Adjust (3:25-3:55)

**Picture:**
Scene `#practice` at localhost:8770. Play the two-lane HyperFrame. Hold at the wrong guess, checked label and saved-settings update. Point to unchanged settings in the normal-check lane.

**Say:**
The model guesses. Training compares that guess with the label and adjusts its saved settings. Repeat with more examples. That's fine-tuning. A prompt gives instructions for a request. Training changes what's saved. Clicking Check in our app uses that saved model; it doesn't train it again. And I've included the travel weights, which are those saved settings, so you can start by running the example.

**On-screen copy:**
Practice. Check. Adjust.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Training code and saved checkpoints. Diagram is conceptual, not a measured individual training step.

**Re-hook:**


## Keep the exam sealed (3:55-4:25)

**Picture:**
Scene `#test` at localhost:8770. Show practice and final-test objects. Open the held-out example and explain its split, then return to the diagram.

**Say:**
Keep some examples out of training, like an exam the model hasn't practised. Keep related documents together when splitting them. Our later test used made-up cases with agent-reviewed answers, including repairs and disputed answers. There was no human validation. We froze the model before scoring it. Once you inspect those mistakes, you need fresh cases for your next final test.

**On-screen copy:**
Keep the exam sealed.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Frozen V2 protocol; 52 document repairs; two writer-assisted adjudications; hashes. V1 held-out download is labeled separately.

**Re-hook:**


## Inspect one real mistake (4:25-4:55)

**Picture:**
Scene `#failure` at localhost:8770. Show case …0036 arrival excerpt and both saved outputs. Open full JSON to show the input is longer than the excerpt.

**Say:**
Here's a real mistake from that test. Arrival at one thirty in the morning is allowed without calling ahead. The reference says yes. Jev says yes. My later model says it can't tell. That sends a clear case to unnecessary review. Both received the same full document. We're looking at an excerpt. This is why I want you to inspect the mistakes too.

**On-screen copy:**
Inspect one real mistake.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
assets/benchmark-case.json; raw frozen local and Jev rows for round1-deeper-fp16-0036, arrival.

**Re-hook:**


## The test kept us honest (4:55-5:25)

**Picture:**
Scene `#results` at localhost:8770. Show common-axis bars; point to text-only scope and distinguish demo V1 from later V2. Do not animate a V1→V2 improvement arrow.

**Say:**
That later model matched our references about ninety-five percent of the time. Jev was closer to ninety-nine. I didn't beat Jev. It failed our promotion rule, so the demo still uses the earlier model. That one scored sixty-six point five on a different test. These aren't comparable improvement scores. And this chart tests text, not picture understanding. We built the workflow. Its reliability still needs work.

**On-screen copy:**
The test kept us honest.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
FROZEN-V2-RESULTS.md; qualification-decision.json; V1 summary. No model or final-test changes.

**Re-hook:**


## Give the system eyes (5:25-6:00)

**Picture:**
Scene `#vision` at localhost:8770. Play photo→observation→app. Open photo-lab.html, choose a local image, run it and inspect actual answers and image hash. Keep the service running before filming.

**Say:**
Now give the system eyes. This pretrained reader looks at the actual pixels and answers questions about visible features. I connected it through OpenJev. Pick a PNG or JPEG in the photo lab and run it on this computer. We send the picture, without its filename or an expected answer. This model reads pictures. The holiday illustrations were created separately.

**On-screen copy:**
Give the system eyes.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Fresh /api/observe receipt; fixed loopback endpoint; pretrained DiffusionGemma. Generated fictional catalogue photos.

**Re-hook:**


## A picture leaves things out (6:00-6:30)

**Picture:**
Scene `#boundary` at localhost:8770. Show pond, ask the three questions and reveal the conclusion. Refer back to the missing stairs photo.

**Say:**
There's water here, but that doesn't establish a swimming pool. Even a pool photo can't tell us whether access costs extra. Pictures show visible features. Terms tell us what's promised. Our forty offers share nine fictional images, so this isn't a test of forty real hotels. And removing Maya's stairs photo never proves the entrance is accessible.

**On-screen copy:**
A picture leaves things out.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Generated-image ledger; location-photos.json; image evidence limitations.

**Re-hook:**


## The app makes the call (6:30-7:00)

**Picture:**
Scene `#rules` at localhost:8770. Play budget/terms/photo gates. In the actual agency open a traveller drawer and show the clause/photo that caused decline or review.

**Say:**
The app combines the checks. Budget passes. Terms pass. Stairs fail, so Maya gets a decline. Missing evidence goes to review unless another requirement already fails. Open her card and inspect the reason. A green card means these checks passed according to our models. A person still confirms the booking details. The app doesn't book anything.

**On-screen copy:**
The app makes the call.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
catalogue.verdict; apply_visual_requirements; live reason drawer; companion local API example.

**Re-hook:**


## Check your computer first (7:00-7:30)

**Picture:**
Scene `#setup` at localhost:8770. Show tested M5 Max/128 GB host and separate text/image requirements. Open Start here prerequisites briefly.

**Say:**
Check your computer before downloading. I used an M5 Max with a hundred and twenty-eight gigabytes of memory. That's the tested machine, not a minimum. The supplied image setup needs Apple silicon and about sixteen gigabytes of model downloads. That's disk space, not a RAM requirement. Smaller machines and Windows or Linux image setups aren't validated here. Text and pictures have separate setup steps.

**On-screen copy:**
Check your computer first.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Inspected host, macOS 26.5.2; pinned vision launcher. No unsupported hardware promises.

**Re-hook:**


## Run it before changing it (7:30-8:10)

**Picture:**
Scene `#first-run` at localhost:8770. Open Start here. Show source and restored files, run first_run.py, start agency in a spare terminal if needed, inspect service status and run a fresh holiday. No fake installation animation.

**Say:**
Open Start here. Get the source and matching model archive, then install the listed tools. Run the first-run check to see what's missing. Start the text service, open the app, and add the photo service when ready. The commands are copyable. Check a holiday yourself. Leave the services running; after sleep, check them again. If they're unavailable, the page tells you instead of showing an old answer.

**On-screen copy:**
Run it before changing it.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
tools/first_run.py, tools/restore_companion.py, docs/SETUP.md and live /api/status. Public access separately gated.

**Re-hook:**


## Count the whole bill (8:10-8:40)

**Picture:**
Scene `#cost` at localhost:8770. Show build/setup and local-running cost columns, then separately labeled historical timings. Point to fresh demo time rather than implying benchmark-equivalent workloads.

**Say:**
These local checks don't create a model-provider API bill. You still have hardware, electricity, setup and maintenance. Building and training can cost money too. I haven't measured the whole bill or proved a fixed saving. These timings cover different jobs, so compare the same workload on your computer before deciding whether this approach pays off.

**On-screen copy:**
Count the whole bill.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Historical V1 HTTP timing receipts and photo integration scan; no measured total-cost ratio.

**Re-hook:**


## Change one example yourself (8:40-9:15)

**Picture:**
Scene `#repurpose` at localhost:8770. Edit support request, choose its human label, add it and download JSONL. Run prepare_task.py on the saved sample. Show held-out separation in the adaptation guide.

**Say:**
Say your job is sorting support messages. Here's someone charged twice. Choose Billing, add the example, and download the data file. You've made a checked example. You haven't trained a support model yet. The guide shows how to prepare the data, change the task and keep a separate test. Start with cases you understand, including confusing ones. Changing the labels alone won't teach the travel model a new job.

**On-screen copy:**
Change one example yourself.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Real JSONL export; tools/prepare_task.py; docs/ADAPT-YOUR-OWN.md. No completed support-model claim.

**Re-hook:**


## Start with a working example (9:15-9:45)

**Picture:**
Scene `#take-it` at localhost:8770. Open Start here and the question index. Show current access/permission status accurately; use only the delivered link once verified. Keep original creator/model credits visible.

**Say:**
You can start with the travel demo, inspect an answer, and then adapt the approach to a job you understand. The same repository brings together the code, setup guide, examples, model downloads and results, including the losses. Start with the guide and check the reuse terms for each part. Get one result running on your computer, then change one thing at a time.

**On-screen copy:**
Start with a working example.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
One repository stays private until the video goes live. Verify signed-out source and model-download access before adding the description link. Original-code reuse terms still need a decision. Retain all upstream credits.

**Re-hook:**

