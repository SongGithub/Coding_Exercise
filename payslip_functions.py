"""this module calculate varies of payslip numbers according to input"""

import calendar
import re

from calculate_tax_rates import TaxRate


def parse_date(date_string):
    try:
        month_number_list = (re.findall('/(\d+)/', date_string))
        month_number_int = int(month_number_list[0])
        month_name = calendar.month_name[month_number_int]
        return month_name
    except IndexError:
        print 'month number out of range!'

def RepresentsInt(str):
    """helper function telling if the str represents an integer"""
    try: 
        int(str)
        return True
    except ValueError:
        return False

def number_cruncher(personal_info_set, calculated_tax=0):

    f_name, l_name, annual_salary, super_rate, pay_start_date = personal_info_set
    name = f_name + ' ' + l_name
    pay_period = parse_date(pay_start_date)
    if RepresentsInt(annual_salary) == False:
        #annual_salary = 0
        print 'salary must be integer! auto-rounding'
        annual_salary = int(round(float(annual_salary)))
    if float(annual_salary) < 0:
        print "salary can't be negative number! auto-correcting..."
        annual_salary = abs(int(round(float(annual_salary))))
    gross_income = int(round(float(annual_salary) / 12))
    income_tax = int(round(calculated_tax / 12))
    net_income = gross_income - income_tax
    if float(super_rate) < 0 or float(super_rate) >50:
        print 'super_rate out of range, auto-correcting'
        super_rate = 0
    superannuation = int(round(float(gross_income) * float(super_rate) / 100))

    return name, pay_period, gross_income, income_tax, net_income, superannuation
