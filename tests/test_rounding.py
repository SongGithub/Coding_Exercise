from src.rounding import Rounding
import unittest

class TestRounding(unittest.TestCase):

    def test_dollar_rounding(self):
        instance = Rounding()
        self.assertEqual(instance.dollar_rounding(2.47),2)
        self.assertEqual(
            instance.dollar_rounding(2.51),
            3,
            "it should round up once sub-dollar value exceeds 50 cent"
            )

        self.assertEqual(instance.dollar_rounding(0.49),0)
        self.assertEqual(
            instance.dollar_rounding(0.51),
            1,
            "it should round up once sub-dollar value exceeds 50 cent"
            )