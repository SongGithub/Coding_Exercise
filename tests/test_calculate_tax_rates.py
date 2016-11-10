from ..calculate_tax_rates import *
import unittest


class TestTaxRate(unittest.TestCase):
	"""docstring for TestTaxRate
"""

	def test_getting_tax_rate(self):
		instance = TaxRate(
							settings.TAX_RATE_ATO_ADDRESS, 
							settings.TAX_RATE_BACKUP_PATH
							)
		self.assertEqual(
			instance.get_taxrate(), 
			[{"Tax rates 2016-17": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 87001.0}, {"rate": 0.45, "low_end": 180001.0}]}, 
			{"Tax rates 2015-16": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 80001.0}, 
			{"rate": 0.45, "low_end": 180001.0}]}]
			)

	def test_get_taxrate_online__(self):
		instance = TaxRate(
							settings.TAX_RATE_ATO_ADDRESS, 
							settings.TAX_RATE_BACKUP_PATH
							)
		self.assertEqual(
			instance.__get_taxrate_online__(instance.get_ato_addr()),
			[{"Tax rates 2016-17": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 87001.0}, {"rate": 0.45, "low_end": 180001.0}]}, 
			{"Tax rates 2015-16": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 80001.0}, 
			{"rate": 0.45, "low_end": 180001.0}]}]
			)

	def test_get_taxrate_local_json__(self):
		instance = TaxRate(
							settings.TAX_RATE_ATO_ADDRESS, 
							settings.TAX_RATE_BACKUP_PATH
							)
		self.assertEqual(
			instance.__get_taxrate_local_json__(instance.get_tax_rate_file_path()),
			[{"Tax rates 2016-17": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 87001.0}, {"rate": 0.45, "low_end": 180001.0}]}, 
			{"Tax rates 2015-16": [{"rate": 0.0, "low_end": 0.0}, {"rate": 0.19, "low_end": 18201.0}, 
			{"rate": 0.325, "low_end": 37001.0}, {"rate": 0.37, "low_end": 80001.0}, 
			{"rate": 0.45, "low_end": 180001.0}]}]
			)

	def test_calculate_tax(self):
		instance = TaxRate(
							settings.TAX_RATE_ATO_ADDRESS, 
							settings.TAX_RATE_BACKUP_PATH
							)
		self.assertEqual(
			instance.calculate_tax(18200),0
			)
		self.assertEqual(
			instance.calculate_tax(36999),3572
			)
		self.assertEqual(
			instance.calculate_tax(79999),17546
			)
		self.assertEqual(
			instance.calculate_tax(179999),54546
			)


if __name__ == '__main__':
	unittest.main()