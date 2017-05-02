"""
    this module calculates varies of payslip numbers according to input
"""
import calendar,re
from tax_rate import TaxRate
from rounding import Rounding

# TODO: separate error and warning messages, and use proper logging,
# instead of using 'Print' for all

class Payslip(object):
    """docstring for Payslip"""
    def __init__(self, personal_info_set={}):
        super(Payslip, self).__init__()
        self.personal_info_set = personal_info_set

    def parse_date(self,date_string):
        try:
            month_number_list = (re.findall('/(\d+)/', date_string))
            month_number_int = int(month_number_list[0])
            return calendar.month_name[month_number_int]
        except IndexError:
            print 'month number out of range!'

    def calculate_payslip(self,calculated_tax=0):
        try:
            rounding = Rounding()
            pay_period = self.parse_date(self.personal_info_set['start_date'])
            annual_salary = self.personal_info_set['annual_salary']

            if annual_salary < 0:
                print "salary can't be negative number! auto-correcting..."
                annual_salary = abs(annual_salary)

            gross_income = rounding.dollar_rounding(annual_salary / 12)
            income_tax = rounding.dollar_rounding(calculated_tax / 12)
            net_income = gross_income - income_tax
            super_rate = float(self.personal_info_set['super_rate'])
            if super_rate < 0 or super_rate > 50:
                print 'super_rate out of range, auto-correcting'
                # when super_rate is out of range, assign a default value
                super_rate = 9
            superannuation = rounding.dollar_rounding(float(gross_income) * super_rate / 100)
            return self.personal_info_set['full_name'], pay_period, gross_income, income_tax, net_income, superannuation

        except ValueError:
            print 'information missing...'
