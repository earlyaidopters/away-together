# Run one example first

1. Read [setup and supported hardware](docs/SETUP.md).
2. Restore the matching companion model archive, install dependencies and build the app.
3. From this folder run `python3 tools/first_run.py`, then `python3 tools/first_run.py --start`.
4. Open localhost:8765 and run one holiday. The first model load can be slower.
5. Start the Apple-silicon photo service separately if needed.
6. Launch `python3 apps/explainer/serve.py` and open localhost:8770.

The explainer includes **Start here**, **Questions & answers**, and **Try your own photo**. Use its data editor to export labeled examples, then follow [adaptation](docs/ADAPT-YOUR-OWN.md) and the [API example](docs/API-EXAMPLE.md).

This is the single project repository: private during preparation, public when the video goes live. Access does not grant a blanket license; reuse follows the supplied component terms. Upstream licenses and notices stay with their components.
