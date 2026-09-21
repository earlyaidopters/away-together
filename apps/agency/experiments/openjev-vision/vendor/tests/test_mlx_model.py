"""The MLX backend against real weights, on Apple silicon:

    OPENJEV_MLX_TEST_MODEL=~/models/diffusiongemma-26B-A4B-it-4bit pytest tests/test_mlx_model.py
"""
import os

import pytest
from fastapi.testclient import TestClient

MODEL = os.environ.get("OPENJEV_MLX_TEST_MODEL")
pytestmark = pytest.mark.skipif(not MODEL, reason="set OPENJEV_MLX_TEST_MODEL to an MLX DiffusionGemma checkpoint")

QUESTIONS = {
    "urgent": {"type": "noul", "instructions": "Does the customer need a reply within the hour?"},
    "team": {"type": "choice", "instructions": "Which team should handle it?",
             "criteria": {"outage": "service down", "billing": "charges, refunds", "feature": "requests, how-to"}},
    "tone": {"type": "score", "instructions": "How upset is the customer?", "criteria": ["calm", "annoyed", "furious"]},
}
STATES = {  # state -> (urgent, team, tone level)
    "Everything is down and we have a demo with our biggest client at noon.": (True, "outage", 2),
    "I was charged twice this month. Not urgent, just let me know when it's refunded. Thanks!": (False, "billing", 0),
    "Love the product. Any chance you could add a dark mode at some point?": (False, "feature", 0),
}


@pytest.fixture(scope="module")
def client():
    from openjev.api import create_app
    from openjev.config import Settings

    with TestClient(create_app(Settings(backend="mlx", mlx_model=os.path.expanduser(MODEL)))) as c:
        yield c


def ask(client, state, questions=QUESTIONS, **extra):
    r = client.post("/v1/systemone", json={"state": state, "model": "openjev-latest", "questions": questions, **extra})
    assert r.status_code == 200, r.text
    return r.json()


def test_readme_example_and_friends(client):
    for state, (urgent, team, tone) in STATES.items():
        body = ask(client, state)
        a = body["answers"]
        assert (a["urgent"]["noul"] > 0.9) == urgent and (a["urgent"]["noul"] < 0.1) != urgent, (state, a["urgent"])
        assert a["team"]["choice"] == team and a["team"]["confidence"] > 0.9, (state, a["team"])
        assert abs(a["tone"]["score"] - tone) < 0.25, (state, a["tone"])
        assert abs(sum(a["team"]["probabilities"].values()) - 1) < 1e-6
        assert body["usage"]["input_tokens"] > 100 and body["usage"]["output_tokens"] == 0


def test_same_request_same_answer(client):
    state = next(iter(STATES))
    assert ask(client, state) == ask(client, state)
    assert ask(client, state, samples=3) == ask(client, state, samples=3)


def test_a_cached_prefill_reads_the_same(client):
    """The decoder pass must leave the prompt's cache as it found it, or reusing
    it for re-reads and samples would change their answers."""
    engine = client.app.state.engine
    rt = engine.runtime
    schema = engine.build_schema(QUESTIONS)
    template, slots = engine.resolve_template(schema["questions"], schema["format"])
    prompt = engine.chat_prompt_ids(engine.system_text(schema["questions"], schema["format"]), "The invoice is wrong.")
    canvases = [engine.build_canvas(template, slots, seed) for seed in (1, 2, 3)]

    def fresh(canvas):
        rt.prefills.clear()
        return rt.read(prompt, canvas, slots, engine.s.mlx_max_prompt)

    def reused():
        rt.prefills.clear()
        return [rt.read(prompt, c, slots, engine.s.mlx_max_prompt) for c in canvases]

    cold = [rt.pool.submit(fresh, c).result() for c in canvases]
    assert rt.pool.submit(reused).result() == cold  # bitwise


COLOUR = {"colour": {"type": "choice", "instructions": "What colour fills the picture?",
                     "criteria": {"red": "the image is red", "blue": "the image is blue",
                                  "green": "the image is green"}}}


def solid_png(rgb, size=64):
    import base64
    import io

    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (size, size), rgb).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def test_the_model_reads_an_image(client):
    """A solid colour is the least ambiguous thing an image can say, so a wrong
    or hedged answer here is a real failure, not flakiness."""
    for colour, rgb in (("red", (255, 0, 0)), ("blue", (0, 0, 255))):
        body = ask(client, "What colour is this?", COLOUR, images=[solid_png(rgb)])
        a = body["answers"]["colour"]
        assert a["choice"] == colour and a["probabilities"][colour] > 0.9, (colour, a)
        assert body["usage"]["input_tokens"] > 100


def test_an_image_prefill_reads_the_same_cold_or_reused(client):
    """Mirrors test_a_cached_prefill_reads_the_same: the decoder pass must leave
    an image prompt's cache as it found it, or re-reads would drift."""
    rt = client.app.state.engine.runtime
    body = {"state": "What colour is this?", "model": "openjev-latest",
            "questions": COLOUR, "images": [solid_png((255, 0, 0))]}
    rt.pool.submit(rt.prefills.clear).result()
    cold = client.post("/v1/systemone", json=body)
    assert cold.status_code == 200, cold.text
    assert rt.prefills, "the image prefill was not cached"
    reused = client.post("/v1/systemone", json=body)  # this one hits the cached vision pass
    assert reused.status_code == 200 and reused.json() == cold.json()
    assert ask(client, body["state"], COLOUR, images=body["images"], samples=3) == \
        ask(client, body["state"], COLOUR, images=body["images"], samples=3)


def test_many_questions_chunk_and_run_in_sequence(client):
    qs = {f"k{i}": {"type": "noul", "instructions": f"The message mentions the number {i}"} for i in range(24)}
    state = "The numbers I care about are 3, 11 and 20."
    for extra in ({}, {"sequential": True}):
        a = ask(client, state, qs, **extra)["answers"]
        assert len(a) == 24 and all(0 <= v["noul"] <= 1 for v in a.values())


def test_more_steps_still_answer_and_cost_no_more_prompt(client):
    """Extra denoise steps settle the canvas; they must not change what is billed,
    because every step shares the one prefill of the same prompt."""
    last = None
    for state, (urgent, team, tone) in STATES.items():
        one, four = ask(client, state), ask(client, state, steps=4)
        last = (state, four)
        assert one["usage"] == four["usage"], (state, one["usage"], four["usage"])
        a = four["answers"]
        assert (a["urgent"]["noul"] > 0.9) == urgent, (state, a["urgent"])
        assert a["team"]["choice"] == team and a["team"]["confidence"] > 0.9, (state, a["team"])
        assert abs(a["tone"]["score"] - tone) < 0.25, (state, a["tone"])
    state, four = last
    assert ask(client, state, steps=4) == four  # and it stays deterministic


def test_steps_hold_the_template_and_reuse_one_prefill(client):
    """The canvas outside the answer slots is what vLLM pins with diffusion_pinned.
    Here it is never written, so it cannot drift however many steps run. steps=1
    must also be exactly the single pass it was before the loop existed."""
    from openjev import mlx_backend

    engine = client.app.state.engine
    rt = engine.runtime
    schema = engine.build_schema(QUESTIONS)
    template, slots = engine.resolve_template(schema["questions"], schema["format"])
    prompt = engine.chat_prompt_ids(engine.system_text(schema["questions"], schema["format"]), "The invoice is wrong.")
    canvas = engine.build_canvas(template, slots, 7)
    seen = list(canvas)

    def run(steps):
        rt.prefills.clear()
        out = rt.read(prompt, canvas, slots, engine.s.mlx_max_prompt, steps)
        return out, len(rt.prefills)

    (one, one_prefills) = rt.pool.submit(run, 1).result()
    (four, four_prefills) = rt.pool.submit(run, 4).result()
    assert one_prefills == four_prefills == 1  # one prefill however many steps
    assert canvas == seen, "the step loop wrote back into the caller's canvas"
    assert one != four, "four steps returned the single pass's logprobs"

    def old_single_pass():
        """read() as it was before the loop: one decoder pass, no self-conditioning,
        no argmax, log-softmax per slot."""
        mx = rt.mx
        rt.prefills.clear()
        cache, n = rt._prefill(prompt, engine.s.mlx_max_prompt)
        ids = mx.array([canvas])
        masks = rt.model.diffusion_decoder_masks(ids, cache, None)
        logits = rt.model.diffusion_decoder_logits(ids, cache=cache, self_conditioning=None,
                                                   decoder_attention_mask=masks)
        out = []
        for s in slots:
            row = logits[0, s["pos"]].astype(mx.float32)
            lp = row - mx.logsumexp(row)
            keep = sorted(set(mx.argpartition(-lp, mlx_backend.TOPK)[:mlx_backend.TOPK].tolist())
                          | set(s["label_ids"]))
            out.append(dict(zip(keep, lp[mx.array(keep)].tolist())))
        return out, n

    assert rt.pool.submit(old_single_pass).result() == one  # bitwise


def test_think_answers_and_is_billed(client):
    """A real thought is written, then read. The thought is billed as output,
    and the input covers both passes, so it exceeds a plain read's."""
    state, (urgent, team, tone) = next(iter(STATES.items()))
    plain = ask(client, state)
    thought = ask(client, state, think=128)
    a = thought["answers"]
    assert a["team"]["choice"] == team and (a["urgent"]["noul"] > 0.9) == urgent
    # the score only has to stay on the right side of the scale: a thought is free
    # to move it, and how far is the model's judgement, not this server's contract
    assert abs(a["tone"]["score"] - tone) < 1.0, a["tone"]
    # what this test is really for: the thought is billed as output, and the input
    # covers both passes
    assert 0 < thought["usage"]["output_tokens"] <= 128
    assert thought["usage"]["input_tokens"] > plain["usage"]["input_tokens"]


def test_think_works_with_sequential(client):
    """think must compose with sequential: one thought, then a read a chunk."""
    qs = {f"k{i}": {"type": "noul", "instructions": f"Is statement {i} about an outage?"} for i in range(24)}
    body = ask(client, next(iter(STATES)), qs, sequential=True, think=64)
    assert len(body["answers"]) == 24 and all(0 <= v["noul"] <= 1 for v in body["answers"].values())
    assert 0 < body["usage"]["output_tokens"] <= 64


def chat(client, **extra):
    return client.post("/v1/chat/completions", json={
        "model": "diffusiongemma-26b", "max_tokens": 64,
        "messages": [{"role": "user", "content": "What is the capital of France? Answer in one short sentence."}],
        **extra})


def test_chat_completion_generates_text(client):
    r = chat(client)
    assert r.status_code == 200, r.text
    d = r.json()
    text = d["choices"][0]["message"]["content"]
    assert "Paris" in text, text
    assert d["model"] == "diffusiongemma-26b" and d["choices"][0]["finish_reason"] in ("stop", "length")
    assert d["usage"]["completion_tokens"] > 0
    assert d["usage"]["total_tokens"] == d["usage"]["prompt_tokens"] + d["usage"]["completion_tokens"]


def test_chat_stream_matches_the_whole_reply(client):
    """The streamed deltas must join to what the non-streaming route returns:
    greedy generation, same prompt, so the two cannot disagree."""
    import json as _json

    whole = chat(client).json()["choices"][0]["message"]["content"]
    with client.stream("POST", "/v1/chat/completions", json={
            "model": "diffusiongemma-26b", "max_tokens": 64, "stream": True,
            "stream_options": {"include_usage": True},
            "messages": [{"role": "user", "content": "What is the capital of France? Answer in one short sentence."}]}) as r:
        assert r.status_code == 200
        events = [_json.loads(line[6:]) for line in r.iter_lines()
                  if line.startswith("data: ") and line != "data: [DONE]"]
    streamed = "".join(e["choices"][0]["delta"].get("content", "") for e in events if e["choices"])
    assert streamed == whole, (streamed, whole)
    assert [e for e in events if e.get("usage")], "include_usage asked for, none sent"


def test_chat_json_mode_returns_one_object(client):
    import json as _json

    r = client.post("/v1/chat/completions", json={
        "model": "diffusiongemma-26b", "max_tokens": 128,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": 'Give the capital of France as {"city": ...}.'}]})
    assert r.status_code == 200, r.text
    content = r.json()["choices"][0]["message"]["content"]
    assert _json.loads(content)  # the reply is exactly one JSON value, no prose or fences


def test_the_prompt_cache_is_bounded_in_tokens(client):
    from openjev import mlx_backend

    rt = client.app.state.engine.runtime
    for i in range(12):
        ask(client, f"Order {i} arrived broken. " + "Please help. " * 600, {"refund": {"type": "noul", "instructions": "The customer wants a refund"}})
    assert 1 <= len(rt.prefills) < 12
    assert sum(map(len, rt.prefills)) <= mlx_backend.PROMPT_CACHE_TOKENS


# "Count: ..." is the prompt that leaked the thought channel most readily before
# the markers were skipped: roughly 1 reply in 5. One clean reply proves nothing,
# so each prompt is asked several times, on both the streaming and the whole-reply
# path -- the two used to leak at different rates.
LEAK_PROMPTS = ["Count: one two three four five", "Name one prime number",
                "What colour is the sky?", "Say hello.", "Give one European capital."]


def test_no_reply_leaks_the_thought_channel(client):
    """No reply may show the markers, on either path.

    Emptiness is counted rather than asserted per reply: the model returns an
    empty generation for an identical greedy prompt about once in thirty, which
    is the checkpoint's own nondeterminism and not something this server can fix.
    The threshold only has to catch a server that returns nothing at all."""
    import json as _json

    replies = []
    for _ in range(3):
        for p in LEAK_PROMPTS:
            body = {"model": "diffusiongemma-26b", "max_tokens": 40,
                    "messages": [{"role": "user", "content": p}]}
            r = client.post("/v1/chat/completions", json=body)
            assert r.status_code == 200, r.text
            text = r.json()["choices"][0]["message"]["content"]
            assert "channel" not in text, (p, text)
            replies.append(text)

            with client.stream("POST", "/v1/chat/completions", json=dict(body, stream=True)) as r:
                assert r.status_code == 200
                events = [_json.loads(line[6:]) for line in r.iter_lines()
                          if line.startswith("data: ") and line.strip() != "data: [DONE]"]
            streamed = "".join(e["choices"][0]["delta"].get("content", "")
                               for e in events if e["choices"])
            assert "channel" not in streamed, (p, streamed)
            replies.append(streamed)
    assert sum(bool(t.strip()) for t in replies) >= 0.6 * len(replies), replies


def test_think_still_gets_its_thought(client):
    """Chat skips the thought-channel markers; think must not, or the thought it
    reads after would be empty."""
    state = next(iter(STATES))
    plain = ask(client, state)
    thought = ask(client, state, think=96)
    assert 0 < thought["usage"]["output_tokens"] <= 96
    assert thought["usage"]["input_tokens"] > plain["usage"]["input_tokens"]
