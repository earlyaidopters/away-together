import unittest,threading
from types import SimpleNamespace
import torch
from experiments.v2.engine import DebertaEngine
from travel_lab.nli import HYPOTHESES

class BatchTests(unittest.TestCase):
 def test_batch_preserves_question_order_and_permuted_candidates(self):
  engine=DebertaEngine.__new__(DebertaEngine);engine.lock=threading.Lock();engine.device='cpu';engine.temperature=1;engine.labels={'entailment':0,'neutral':1,'contradiction':2};engine.name='test';engine.selection={'sha256':'test','revision':'test'}
  seen=[]
  def encode(a,b):
   seen.append((a,b));return {'hypotheses':b}
  engine.encode=encode
  engine.model=lambda hypotheses:SimpleNamespace(logits=torch.tensor([[6.,0.,-2.] if h==HYPOTHESES['refund'][0] else [-2.,0.,6.] for h in hypotheses]))
  qs=[{'id':'arrival','question':'arrival','candidates':list(reversed(HYPOTHESES['arrival']))},{'id':'refund','question':'refund','candidates':HYPOTHESES['refund']}]
  result=engine.predict('full document',qs)
  self.assertEqual(result['usage']['local_model_calls'],1)
  self.assertEqual([a['id'] for a in result['answers']],['arrival','refund'])
  self.assertEqual([a['choice'] for a in result['answers']],[1,0])
  self.assertEqual(seen[0][0],['full document','full document'])
  self.assertEqual(seen[0][1],[HYPOTHESES['arrival'][0],HYPOTHESES['refund'][0]])
  for a in result['answers']:self.assertAlmostEqual(sum(a['probabilities']),1,places=6)

 def test_policy_temperature_changes_confidence_without_changing_choice(self):
  engine=DebertaEngine.__new__(DebertaEngine);engine.lock=threading.Lock();engine.device='cpu';engine.temperature=1;engine.temperature_by_field={'refund':3};engine.labels={'entailment':0,'neutral':1,'contradiction':2};engine.name='test';engine.selection={'sha256':'test','revision':'test'}
  engine.encode=lambda a,b:{'n':len(b)}
  engine.model=lambda n:SimpleNamespace(logits=torch.tensor([[4.,0.,-1.]]*n))
  qs=[{'id':t,'question':t,'candidates':HYPOTHESES[t]} for t in ['refund','arrival']]
  answers=engine.predict('document',qs)['answers']
  self.assertEqual([a['choice'] for a in answers],[0,0])
  self.assertLess(answers[0]['probabilities'][0],answers[1]['probabilities'][0])
  expected=torch.softmax(torch.tensor([4.,-1.,0.])/3,dim=-1).tolist()
  for a,b in zip(answers[0]['probabilities'],expected):self.assertAlmostEqual(a,b,places=6)

if __name__=='__main__':unittest.main()
