import unittest
from experiments.v2.paired_report import compare


def row(i, pred, gold=0):
    return {'id': str(i), 'elapsed_ms': 1, 'decisions': [
        {'field': 'refund', 'labels': ['meets', 'violates', 'unknown'], 'gold': gold,
         'pred': pred, 'probabilities': [.98,.01,.01] if pred == 0 else [.01,.98,.01],
         'accepted': pred == 0, 'review': pred is None}]}


class PairedReportTests(unittest.TestCase):
    def test_identical_engines_cannot_win(self):
        rows = [row(i, i%3, i%3) for i in range(30)]
        r = compare(rows, rows)
        self.assertEqual(r['paired_accuracy_difference_ci95'], [0, 0])
        self.assertFalse(r['round_qualifies'])

    def test_failure_counts_as_wrong(self):
        local = [row(i, i%3, i%3) for i in range(30)]
        remote = [row(i, None, i%3) for i in range(30)]
        self.assertEqual(compare(local, remote)['paired_accuracy_difference'], 1)

    def test_mismatched_gold_and_missing_rows_rejected(self):
        with self.assertRaises(ValueError): compare([row(1,0)], [row(1,0,1)])
        with self.assertRaises(ValueError): compare([row(1,0)], [row(2,0)])

    def test_false_accept_gate_cannot_be_hidden_by_accuracy(self):
        local = [row(i, 0, 1 if i < 10 else 0) for i in range(100)]
        remote = [row(i, None, 1 if i < 10 else 0) for i in range(100)]
        r = compare(local, remote)
        self.assertFalse(r['gates']['false_accept_rate_at_most_005'])

    def test_tiny_acceptance_coverage_cannot_qualify(self):
        local=[row(i,i%3,i%3) for i in range(30)]
        for r in local:r['decisions'][0]['accepted']=r['id']=='0'
        remote=[row(i,None,i%3) for i in range(30)]
        r=compare(local,remote)
        self.assertTrue(r['gates']['false_accept_rate_at_most_005'])
        self.assertFalse(r['gates']['gold_meets_acceptance_recall_at_least_half'])
        self.assertFalse(r['round_qualifies'])


if __name__ == '__main__': unittest.main()
