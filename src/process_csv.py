"""
    this module handles all file operations
"""
from employee import Employee
from tax_rate import TaxRate
from payslip import Payslip
import csv,settings,datetime,os


class ProcessCsvFile(object):
    """
    The Class is designed to close read file thread gracefully
    """
    def __init__(self, input_filename, output_filepath,tax_filepath):
        self._input_filename = input_filename
        self._output_filepath = output_filepath
        self._tax_filepath = tax_filepath
        self._input_object = None
        self._headers = []

    def read_csv(self):
        """read csv file content then return a list of dictionaries'"""
        try:
            f_obj = open(self._input_filename, 'rU')
            reader = csv.reader(f_obj)
            # following section skips the header row
            has_header = csv.Sniffer().has_header(f_obj.readline())
            f_obj.seek(0)  # rewind
            incsv = csv.reader(f_obj)
            if has_header:
                self._headers = keys = reader.next()
            self._input_object = f_obj
            return {'keys':keys, 'reader':reader}

        except IOError as e:
            print "I/O error({0}): {1}".format(
                e.errno, e.strerror
                )

    def assemble_read_results(self,reader_obj):
        """assemble reader result from passed in object"""
        keys = reader_obj['keys']
        reader = reader_obj['reader']
        rows = []
        for row in reader:
            dic = {}
            # fiels-size integrity control:
            # if any field is missing from the input row, or extra field exists
            # then the this row is ignored.
            if len(keys) == len(row):
                for i in range(len(keys)):
                    dic[keys[i]] = row[i]
                rows.append(dic)
        return rows

    def close_csv(self):
        self._input_object.close()

    def write_csv_header(self):
        """write csv header with pre-defined content
        Args:
            filename as input
        """

        with open(self._output_filepath, 'w') as f_obj:
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
        with open(self._output_filepath, 'a') as f_obj:

            writer = csv.writer(
                f_obj, delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
                )
            writer.writerow(content)

    def prepare_result_file(self):
        """
            The result file name needs to be calculated on the spot and time-stamped
            on the filename in order to avoid conflict on file name.
        """
        result_filename = 'result_' + str(
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + '.csv'
        self._output_filepath = os.path.join(self._output_filepath,result_filename)

    def process_data(self):
        """process data according to param loaded"""
        tax_object = TaxRate(self._tax_filepath)
        csv_reader_object = self.read_csv()
        csv_read_results = self.assemble_read_results(csv_reader_object)
        self.prepare_result_file()
        self.write_csv_header()

        if csv_read_results != False:
            for person in csv_read_results:
                emp = Employee(person)
                tax = tax_object.calculate_tax(emp.get_salary())
                payslip = Payslip(emp.get_personal_info())
                individual_payslip = payslip.calculate_payslip(tax)
                print individual_payslip
                # write actual content to the file
                self.write_csv(individual_payslip)

        self.close_csv()
