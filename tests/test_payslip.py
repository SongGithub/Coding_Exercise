from src.payslip import Payslip
from src.employee import Employee
from src.tax_rate import  TaxRate
import os,settings,unittest,json


class test_payslip_functions(unittest.TestCase):

    def load_fixtures(self):
        path = os.path.join(settings.TEST_FIXTURE_DIR,'fixture_payslip.json')
        try:
            with open(path) as data_file:
                data = json.load(data_file)
            return data

        except IOError as e:
            print "Program can't proceed without the fixture!({0}): {1}".format(
                e.errno, e.strerror
                )
            return None

    def setUp(self):
        test_name = self.shortDescription()
        # load specific test fixture according to test routine's ShortDescription
        emp = Employee(self.load_fixtures()[test_name])
        person_info_set = emp.get_personal_info()
        self.inst = Payslip(person_info_set)
        tax_rate_file_path = os.path.join(
            settings.TAX_RATE_BACKUP_PATH,
            settings.TAX_RATE_DEFAULT_FILENAME)

        self.tax = TaxRate(tax_rate_file_path).calculate_tax(emp.get_salary())


    def test_normal_case(self):
        """normal"""
        self.assertEqual(self.inst.calculate_payslip(
            self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )

    def test_negative_salary(self):
        """negative_salary"""
        self.assertEqual(self.inst.calculate_payslip(
            self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )

    def test_non_integer_salary(self):
        """non_integer_salary"""
        self.assertEqual(self.inst.calculate_payslip(self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )

    def test_negative_non_integer_salary(self):
        """negative_non_integer_salary"""
        self.assertEqual(self.inst.calculate_payslip(self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )

    def test_nagative_super_rate(self):
        """nagative_super_rate"""
        self.assertEqual(self.inst.calculate_payslip(self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )

    def test_excessive_super_rate(self):
        """excessive_super_rate"""
        self.assertEqual(self.inst.calculate_payslip(self.tax),
            ('John.Smith', 'January', 5001,921,4080,450)
            )