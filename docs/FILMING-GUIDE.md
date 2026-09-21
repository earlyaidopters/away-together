# Build your own decision system

Canonical audience-gap revision. Eighteen filming surfaces. Exact Say blocks; companion holds deeper setup and troubleshooting. No TTS requested.

## Watch the photo change it (0:00-0:50)

**Picture:**
Scene `#demo` at localhost:8770. Run Maya with the stairs photo. Remove it and run again. Open the full agency’s persona grid briefly.

**Say:**
Watch Maya. She wants her money back if she cancels, and she doesn't want entrance stairs. The written terms work for her. Add this photo and her card turns red. Take it away and run it again. Now it asks us to check. The stairs haven't disappeared. We have less evidence. This runs on my computer. I used Astra to help build a Jev-like system that reads words and pictures. I'll show you the pieces, how to run my example, and what you'd change for your own job.

**On-screen copy:**
Watch the photo change it.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Fresh /api/decide receipts; active V1 plus pretrained vision. Fictional travellers and photos.

**Re-hook:**


## Give one job a home (0:50-1:30)

**Picture:**
Scene `#why` at localhost:8770. Follow holiday input → a small decision → a person checking the reason. Point at the review branch.

**Say:**
You might already use a big AI model to check the same thing over and over. Does this policy fit what my customer asked for? Here, we turn that question into a small part of an app. It chooses an answer, and the app knows what to do next. That can be useful. But training and setup take work. Start by testing ordinary rules and an existing model. Build the specialist when your own results give you a reason. I haven't proved this beats every alternative.

**On-screen copy:**
Give one job a home.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Task-selection guidance; no universal price or quality claim.

**Re-hook:**


## Astra helped build the system (1:30-2:05)

**Picture:**
Scene `#build` at localhost:8770. Show the exact prepared specification excerpt, then the saved source and model folders. Identify it as a prepared specification, not a captured chat.

**Say:**
This was the job I wrote down: build a local travel classifier, train it, test it, and connect it to an app. Astra helped me work through that build. There were follow-ups, fixes and multiple experiments. The downloaded models run without Astra answering each holiday question. My work here is the task, the app, the experiments and putting the pieces together. The foundation models and OpenJev came from other people. Their credits stay in the project.

**On-screen copy:**
Astra helped build the system.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
production/ASTRA-BUILD-PROMPT.md; saved source/checkpoint manifests; THIRD-PARTY-NOTICES.md.

**Re-hook:**


## Three parts. One decision (2:05-2:40)

**Picture:**
Scene `#map` at localhost:8770. Point to text reader, pretrained photo reader and app rules in order; keep Maya visible when returning to the agency.

**Say:**
The big picture is three pieces. One model reads the booking terms. Another looks at the actual pictures. Ordinary code checks their answers against Maya's wishes and her budget. I trained the text reader for this travel task. I connected an already trained image model. So when I say multimodal, I mean the system uses words and pictures. There isn't one new foundation model hiding behind these cards. And checking whether a price fits a budget belongs in ordinary code.

**On-screen copy:**
Three parts. One decision.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
travel_lab/vision.py; catalogue.py; active selection.json.

**Re-hook:**


## Give it three choices (2:40-3:15)

**Picture:**
Scene `#labels` at localhost:8770. Click Cash back, then Hotel credit. Point to the mapping between the teaching labels and actual output labels.

**Say:**
This policy says you get hotel credit. Can Maya get a full cash refund? No. We call that violates. A clear cash refund meets her requirement. If the document doesn't tell us, it's insufficient evidence. Those are the three labels the app uses. A classifier picks a label. Having a short list of answers makes the response easier for code to use. It doesn't guarantee the answer is right, or establish that every run will always return the same answer.

**On-screen copy:**
Give it three choices.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Teaching exercise; actual NLI labels in data/train.jsonl. Fixed format is not a deterministic-output claim.

**Re-hook:**


## An example has three parts (3:15-3:55)

**Picture:**
Scene `#training` at localhost:8770. Open actual train-00000 excerpt. Download the full record. Point at input, question, answer; show the separate held-out file only as data provenance.

**Say:**
We start with a reader that's already learned language patterns. The demo uses ModernBERT as its base. Then we give it examples like this actual training record. Here's what it reads. Here's the question. Here's the answer we've assigned. The policy tells us to contact the booking office, so the refund rule isn't established. These travel examples are made up. For your task, collect cases you understand and check the answers. A wrong label teaches the wrong lesson. The full record is in the download.

**On-screen copy:**
An example has three parts.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
assets/training-example.json exact data/train.jsonl record; synthetic, no human labels.

**Re-hook:**


## Practice. Check. Adjust (3:55-4:35)

**Picture:**
Scene `#practice` at localhost:8770. Play the two-lane HyperFrame. Hold at the wrong guess, checked label and saved-settings update. Point to unchanged settings in the normal-check lane.

**Say:**
During training, the model guesses, the training process checks that guess against the label, and it adjusts saved settings. We repeat that over the practice examples. That's fine-tuning. A prompt gives instructions for the current request. Training changes what gets saved. When you click Check in this app, it uses the saved model. It isn't learning a new lesson every time. You can run the travel demo with the weights I've already supplied. You don't need to train it again first.

**On-screen copy:**
Practice. Check. Adjust.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Training code and saved checkpoints. Diagram is conceptual, not a measured individual training step.

**Re-hook:**


## Keep the exam sealed (4:35-5:15)

**Picture:**
Scene `#test` at localhost:8770. Show practice and final-test objects. Open the held-out example and explain its split, then return to the diagram.

**Say:**
Some examples must stay away from training. Otherwise we're testing how well it remembers our practice sheet. Keep related templates and documents together when you split the data. We used synthetic cases and agent review for the later test. That included document repairs and a couple of disputed references resolved with help from the writer. There was no human validation. Then we froze the model before the final comparison. You can inspect that trail. Once we've seen the mistakes, that exam can't become a fresh test again.

**On-screen copy:**
Keep the exam sealed.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Frozen V2 protocol; 52 document repairs; two writer-assisted adjudications; hashes. V1 held-out download is labeled separately.

**Re-hook:**


## Inspect one real mistake (5:15-5:55)

**Picture:**
Scene `#failure` at localhost:8770. Show case …0036 arrival excerpt and both saved outputs. Open full JSON to show the input is longer than the excerpt.

**Say:**
Here's one of the mistakes. The document says arrival at one thirty in the morning is available automatically, without contacting anyone first. Our reference says that meets the late-arrival requirement. Jev agreed. My later challenger said it couldn't tell. In this case it creates unnecessary review work. Both models received the same full document; you're seeing an excerpt. This is a saved test result. Looking at an actual mistake tells us more than a green card in a selected demo.

**On-screen copy:**
Inspect one real mistake.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
assets/benchmark-case.json; raw frozen local and Jev rows for round1-deeper-fp16-0036, arrival.

**Re-hook:**


## The test kept us honest (5:55-6:35)

**Picture:**
Scene `#results` at localhost:8770. Show common-axis bars; point to text-only scope and distinguish demo V1 from later V2. Do not animate a V1→V2 improvement arrow.

**Say:**
Across those same test cases, my later challenger agreed with the references about ninety-five percent of the time. Jev was closer to ninety-nine. I didn't beat Jev. The challenger failed the promotion rule we'd set beforehand, so the app still runs the earlier model. That earlier model scored sixty-six point five on a different test. You can't compare those as an improvement chart. And this chart tests text decisions, not the complete picture-aware system. A working interface and a reliable model are separate things.

**On-screen copy:**
The test kept us honest.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
FROZEN-V2-RESULTS.md; qualification-decision.json; V1 summary. No model or final-test changes.

**Re-hook:**


## Give the system eyes (6:35-7:20)

**Picture:**
Scene `#vision` at localhost:8770. Play photo→observation→app. Open photo-lab.html, choose a local image, run it and inspect actual answers and image hash. Keep the service running before filming.

**Say:**
Now give it a picture. This image reader is already trained. It reads the pixels and answers questions about visible features. It isn't creating these pictures; the holiday illustrations were made separately. I connected the reader through OpenJev, and you can try your own PNG or JPEG in this local photo lab. The image goes to the model on this computer. Its filename and an expected answer aren't sent. This shows our local integration. It doesn't establish what the hosted Jev product supports.

**On-screen copy:**
Give the system eyes.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Fresh /api/observe receipt; fixed loopback endpoint; pretrained DiffusionGemma. Generated fictional catalogue photos.

**Re-hook:**


## A picture leaves things out (7:20-8:00)

**Picture:**
Scene `#boundary` at localhost:8770. Show pond, ask the three questions and reveal the conclusion. Refer back to the missing stairs photo.

**Say:**
There's water in this garden. That doesn't establish a swimming pool. Even a clear pool wouldn't tell you whether guests can use it, whether it's open, or whether it costs extra. The photo shows what's visible. The written terms tell us what's promised. Our forty holiday offers share nine fictional images across three destinations, so this isn't a test of forty real hotels. If the pictures don't settle Maya's access question, a person has to check it. Removing a photo doesn't make the entrance accessible.

**On-screen copy:**
A picture leaves things out.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Generated-image ledger; location-photos.json; image evidence limitations.

**Re-hook:**


## The app makes the call (8:00-8:40)

**Picture:**
Scene `#rules` at localhost:8770. Play budget/terms/photo gates. In the actual agency open a traveller drawer and show the clause/photo that caused decline or review.

**Say:**
The app brings the checks together. Budget passes. Terms pass. Entrance stairs fail, so Maya's card declines. If evidence is missing, it goes to review, unless another requirement already fails. Click the person and inspect the reason. A green card means the implemented checks passed according to these models. It isn't a verified booking recommendation. A person still confirms unclear terms or access. The app doesn't book anything. You can use a checked status to suggest a next step in another workflow.

**On-screen copy:**
The app makes the call.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
catalogue.verdict; apply_visual_requirements; live reason drawer; companion local API example.

**Re-hook:**


## Check your computer first (8:40-9:20)

**Picture:**
Scene `#setup` at localhost:8770. Show tested M5 Max/128 GB host and separate text/image requirements. Open Start here prerequisites briefly.

**Say:**
Before you download anything, here's the computer I used. An M5 Max with a hundred and twenty-eight gigabytes of memory. That's my tested machine, not a minimum requirement. The photo launcher uses Apple silicon and downloads about sixteen gigabytes of weights. Download size isn't RAM usage. I haven't validated this image setup on Windows, Linux or a smaller-memory machine. The text app and image reader have separate setup steps. Seeing a page on your phone also doesn't mean the model is running on your phone.

**On-screen copy:**
Check your computer first.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Inspected host, macOS 26.5.2; pinned vision launcher. No unsupported hardware promises.

**Re-hook:**


## Run it before changing it (9:20-10:05)

**Picture:**
Scene `#first-run` at localhost:8770. Open Start here. Show source and restored files, run first_run.py, start agency in a spare terminal if needed, inspect service status and run a fresh holiday. No fake installation animation.

**Say:**
Start with the guide in the kit. Get the source, restore the matching model archive, and install the listed tools. The first-run check tells you what's missing. Then start the text service and open the app. Add the separate photo service when you're ready. These commands are copyable in the guide. If the service isn't running, the page tells you; it doesn't slip in an old successful answer. Leave the process running while you use it. After your laptop sleeps, check the services and restart anything that stopped.

**On-screen copy:**
Run it before changing it.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
tools/first_run.py, tools/restore_companion.py, docs/SETUP.md and live /api/status. Public access separately gated.

**Re-hook:**


## Count the whole bill (10:05-10:45)

**Picture:**
Scene `#cost` at localhost:8770. Show build/setup and local-running cost columns, then separately labeled historical timings. Point to fresh demo time rather than implying benchmark-equivalent workloads.

**Say:**
Running the local check doesn't create a model-provider API charge. You still paid for the computer, use electricity, and spend time setting it up. Coding tools and training can have costs too. I haven't measured the total build bill or proved a fixed saving over every language model. The timing examples here are different workloads: a cold text request, a warm text request, and a whole photo scan. Measure the job you care about on your machine. Hosted benchmark calls are separate from running this local demo.

**On-screen copy:**
Count the whole bill.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Historical V1 HTTP timing receipts and photo integration scan; no measured total-cost ratio.

**Re-hook:**


## Change one example yourself (10:45-11:30)

**Picture:**
Scene `#repurpose` at localhost:8770. Edit support request, choose its human label, add it and download JSONL. Run prepare_task.py on the saved sample. Show held-out separation in the adaptation guide.

**Say:**
Let's make something you can change. Here's a support message about being charged twice. You choose Billing, add the example, and download a real data file. The editor hasn't trained anything or guessed the answer. You're creating checked examples. The companion shows how to map them into the training format. Keep a separate test, including confusing cases. Twenty examples you personally check can reveal obvious problems, but twenty isn't a proven training minimum. A new subject needs its own configuration and tests. Renaming the travel model won't teach it support.

**On-screen copy:**
Change one example yourself.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Real JSONL export; tools/prepare_task.py; docs/ADAPT-YOUR-OWN.md. No completed support-model claim.

**Re-hook:**


## Start with a working example (11:30-12:10)

**Picture:**
Scene `#take-it` at localhost:8770. Open Start here and the question index. Show current access/permission status accurately; use only the delivered link once verified. Keep original creator/model credits visible.

**Say:**
Everything is organized around that path. Run the travel example. Inspect an answer and a mistake. Then change one job you understand well. The companion includes the setup steps, data examples, source credits and the results we kept, including the losses. It also answers the practical questions about hardware, costs, photos and recovery. Use the resource's stated access and reuse terms. Don't assume a private link grants permission to share or sell it. Start with one result you can check yourself, and build from there.

**On-screen copy:**
Start with a working example.

**Editing note:**
Let the result finish before speaking its meaning. P pauses diagrams; R resets current scene. Give the final visual time to read. Setup commands and photo results must be real; extended installation waits can be cut with the elapsed time disclosed.

**Source or truth card:**
Current resource manifest, access check and reuse terms. Until public delivery is authorized, film as private preparation and do not promise public access.

**Re-hook:**

