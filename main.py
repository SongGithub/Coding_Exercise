"""this module orchestrates the sub modules to perform the task"""

import sys, payslip_functions, calculate_tax_rates, process_csv, settings, sys, os
import datetime

csv_read_result = process_csv.read_csv(settings.INPUT_PATH)

tax_rates_instance = calculate_tax_rates.TaxRate('https://www.ato.gov.au/rates/individual-income-tax-rates/')

result_filename = 'result_' + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'
result_filepath = os.path.join(settings.RESULT_DIR, result_filename)
process_csv.write_csv_header(result_filepath)
for row in csv_read_result:
    print('\n', 'Previewing result for salary: ', row[2])
    print(payslip_functions.number_cruncher(row, tax_rates_instance.calculate_tax(float(row[2]))))

    process_csv.write_csv(
                          result_filepath,
                          payslip_functions.number_cruncher(row, tax_rates_instance.calculate_tax(float(row[2])))
                         )
