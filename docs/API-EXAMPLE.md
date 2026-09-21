# Connect a checked label to an app

With the local agency running, this Python standard-library example sends an actual travel request and prints its status and reasons:

```python
import json
from urllib.request import Request, urlopen
body = {"offer_id": "o0", "profiles": [{"id": "p0", "budget": 1600,
        "requirements": ["refund"], "visual_requirements": []}], "include_photos": False}
request = Request("http://127.0.0.1:8765/api/decide", data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json"})
with urlopen(request, timeout=120) as response:
    result = json.load(response)
print(result["profiles"]["p0"]["status"])
print(result["profiles"]["p0"]["reasons"])
```

A caller can use `match`, `decline`, or `review` to display a next step. Inspect the evidence, handle service errors and keep a human approval checkpoint before any real booking or external action. This snippet does not book anything. The travel API does not become a support router merely by changing the label name.

Fresh requests create run receipts. The explainer’s `/api/status` only checks local service reachability. The photo lab forwards pixels to the local vision service and returns visible-feature observations; it does not save the selected image or modify the catalogue.
