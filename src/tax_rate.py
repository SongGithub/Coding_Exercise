# -*- coding: utf-8 -*-
"""
 This module is developed for calculate tax rate.
 Author: Song Jin 2016
"""
import json, os
from rounding import Rounding
import settings

class TaxRate(object):
    """
        Loads Tax rate from varies sources.
        Current source is a local json file.
        sources could include web-scraping results or APIs
    """

    def __init__(self, tax_rate_file_path):
        """
        Args:
            input(tax_rate_file_path): path to default/backup tax rate file
            output(result): contains taxable_income_bracket, and
            corresponding tax rate
        """
        self._tax_rate_file_path = tax_rate_file_path
        result = self.__get_taxrate_local_json__()
        self._taxrate_list = result

    def __get_taxrate_local_json__(self):
        tax_rate_file_path = self._tax_rate_file_path
        try:
            with open(tax_rate_file_path) as data_file:
                data = json.load(data_file)
            return data

        except IOError as e:
            print "Program can't proceed without tax rate!({0}): {1}".format(
                e.errno, e.strerror
                )
            return None

    def get_taxrate(self):
        return self._taxrate_list

    def calculate_tax(self,salary):
        """calculate_tax according to input tax rate table
        Args:
            salary: individual salary for calculation
        """

        if salary < 0:
            print "salary can't be negative number! auto-correcting..."
            salary = abs(salary)
        accumulated_base_tax_amt = 0
        if salary < 0:
            tax = 0
            return tax

        current_tax_rate = []
        for rate in self._taxrate_list:
            if rate['financial_year'] == settings.TAX_RATE_FINANCIAL_YEAR:
                current_tax_rate = rate['brackets']

        # loop above goes through lower-boundary of a tax bracket, trying
        # to see which lower-boundary just exceed
        # the figure of the 'salary'. Then the index of match tax bracket
        # can be calculated by (current index - 1)
        for i in range(0, len(current_tax_rate)):
            if i >= 2:
                accumulated_base_tax_amt += current_tax_rate[i-2][u'rate'] * (
                        current_tax_rate[i-1][u'low_end'] - current_tax_rate[i-2][u'low_end']
                    )
            if salary < current_tax_rate[i][u'low_end']:
                # 'tax range located by now!'
                break
        rounding = Rounding()
        tax = rounding.dollar_rounding(
                current_tax_rate[i-1][u'rate'] *
                (salary - current_tax_rate[i-1][u'low_end']) +
                accumulated_base_tax_amt
            )
        return tax
