# -*- coding: utf-8 -*-
"""
#This module is developed for calculate tax rate, including web scraping the
ATO individual tax rate table
# Author: Song Jin 2016
#Ref: http://docs.python-guide.org/en/latest/scenarios/scrape/
#Specialised knowledge: XPath
"""
from lxml import html
import requests, re, json, settings, datetime, os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Suppress InsecureRequestWarning: Unverified HTTPS request is being made
# in Python2.6 (credit: StackOverflow)


class TaxRate(object):
    """the class includes all sorts of methods to calculate tax"""

    def __get_taxrate_online__(self, ato_url):
        page = requests.get(ato_url, verify=False)
        if page.status_code != 200:
            # in case the site is down
            print 'WEBSITE NOT READY'
            return -1
        else:
            tree = html.fromstring(page.content)
            result = []
            RESIDENT_TABLE_AMT = 2
            for table_num in range(1, RESIDENT_TABLE_AMT+1):
                tax_table_title_temp = str(
                                            tree.xpath('//*[@id="main-content"]/section/div[2]/div/article/div[1]/div/h3[' + str(table_num) + ']/text()')
                                        )
                tax_table_title = "".join(
                        re.findall(
                            r"[^[^'^\]^u]",
                            tax_table_title_temp.replace('\u2013', '-')
                            )
                    )
                tax_table_dics = []
                for i in range(2, 7):
                    taxable_income_range = tree.xpath(
                            (
                                '//*[@id="main-content"]/section/div[2]/div/'
                                'article/div[1]/div/table['
                            ) +
                            str(table_num)+']/tbody/tr[' +
                            str(i)+']/td[1]/p/text()')
                    # take info about low & high end boundary of
                    # the taxable income bracket
                    target_webcontent_string = str(taxable_income_range)

                    if len(taxable_income_range) == 0:
                        print 'breaking due to website out of order'
                        return -1
                        # in case the site is still on but particular service
                        # is out of order
                    else:
                        transformed_webcontent_string_A = target_webcontent_string.replace('over', ' - 999,999')
                        # normalisation: replace 'over' with numeric value
                        transformed_webcontent_string_B = transformed_webcontent_string_A.replace(',', '')
                        # normalisation: remove comma
                        transformed_webcontent_string_C = transformed_webcontent_string_B.replace('\u2013', '')
                        # normalisation: remove dash
                        boarder_list = re.findall(r"(\d+)", transformed_webcontent_string_C)
                        lower_boundary_tax_bracket = [float(x) for x in boarder_list][0]
                        # grab only the lower boundary of taxable income bracket

                        # extracting the TAX_RATE below:
                        tax_rate_description = tree.xpath(
                                        (
                                        '//*[@id="main-content"]/section/'
                                        'div[2]/div/article/div[1]/div/'
                                        'table['
                                        ) +
                                    str(table_num)+']/tbody/tr[' +
                                    str(i)+']/td[2]/p/text()')
                        # grab tax rate info for Xcent for each $1 taxable income over the low boundary.
                        target_webcontent_string = str(tax_rate_description)
                        transformed_webcontent_string_digitized = target_webcontent_string.replace('Nil', '0c')
                        tax_rate = float(re.findall
                                        (
                                            r"(\d+.?\d*){1}c",
                                            transformed_webcontent_string_digitized
                                        )[0]) / 100
                        dic_tax_bracket = {
                            'low_end': lower_boundary_tax_bracket,
                            'rate': tax_rate
                            }
                        tax_table_dics.append(dic_tax_bracket)
                    annual_tax_table = {tax_table_title: tax_table_dics}
                result.append(annual_tax_table)
            taxrate_filename = 'taxrate_' + str(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                ) + '.json'
            taxrate_path = os.path.join(
                settings.TAX_RATE_BACKUP_PATH, taxrate_filename
                )
            with open(taxrate_path, 'w') as outfile:
                json.dump(result, outfile)
            return result

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

    def __init__(self, ato_url, tax_rate_file_path):
        """init with generation of tax rate base on ATO offical page's data
        Args:

            input(ato_url): url to the ATO individual tax web page
            input(tax_rate_file_path): path to default/backup tax rate file
            output(result): contains taxable_income_bracket, and
            corresponding tax rate
        """
        get_online_taxrate = self.__get_taxrate_online__(ato_url)
        self._ato_addr = ato_url
        self._tax_rate_file_path = tax_rate_file_path
        # variable get_online_taxrate is intentionally created so that it only
        # runs once to save time in case
        # ATO online services are normal.
        if get_online_taxrate == -1:
            result = self.__get_taxrate_local_json__(tax_rate_file_path)
        else:
            result = get_online_taxrate
        self._taxrate_list = result

    def get_taxrate(self):
        return self._taxrate_list

    def get_ato_addr(self):
        return self._ato_addr

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
