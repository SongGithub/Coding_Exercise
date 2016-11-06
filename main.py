"""this module orchestrates the sub modules to perform the task"""

import sys
import payslip_functions
import calculate_tax_rates
import process_csv
import settings
#
print(settings.INPUT_PATH)
print(settings.OUTPUT_PATH)
read_result = process_csv.read_csv(settings.INPUT_PATH)
process_csv.write_csv_header(settings.OUTPUT_PATH)
tax_rates_instance = calculate_tax_rates.TaxRate('https://www.ato.gov.au/rates/individual-income-tax-rates/')

for row in read_result:
    print('\n', 'Previewing result for salary: ', row[2])
    print(payslip_functions.number_cruncher(row, tax_rates_instance.calculate_tax(float(row[2]))))
    process_csv.write_csv(
                          settings.OUTPUT_PATH,
                          payslip_functions.number_cruncher(row, tax_rates_instance.calculate_tax(float(row[2])))
                         )
