from ..payslip_functions import *
import unittest


class test_payslip_functions(unittest.TestCase):

    def test_normal_case(self):
        self.assertEqual(number_cruncher(['a', 'b', '60050', '9', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 450))

    def test_negative_salary(self):
        self.assertEqual(number_cruncher(['a', 'b', '-60050', '9', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 450))

    def test_non_integer_salary(self):
        self.assertEqual(number_cruncher(['a', 'b', '60050.5', '9', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 450))

    def test_negative_non_integer_salary(self):
        self.assertEqual(number_cruncher(['a', 'b', '-60050.5', '9', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 450))

    def test_missing_salary(self):
        self.assertEqual(number_cruncher(['a', 'b', '9', '1/3/2016']), None)

    def test_missing_multiple_info(self):
        self.assertEqual(number_cruncher(['-60050.5', '9', '1/3/2016']), None)

    def test_invalid_super_rate(self):
        self.assertEqual(number_cruncher(['a', 'b', '-60050.5', '-1', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 0))
    def test_invalid_super_rate(self):
        self.assertEqual(number_cruncher(['a', 'b', '-60050.5', '51', '1/3/2016']), ('a b', 'March', 5004, 0, 5004, 0))


if __name__ == '__main__':
    unittest.main()