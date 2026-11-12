import unittest

from sample_eval.dataset import Case
from sample_eval.scoring import score_case, summarize


class ScoreCaseTest(unittest.TestCase):
    def test_counts_correct_after_normalizing(self):
        score = score_case(Case("a", "Paris", ["paris", "Paris.", "Lyon"]), k=2)
        self.assertEqual((score.n, score.correct), (3, 2))

    def test_majority_can_be_right_while_pass_pow_k_is_not_one(self):
        score = score_case(Case("a", "x", ["x", "x", "y"]), k=2)
        self.assertTrue(score.majority_correct)
        self.assertAlmostEqual(score.pass_pow_k, 1 / 3)

    def test_k_above_n_is_rejected(self):
        with self.assertRaises(ValueError):
            score_case(Case("a", "x", ["x", "y"]), k=3)


class SummarizeTest(unittest.TestCase):
    def test_means_over_cases(self):
        scores = [
            score_case(Case("a", "x", ["x", "x"]), k=2),
            score_case(Case("b", "x", ["y", "y"]), k=2),
        ]
        summary = summarize(scores)
        self.assertEqual(summary["pass@1"], 0.5)
        self.assertEqual(summary["pass^k"], 0.5)
        self.assertEqual(summary["agreement"], 1.0)
        self.assertEqual(summary["majority"], 0.5)


if __name__ == "__main__":
    unittest.main()
