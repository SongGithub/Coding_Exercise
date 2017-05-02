#!/usr/bin/env python

# To remove CR characters from the file so that it can be an Executable file:
# Convert to UNIX:
# perl -pe 's/\r\n|\n|\r/\n/g'   inputfile > outputfile

"""this module orchestrates the sub modules to perform the task"""

from process_csv import ProcessCsvFile
import config.settings,os

tax_rate_file_path = os.path.join(
        settings.TAX_RATE_BACKUP_PATH,
        settings.TAX_RATE_DEFAULT_FILENAME
    )

csv_obj = ProcessCsvFile(settings.INPUT_PATH,settings.RESULT_DIR,tax_rate_file_path)
csv_obj.process_data()