"""this module calculate varies of payslip numbers according to input"""

import calendar
import re

from calculate_tax_rates import TaxRate


def parse_date(date_string):

    month_number_list = (re.findall('/(\d+)/', date_string))
    month_number_int = int(month_number_list[0])
    month_name = calendar.month_name[month_number_int]
    return month_name


def number_cruncher(personal_info_set, calculated_tax):
    f_name, l_name, annual_salary, super_rate, pay_start_date = personal_info_set
    name = f_name + ' ' + l_name
    pay_period = parse_date(pay_start_date)
    gross_income = int(round(float(annual_salary) / 12))
    income_tax = int(round(calculated_tax / 12))
    net_income = gross_income - income_tax
    superannuation = int(round(float(gross_income) * float(super_rate) / 100))

    return name, pay_period, gross_income, income_tax, net_income, superannuation

if __name__ == '__main__':
    tax_instance = TaxRate('https://www.ato.gov.au/rates/individual-income-tax-rates/')
    print(
          number_cruncher(
                          ['Kevin', 'Rudd', '60050', '9', '01/03/2016'],
                          tax_instance.calculate_tax(60050)
                          )
          )

