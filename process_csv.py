#!/usr/bin/python
"""this module handles all file operations"""
import csv
import settings


class ProcessCsvFile(object):
    """
    The Class is designed to close read file thread gracefully
    """
    def __init__(self, input_filename, output_filename):
        self._input_filename = input_filename
        self._output_filename = output_filename
        self._input_object = None


    def read_csv(self):
        """read csv file content then output the 'reader object'"""
        f_obj = open(self._input_filename, 'rU')
        reader = csv.reader(f_obj)
        #following section skips the header row
        has_header = csv.Sniffer().has_header(f_obj.read(1024))
        f_obj.seek(0)  # rewind
        incsv = csv.reader(f_obj)
        if has_header:
            next(incsv)  # skip header row
        self._input_object = f_obj
        return reader

    def close_csv(self):
        self._input_object.close()

    def write_csv_header(self):
        """write csv header with pre-defined content
        Args:

            filename as input
        """

        with open(self._output_filename, 'w') as f_obj:
            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
                )

            writer.writerow(
                            [
                                'full name',
                                'pay period',
                                'gross income',
                                'income tax',
                                'net income',
                                'superannuation',
                            ]
                              )
        
    def write_csv(self, content):
        """write a csv file with intended content"""
        with open(self._output_filename, 'a') as f_obj:

            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
                )
            writer.writerow(content)
        f_obj.close()
