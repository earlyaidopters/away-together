import json
import unittest
import httpx
from experiments.diffusion.engine import DiffusionEngine

class AdapterTests(unittest.TestCase):
    def run_response(self, answer, questions=None):
        questions = questions or [{'id':'refund','question':'Refund?', 'candidates':['Cash','Voucher','Unknown'],'gold':0}]
        def handler(request):
            payload=json.loads(request.content)
            self.assertNotIn('gold',payload['questions']['refund'])
            self.assertEqual(payload['samples'],1)
            self.assertEqual(payload['state'],'Document')
            self.assertEqual(list(payload['questions']['refund']['criteria']),['option_0','option_1','option_2'])
            return httpx.Response(200,json={'model':'dgemma','answers':{'refund':answer}})
        client=httpx.Client(transport=httpx.MockTransport(handler))
        return DiffusionEngine('http://127.0.0.1:8999',client=client).predict('Document',questions)

    def test_choice_mapping_uses_candidate_order(self):
        r=self.run_response({'choice':'option_1','probabilities':{'option_2':.1,'option_0':.2,'option_1':.7}})
        self.assertEqual(r['answers'][0]['choice'],1)
        self.assertEqual(r['answers'][0]['probabilities'],[.2,.7,.1])

    def test_malformed_distributions_rejected(self):
        for p in [float('nan'),float('inf'),-.1,1.2]:
            with self.subTest(p=p), self.assertRaises(ValueError):
                self.run_response({'choice':'option_0','probabilities':{'option_0':p,'option_1':.2,'option_2':.1}})

    def test_conflicting_choice_rejected(self):
        with self.assertRaises(ValueError):
            self.run_response({'choice':'option_0','probabilities':{'option_0':.1,'option_1':.8,'option_2':.1}})

    def test_sampling_lanes_explicit(self):
        with self.assertRaises(ValueError):DiffusionEngine('http://localhost',samples='auto')

if __name__=='__main__':unittest.main()
