import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from experiments.v2.promote import promote
from experiments.v2.freeze_candidate import sha

class PromotionTests(unittest.TestCase):
 def test_one_round_or_same_round_twice_is_not_replication(self):
  with self.assertRaises(ValueError):promote('unused',['a'])
  with self.assertRaises(ValueError):promote('unused',['a','a'])
 def test_matching_engines_cannot_be_promoted(self):
  with tempfile.TemporaryDirectory() as d:
   before=Path.cwd();os.chdir(d)
   try:
    freeze={'checkpoint':'checkpoint','model_sha256':'test-only'};Path('freeze.json').write_text(json.dumps(freeze))
    for name in ['first','replica']:
     folder=Path(name);folder.mkdir();(folder/'freeze.json').write_text(json.dumps(freeze));(folder/'data-manifest.json').write_text(json.dumps({'freeze_sha256':sha('freeze.json')}))
     rows=[];inputs=[]
     for i in range(300):
      gold=i%3;inputs.append({'id':str(i),'input_sha256':name+str(i)})
      rows.append({'id':str(i),'elapsed_ms':1,'raw':{'model_sha256':'test-only'},'decisions':[{'field':t,'gold':gold,'pred':gold,'labels':['meets','violates','insufficient_evidence'],'probabilities':[.98 if x==gold else .01 for x in range(3)],'accepted':gold==0,'review':gold==2} for t in ['refund','arrival','facility','activity']]})
     (folder/'travel-fresh-input-manifest.json').write_text(json.dumps(inputs));raw=''.join(json.dumps(r)+'\n' for r in rows)
     for engine in ['deberta-travel-v2','jev']:(folder/f'{engine}-travel-fresh.jsonl').write_text(raw)
    with patch('experiments.v2.promote.verify',return_value=True):
     with self.assertRaisesRegex(ValueError,'fails preregistered'):promote('freeze.json',['first','replica'])
    self.assertFalse(Path('models/active-model.json').exists())
   finally:os.chdir(before)

if __name__=='__main__':unittest.main()
