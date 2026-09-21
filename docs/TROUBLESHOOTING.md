# Get back to one working result

Start with [setup](SETUP.md). Run commands from the repository root unless the command explicitly changes directory. Keep the service terminal open.

```bash
python3 tools/first_run.py
python3 tools/first_run.py --probe
```

The first checks prerequisites. The second checks the running agency. A reachable service is not proof of correct inference: run a holiday and inspect its fresh receipt.

| What happens | Likely next check | What success looks like |
|---|---|---|
| GitHub says repository not found | This repo is private until video launch; check your access | You can view/download the authorized repository |
| Missing weights | Restore the matching companion release before starting inference | Selected model file exists and restore verifies its hash |
| Restore says existing source differs | Preserve your changes; use a clean matching checkout | Restore finishes without overwriting differing files |
| Command not found | Install the named prerequisite, reopen the terminal | Prerequisite checker reports it present |
| Page opens but live check fails | Agency must run on 8765; photo service separately on 8081 | Fresh result with status, reasons and run ID |
| Address already in use | Check whether the existing local service is already healthy | One intended service owns the port |
| First request is slow | The text model loads on first use; vision downloads separately | Request completes; compare later requests separately |
| Images unavailable | Supplied vision setup requires Apple silicon and its own completed download | Photo service reachable, then a fresh image observation |
| Computer slept or terminal closed | Wake it and restart the affected service | New successful request; old output is not substituted |
| High memory usage | Stop other model workloads; smaller-memory support is unverified | Your machine completes the actual workload |
| Diagram is paused | Use P to play/pause and R to reset the current scene | Scene restarts; reduced-motion preference may start paused |
| Edited support example does not change model behavior | The editor prepares data; it does not train or predict | Export JSONL, then follow the separate adaptation workflow |

## Report a reproducible problem

Include your OS, processor/memory, repository commit, exact command, error text and whether text-only or image inference failed. Describe expected versus actual behavior and the smallest example that reproduces it. Remove credentials and private customer data. Do not send an entire environment dump. A public issue channel becomes available when this same repository goes public.

## Hardware and accessibility scope

The tested host was Apple M5 Max, 128 GB RAM, macOS 26.5.2. That is not a minimum requirement. The roughly 16 GB vision download is not a RAM estimate. Windows/Linux vision, smaller machines and phone inference are unvalidated. Reading the Markdown guides or the visual explainer does not require running the models.

Diagrams also have prose/table explanations here. The site uses text labels alongside status colors and offers pause/reset controls. Four viewport sizes were checked; that is not a complete accessibility certification or a claim of full assistive-technology testing.
