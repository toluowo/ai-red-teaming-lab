import unittest

from testing.risk_classifier import classify_risk


class RiskClassifierTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(classify_risk(0), "Safe")
        self.assertEqual(classify_risk(4), "Low")
        self.assertEqual(classify_risk(5), "Medium")
        self.assertEqual(classify_risk(9), "Medium")
        self.assertEqual(classify_risk(10), "High")
        self.assertEqual(classify_risk(14), "High")
        self.assertEqual(classify_risk(15), "Critical")

    def test_negative_scores_are_rejected(self):
        with self.assertRaises(ValueError):
            classify_risk(-1)


if __name__ == "__main__":
    unittest.main()
