"""Adapter invariants using the real tokenizer and a tiny random CPU Qwen model."""
import importlib.util
import json
from pathlib import Path
import pytest
import torch
from transformers import AutoTokenizer, Qwen3Config, Qwen3ForCausalLM

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('next_token_adapter', root / 'engine.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

@pytest.fixture(scope='module')
def engine():
    pin = json.loads((root / 'pin.json').read_text())
    value = adapter.NextTokenEngine.__new__(adapter.NextTokenEngine)
    value.pin = pin
    value.device = 'cpu'
    value.dtype = torch.float32
    value.source_sha256 = 'test-only-random-weights'
    value.name = 'test-only'
    value.tokenizer = AutoTokenizer.from_pretrained(pin['id'], revision=pin['revision'], local_files_only=True)
    value.tokenizer.padding_side = 'left'
    torch.manual_seed(42)
    torch.set_num_threads(2)
    value.model = Qwen3ForCausalLM(Qwen3Config(vocab_size=len(value.tokenizer),
        hidden_size=32, intermediate_size=64, num_hidden_layers=1,
        num_attention_heads=4, num_key_value_heads=2, head_dim=8,
        max_position_embeddings=4096)).eval()
    return value

def question():
    return {'id': 'refund', 'question': 'Can I cancel for a full refund?',
            'candidates': ['Fully refundable', 'Not fully refundable', 'Unspecified']}

def test_gold_does_not_change_prompt_and_long_inputs_fail(engine):
    q = question()
    a = adapter.render(engine.tokenizer, 'The hotel offers refunds.', q)
    b = adapter.render(engine.tokenizer, 'The hotel offers refunds.', {**q, 'gold': 2, 'soft_gold': [0, 0, 1]})
    assert a == b
    assert len(set(a[1])) == 3
    with pytest.raises(ValueError, match='no truncation'):
        adapter.render(engine.tokenizer, 'holiday ' * 3000, q)

def test_batch_padding_preserves_serial_scores(engine):
    q = question()
    qs = [q, {**q, 'id': 'long', 'question': 'The current booking is for the named property. ' * 8 + q['question']}]
    batched = engine.predict('Current terms provide a full refund.', qs)
    singles = [engine.predict('Current terms provide a full refund.', [x])['answers'][0] for x in qs]
    for a, b in zip(batched['answers'], singles):
        assert a['choice'] == b['choice']
        assert a['probabilities'] == pytest.approx(b['probabilities'], abs=1e-5)
        assert sum(a['probabilities']) == pytest.approx(1)
    assert batched['usage']['generated_tokens'] == 0

def test_nonfinite_logits_fail_closed(engine):
    original = engine.model
    class Invalid:
        def __call__(self, **kwargs):
            from types import SimpleNamespace
            return SimpleNamespace(logits=torch.full((1, 1, len(engine.tokenizer)), float('nan')))
    try:
        engine.model = Invalid()
        with pytest.raises(ValueError, match='Non-finite'):
            engine.predict('Terms', [question()])
    finally:
        engine.model = original
