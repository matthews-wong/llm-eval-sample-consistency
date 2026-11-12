import unittest

from sample_eval.consistency import agreement, majority, majority_correct
from sample_eval.normalize import normalize


class NormalizeTest(unittest.TestCase):
    def test_case_space_and_edge_punctuation(self):
        self.assertEqual(normalize("  Paris. "), "paris")
        self.assertEqual(normalize("The   Answer\n is 4!"), "the answer is 4")

    def test_unicode_width(self):
        self.assertEqual(normalize("ＡＢＣ"), "abc")


class MajorityTest(unittest.TestCase):
    def test_counts_after_normalizing(self):
        self.assertEqual(majority(["Paris", "paris.", "Lyon"]), ("paris", 2))

    def test_tie_goes_to_first_seen(self):
        self.assertEqual(majority(["b", "a"]), ("b", 1))

    def test_empty_is_an_error(self):
        with self.assertRaises(ValueError):
            majority([])


class AgreementTest(unittest.TestCase):
    def test_unanimous(self):
        self.assertEqual(agreement(["x", "X", "x."]), 1.0)

    def test_split(self):
        self.assertAlmostEqual(agreement(["a", "a", "b", "c"]), 0.5)

    def test_all_different_is_one_over_n(self):
        self.assertAlmostEqual(agreement(["a", "b", "c", "d"]), 0.25)


class MajorityCorrectTest(unittest.TestCase):
    def test_correct_majority(self):
        self.assertTrue(majority_correct("Paris", ["paris", "Paris", "Lyon"]))

    def test_wrong_majority_even_if_one_sample_is_right(self):
        self.assertFalse(majority_correct("Paris", ["Lyon", "lyon", "Paris"]))


if __name__ == "__main__":
    unittest.main()
