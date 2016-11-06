#!/usr/bin/python
"""this module handles all file operations"""
import csv
import settings

def read_csv(filename):
    """read csv file content then output the 'reader object'"""
    f_obj = open(filename, 'r')
    reader = csv.reader(f_obj)
    #following section skips the header row
    has_header = csv.Sniffer().has_header(f_obj.read(1024))
    f_obj.seek(0)  # rewind
    incsv = csv.reader(f_obj)
    if has_header:
        next(incsv)  # skip header row
    return reader


def write_csv_header(filename):
    """write csv header with pre-defined content
    Args:

        filename as input
    """

    with open(filename, 'w') as f_obj:
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


def write_csv(filename, content):
    """write a csv file with intended content"""
    with open(filename, 'a') as f_obj:

        writer = csv.writer(
            f_obj, delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
            )
        writer.writerow(content)

if __name__ == '__main__':
    write_csv(settings.OUTPUT_PATH, ('Rudd', 'March', 5004, 922, 4082, 450))
