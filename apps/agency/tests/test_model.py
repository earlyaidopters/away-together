import torch
from travel_lab.model import group_logits

def test_variable_candidates_mask_and_gradient():
    x=torch.tensor([1.,2.,3.,4.,5.],requires_grad=True);z=group_logits(x,[2,3]);assert torch.isneginf(z[0,2]);p=z.softmax(-1);assert p[0,2]==0;assert torch.allclose(p.sum(-1),torch.ones(2))
    torch.nn.functional.cross_entropy(z,torch.tensor([0,2])).backward();assert torch.isfinite(x.grad).all()
def test_admission_has_finite_gradient_updates_and_parity():
    import json
    r=json.load(open('runs/preflight/admission.json'));assert r['parity_max_abs']<1e-4;assert r['head_reload'];assert all(v['finite'] for v in r['timings'].values())
