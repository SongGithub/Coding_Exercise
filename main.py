"""this module orchestrates the sub modules to perform the task"""

import sys, payslip_functions, calculate_tax_rates, process_csv, settings, sys, os
import datetime
from process_csv import ProcessCsvFile

tax_calculation = calculate_tax_rates.TaxRate(
													settings.TAX_RATE_ATO_ADDRESS,
													settings.TAX_RATE_BACKUP_PATH
												)
result_filename = 'result_' + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'
result_filepath = os.path.join(settings.RESULT_DIR, result_filename)
# result file name needs to be calculated on the spot and timestamped on the filename
# in order to avoid conflict on file name.

csv_obj = ProcessCsvFile(settings.INPUT_PATH,result_filepath)
csv_read_result = csv_obj.read_csv()
csv_obj.write_csv_header()

for row in csv_read_result:
    csv_obj.write_csv(
                          payslip_functions.number_cruncher(row, tax_calculation.calculate_tax(float(row[2])))
                	)
csv_obj.close_csv()
