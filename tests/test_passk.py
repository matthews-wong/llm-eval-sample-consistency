import unittest

from sample_eval.passk import pass_at_k, pass_pow_k


class PassAtKTest(unittest.TestCase):
    def test_k_one_is_the_plain_rate(self):
        self.assertAlmostEqual(pass_at_k(10, 3, 1), 0.3)

    def test_no_correct_samples(self):
        self.assertEqual(pass_at_k(5, 0, 3), 0.0)

    def test_all_correct_samples(self):
        self.assertEqual(pass_at_k(5, 5, 3), 1.0)

    def test_known_value(self):
        # 1 - C(3,2)/C(5,2) = 1 - 3/10
        self.assertAlmostEqual(pass_at_k(5, 2, 2), 0.7)

    def test_guaranteed_when_wrong_samples_fewer_than_k(self):
        self.assertEqual(pass_at_k(5, 3, 3), 1.0)

    def test_monotonic_in_k(self):
        values = [pass_at_k(8, 3, k) for k in range(1, 9)]
        self.assertEqual(values, sorted(values))


class PassPowKTest(unittest.TestCase):
    def test_k_one_is_the_plain_rate(self):
        self.assertAlmostEqual(pass_pow_k(10, 3, 1), 0.3)

    def test_known_value(self):
        # C(3,2)/C(5,2)
        self.assertAlmostEqual(pass_pow_k(5, 3, 2), 0.3)

    def test_zero_when_fewer_correct_than_k(self):
        self.assertEqual(pass_pow_k(5, 2, 3), 0.0)

    def test_never_above_pass_at_k(self):
        for c in range(0, 7):
            self.assertLessEqual(pass_pow_k(6, c, 3), pass_at_k(6, c, 3))


class ValidationTest(unittest.TestCase):
    def test_rejects_bad_counts(self):
        with self.assertRaisesRegex(ValueError, "correct count 6"):
            pass_at_k(5, 6, 1)

    def test_rejects_k_above_n(self):
        with self.assertRaisesRegex(ValueError, "k=4"):
            pass_pow_k(3, 1, 4)

    def test_rejects_k_zero(self):
        with self.assertRaisesRegex(ValueError, "k=0"):
            pass_at_k(3, 1, 0)


if __name__ == "__main__":
    unittest.main()
