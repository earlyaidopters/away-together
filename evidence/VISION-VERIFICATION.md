# Image integration verification — 2026-09-21

OpenJev / DiffusionGemma MLX ran locally on actual pixels for all nine fictional destination images. Six images were added, two per destination. The pretrained vision branch is separate from our trained text classifier and historical benchmark.

- Python: 62 tests plus four subtests passed. Frontend: four tests passed; production build passed after saved-run preference repair.
- Causal HTTP check: unchanged text answers; Madeira stairs included makes Maya decline, removing that photograph makes her review. Photos disabled makes visual requirements review. Receipt: vision-causal-checks.json.
- All 40 offers completed fresh requests, with unique run IDs, in 40.7168 seconds. This is a smoke test, not an accuracy benchmark. OpenJev may reuse prompt prefills. Receipt: vision-full-scan.json.
- Browser: photo toggles, terms-only mode, traveller evidence, four-friend results, pause and reset checked. DOM had no horizontal overflow at 1920×1080, 1440×900, 1366×768 and 390×844. Screenshots inspected. Native screenshot scaling cropped its captured edge; DOM dimensions were checked independently.
- Guide: 13 pages visually inspected; narration source 1,507 words; production check 16 passed, zero warnings/errors. No TTS requested.
- Images are generated fictional examples shared by destination across the 40 offers. Photo absence is not proof of feature absence; photos cannot establish free access or override written terms. The 0.8 threshold is a demo heuristic, not calibrated accuracy.
- Setup requires Apple silicon and a separate approximately 16 GB model download. Model weights and local virtual environments are excluded from the resource archive.
