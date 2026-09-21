import unittest
from experiments.v2.breakdown import breakdown
class BreakdownTests(unittest.TestCase):
 def test_easy_fields_do_not_hide_focused_error(self):
  fields=['refund','arrival','facility','activity'];inputs=[{'id':'a','provenance':{'family':'scope','focus':'refund'}}]
  decisions=[{'field':f,'gold':0,'pred':1 if f=='refund' else 0,'labels':['meets','violates','unknown'],'accepted':f!='refund'} for f in fields]
  r=breakdown(inputs,[{'id':'a','decisions':decisions}])['groups']
  self.assertEqual(r['family/scope']['accuracy'],.75);self.assertEqual(r['focused_policy/scope']['accuracy'],0)
 def test_missing_cases_rejected(self):
  with self.assertRaises(ValueError):breakdown([{'id':'a'}],[])
if __name__=='__main__':unittest.main()
