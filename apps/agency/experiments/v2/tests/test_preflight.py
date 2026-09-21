import json,tempfile,unittest
from pathlib import Path
from experiments.v2.preflight import preflight
from travel_lab.nli import HYPOTHESES

class Tokenizer:
 def __init__(self,n=30):self.n=n
 def __call__(self,a,b,truncation):
  assert truncation is False
  return {'input_ids':[0]*self.n}

def dataset(root):
 (root/'data').mkdir();(root/'runs').mkdir()
 for split in ['train','dev','calibration','robustness-dev']:
  row={'id':split,'state':split+' distinct text','questions':[{'id':t,'gold':0,'candidates':h} for t,h in HYPOTHESES.items()], 'provenance':{t:{'source':split+'.json','index':i} for i,t in enumerate(HYPOTHESES)}}
  (root/f'data/{split}.jsonl').write_text(json.dumps(row)+'\n')

class PreflightTests(unittest.TestCase):
 def test_clean_splits_pass(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);dataset(root);self.assertEqual(preflight(Tokenizer(),root)['splits']['train']['max_tokens'],30)
 def test_shared_source_rejected_even_with_different_text(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);dataset(root);p=root/'data/dev.jsonl';row=json.loads(p.read_text());row['provenance']['refund']={'source':'train.json','index':0};p.write_text(json.dumps(row)+'\n')
   with self.assertRaisesRegex(ValueError,'contamination'):preflight(Tokenizer(),root)
 def test_overlong_text_rejected_with_receipt(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);dataset(root)
   with self.assertRaisesRegex(ValueError,'Overlong'):preflight(Tokenizer(513),root)
   self.assertTrue((root/'runs/data-preflight.json').exists())

if __name__=='__main__':unittest.main()
