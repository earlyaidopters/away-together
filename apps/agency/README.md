# Away Together: build your own Jev experiment

The frozen V2 challenger scored **95.28%** on fresh synthetic travel references versus **98.61%** for Jev. It passed the quality and coverage floors but failed the prespecified head-to-head superiority gate. It was not promoted; conditional replication was not launched. No final-error tuning or replacement seed followed.

Start with [START-HERE.md](START-HERE.md). The local agency still serves historical V1, which failed its reliability targets. The model page shows V2 evidence separately. See the [frozen challenger report](output/benchmarks/FROZEN-V2-RESULTS.md), [model card](MODEL-CARD.md), and [V1 history](output/benchmarks/RESULTS.md).

Run the launcher or open http://127.0.0.1:8765 while the server is running. The demo uses local saved weights and requires no API key. The companion resource includes both the active V1 model and the frozen V2 challenger, plus original and repaired reference evidence. Synthetic references have not been validated by humans.

## Photo-aware revision, 21 September 2026

The agency now uses real local OpenJev / DiffusionGemma image inference alongside the existing V1 text classifier. Each destination has three fictional listing photos, with selectable image evidence and editable traveller photo preferences. Run `Launch Vision.command` once to set up the pinned Apple Silicon backend, then launch the agency. The additional model download is about 16 GB and is not included in the ZIP. It runs in a separate environment on localhost:8081. Photo observations do not establish prices, free access, availability or accessibility. Missing evidence requires review. See `experiments/openjev-vision/README.md` for source pins, installation, real run receipts and limits. The historical V2 text comparison is unchanged; this is not a new Jev superiority result.
