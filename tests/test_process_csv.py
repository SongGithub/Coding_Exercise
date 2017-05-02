#!/usr/bin/python

from src.process_csv import ProcessCsvFile
from src.tax_rate import TaxRate
from src.employee import Employee
from payslip import Payslip

import os,settings,datetime
import unittest,string,random,csv


class NewDate(datetime.datetime):
    """overwrite original method to mock """
    @classmethod
    def now(cls):
        return cls(2010,1,1,12,12,12)

class TestProcessCSV(unittest.TestCase):
    """testing methods within processCSV class"""

    def setUp(self):

        tax_rate_file_path = os.path.join(
            settings.TAX_RATE_BACKUP_PATH,
            settings.TAX_RATE_DEFAULT_FILENAME
        )

        input_filepath = os.path.join(settings.TEST_FIXTURE_DIR,'valid_inputs.csv')
        self.instance = ProcessCsvFile(input_filepath,settings.TEST_FIXTURE_DIR,tax_rate_file_path)
        datetime.datetime = NewDate
        print datetime.datetime.now()

        test_name = self.shortDescription()
        print 'outstanding test = ', test_name

    def tearDown(self):
        """remove generated result files during the tests."""
        path = settings.TEST_FIXTURE_DIR
        for root, dirs, files in os.walk(path):
            for currentFile in files:
                print "processing file: " + currentFile
                exts = ('result')
                if any(currentFile.lower().startswith(ext) for ext in exts):
                    os.remove(os.path.join(root, currentFile))

    def test_read_csv(self):
        """load_csv"""
        read_result = self.instance.read_csv()
        readerObject = read_result['reader']
        self.assertTrue(str(type(readerObject)), "_csv.reader")
            # "reader object should exist given the valid file path"

        keys = read_result['keys']
        self.assertEqual(
                keys,
                ['first_name', 'last_name', 'annual_salary', 'super_rate', 'start_date'],
                "keys read from csv headers should contains the 5 elements in the list"
            )

    def generate_random_string(self,size=6,chars=string.ascii_uppercase + string.digits):
        """utility module to generate random string """
        return ''.join(random.choice(chars) for _ in range(size))

    def test_read_non_existing_csv(self):
        """Expect an error when path to csv is invalid"""
        self.instance._input_filename = os.path.join(self.instance._input_filename,self.generate_random_string())
        self.assertRaises(IOError,self.instance.read_csv(),"reader object should exist given the valid file path")

    def test_assemble_read_results(self):
        """it should allocate values to coresponding columns"""
        reader = self.instance.read_csv()
        result = self.instance.assemble_read_results(reader)
        self.assertEqual(len(result),2)
        self.assertEqual(
            result[0],
                {
                    'annual_salary': '60050',
                    'first_name': 'David',
                    'last_name': 'Rudd',
                    'start_date': '1/3/16',
                    'super_rate': '9'
                }
            )
        self.assertEqual(
            result[1],
                {
                    'annual_salary': '120000',
                    'first_name': 'Ryan',
                    'last_name': 'Chen',
                    'start_date': '2/4/16',
                    'super_rate': '10'
                }
            )


    def test_assemble_read_results_reject_imcomplete_rows(self):
        """it should reject if number of values is less than keys - (value missing)"""
        self.instance._input_filename = os.path.join(settings.TEST_FIXTURE_DIR,'invalid_inputs.csv')
        reader = self.instance.read_csv()
        result = self.instance.assemble_read_results(reader)
        self.assertEqual(len(result),1,"it should reject rows with imcomplete info")
        self.assertEqual(
            result[0],
                {
                    'annual_salary': '60050',
                    'first_name': 'David',
                    'last_name': 'Rudd',
                    'start_date': '1/3/16',
                    'super_rate': '9'
                }
            )
        self.assertNotIn(
                {
                   'annual_salary': '120000',
                    'first_name': 'Ryan',
                    'last_name': 'Chen',
                    'start_date': '2/4/16',
                    'super_rate': '10'
                },
                result,
                "when one field is missing from the set, such as salary, the row should be discarded"
            )

    def test_close_csv(self):
        """reader object should not exist after it has been closed"""
        # do something to open the file
        self.instance.read_csv()
        self.instance.close_csv()
        f_obj = self.instance._input_object
        self.assertTrue(f_obj,'closed')

    def test_write_csv_header_exists(self):
        """ verify if the file has been created"""
        self.instance.prepare_result_file()
        self.instance.write_csv_header()
        self.assertTrue(os.path.exists(self.instance._output_filepath))

    def test_write_csv_header_correct_content(self):
        """ verify if the file has been created with correct content"""
        self.instance.prepare_result_file()
        self.instance.write_csv_header()

        f_obj = open(self.instance._output_filepath, 'rU')
        reader = csv.reader(f_obj)
        # following section skips the header row
        has_header = csv.Sniffer().has_header(f_obj.readline())
        f_obj.seek(0)  # rewind
        incsv = csv.reader(f_obj)
        if has_header:
            keys= reader.next()
        self.assertEqual(keys,['full name','pay period','gross income','income tax','net income','superannuation'])

    def test_write_csv(self):
        """verify if cargo data "Content" has been written into the file."""
        self.instance.prepare_result_file()
        self.instance.write_csv_header()
        self.instance.write_csv(('Ryan.Chen', 'April', '10000', '2696', '7304', '1000'))
        f_obj = open(self.instance._output_filepath, 'rU')
        reader = csv.reader(f_obj)
        # following section skips the header row
        has_header = csv.Sniffer().has_header(f_obj.readline())
        f_obj.seek(0)  # rewind
        incsv = csv.reader(f_obj)
        if has_header:
            keys= reader.next()
        rows = []
        for row in reader:
            for i in range(len(keys)):
                rows.append(row[i])

        self.assertEqual(rows,['Ryan.Chen', 'April', '10000', '2696', '7304', '1000'])


    def test_prepare_result_file(self):
        """it should concat result file name with current date-time"""
        self.instance.prepare_result_file()
        self.assertEqual(self.instance._output_filepath, os.path.join(settings.TEST_FIXTURE_DIR,'result_20100101_121212.csv'))

    def test_process_data(self):
        """can be treated as an integration test"""
        self.instance.process_data()
        f_obj = open(self.instance._input_filename, 'rU')
        reader = csv.reader(f_obj)
        # following section skips the header row
        has_header = csv.Sniffer().has_header(f_obj.readline())
        f_obj.seek(0)  # rewind
        incsv = csv.reader(f_obj)
        if has_header:
            keys = reader.next()
        rows = []
        for row in reader:
            person_info = []
            for i in range(len(keys)):
                person_info.append(row[i])
            rows.append(person_info)
        print rows
        self.assertEqual(rows,[['David', 'Rudd', '60050', '9', '1/3/16'], ['Ryan', 'Chen', '120000', '10', '2/4/16']])


