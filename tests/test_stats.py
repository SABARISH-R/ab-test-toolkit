import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from abkit.simulate import empirical_power, peeking_false_positive_rate  # noqa: E402
from abkit.stats import (bonferroni_alpha, sample_size_per_group, srm_check,  # noqa: E402
                         two_proportion_test)


class SampleSizeTests(unittest.TestCase):
    def test_known_value(self):
        # 10% -> 12%, alpha 0.05 two-sided, power 0.8: hand calculation gives about 3841
        self.assertTrue(3835 <= sample_size_per_group(0.10, 0.02) <= 3850)

    def test_smaller_effect_needs_more_users(self):
        self.assertGreater(sample_size_per_group(0.10, 0.01), sample_size_per_group(0.10, 0.02))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            sample_size_per_group(0.99, 0.05)


class TestStatTests(unittest.TestCase):
    def test_two_proportion_hand_calculation(self):
        r = two_proportion_test(200, 2000, 260, 2000)
        self.assertAlmostEqual(r.z, 2.974, places=2)
        self.assertTrue(r.significant)
        self.assertAlmostEqual(r.abs_lift, 0.03)
        self.assertLess(r.ci_low, r.abs_lift)
        self.assertGreater(r.ci_high, r.abs_lift)

    def test_no_difference_is_not_significant(self):
        r = two_proportion_test(100, 1000, 100, 1000)
        self.assertFalse(r.significant)
        self.assertAlmostEqual(r.p_value, 1.0)

    def test_srm(self):
        self.assertAlmostEqual(srm_check(5000, 5000)[1], 1.0)
        self.assertLess(srm_check(5200, 4800)[1], 0.001)

    def test_bonferroni(self):
        self.assertAlmostEqual(bonferroni_alpha(0.05, 5), 0.01)


class SimulationTests(unittest.TestCase):
    def test_power_close_to_target(self):
        n = sample_size_per_group(0.10, 0.02)
        self.assertAlmostEqual(empirical_power(n, 0.10, 0.02, sims=4000), 0.80, delta=0.04)

    def test_peeking_inflates_false_positives(self):
        one = peeking_false_positive_rate(1500, looks=1, sims=3000)
        many = peeking_false_positive_rate(1500, looks=10, sims=3000)
        self.assertAlmostEqual(one, 0.05, delta=0.02)
        self.assertGreater(many, one + 0.05)


if __name__ == "__main__":
    unittest.main()
