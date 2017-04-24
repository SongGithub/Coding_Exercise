# -*- coding: utf-8 -*-
"""
 This module is developed for calculate tax rate.
 Author: Song Jin 2016
"""

import requests, re, json, datetime, os, settings


class TaxRate(object):
    """the class includes all sorts of methods to calculate tax"""

    def __get_taxrate_local_json__(self, tax_rate_file_path):
        tax_rate_file_path = os.path.join(
                settings.TAX_RATE_BACKUP_PATH,
                settings.TAX_RATE_DEFAULT_FILENAME
            )
        print 'reading taxrate from local json' + tax_rate_file_path

        try:
            with open(tax_rate_file_path) as data_file:
                data = json.load(data_file)
            return data

        except IOError as e:
            print "Program can't proceed without tax rate!({0}): {1}".format(
                e.errno, e.strerror
                )
            return None

    def __init__(self, tax_rate_file_path):
        """init with generation of tax rate base on ATO offical page's data
        Args:
            input(tax_rate_file_path): path to default/backup tax rate file
            output(result): contains taxable_income_bracket, and
            corresponding tax rate
        """
        self._tax_rate_file_path = tax_rate_file_path
        result = self.__get_taxrate_local_json__(tax_rate_file_path)

        self._taxrate_list = result

    def get_taxrate(self):
        return self._taxrate_list

    def get_tax_rate_file_path(self):
        return self._tax_rate_file_path

    def calculate_tax(self, salary):
        """calculate_tax according to input tax rate table
        Args:
            salary: individual salary for calculation
        """
        accumulated_base_tax_amt = 0
        for key, value in self._taxrate_list[settings.TAX_RATE_FINANCIAL_YEAR].items():
            for i in range(0, len(value)):
                if i >= 2:
                    accumulated_base_tax_amt += value[i-2][u'rate'] * (
                        value[i-1][u'low_end'] - value[i-2][u'low_end']
                        )
                if salary < value[i][u'low_end']:
                    # 'tax range located by now!'
                    break
            tax = round(
                value[i-1][u'rate'] *
                (salary - value[i-1][u'low_end']) +
                accumulated_base_tax_amt
                )
        return tax
        # loop above goes through lower-boundary of a tax bracket, trying
        # to see which lower-boundary just exceed
        # the figure of the 'salary'. Then the index of match tax bracket
        # can be calculated by (current index - 1)
