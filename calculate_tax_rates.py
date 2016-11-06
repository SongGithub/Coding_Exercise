"""
#This module is developed for calculate tax rate, including web scraping the
ATO individual tax rate table
# Author: Song Jin 2016
#Ref: http://docs.python-guide.org/en/latest/scenarios/scrape/
#Specialised knowledge: XPath
#
"""

from lxml import html
import requests, re


class TaxRate(object):
    """the class includes all sorts of methods to calculate tax"""

    def __init__(self, ato_url):
        """init with generation of tax rate base on ATO offical page's data

        Args:

            input(ato_url): url to the ATO individual tax web page

            output(result): Json file containing taxable_income_range, and
            corresponding tax rate
        """
        page = requests.get(ato_url, verify=False)
        tree = html.fromstring(page.content)
        result = []
        for i in range(2, 7):
            taxable_income_range = tree.xpath('//*[@id="ctl00_MainPlaceHolder_contentWrapperDropZone_columnDisplay_ctl00_controlcolumn_ctl00_WidgetHost_updatepanel"]/div/table[1]/tbody/tr[' + str(i) + ']/td[1]/p/text()')
            target_webcontent_string = str(taxable_income_range)
            transformed_webcontent_string_midway = target_webcontent_string.replace('over', '999,999')
            # replace 'over' with numeric value
            transformed_webcontent_string_final0 = transformed_webcontent_string_midway.replace(',', '')
            # remove comma
            transformed_webcontent_string_final1 = transformed_webcontent_string_final0.replace('\u2013', '')
            # remove dash
            boarder_list = re.findall(r"(\d+)", transformed_webcontent_string_final1)
            income_range_rate = [float(x) for x in boarder_list]
            # extract the TAX_RATE
            tax_rate_description = tree.xpath('//*[@id="ctl00_MainPlaceHolder_contentWrapperDropZone_columnDisplay_ctl00_controlcolumn_ctl00_WidgetHost_updatepanel"]/div/table[1]/tbody/tr[' + str(i) + ']/td[2]/p/text()')
            target_webcontent_string = str(tax_rate_description)
            transformed_webcontent_string_digitized = target_webcontent_string.replace('Nil','0c')
            transformed_webcontent_string_no_comma = transformed_webcontent_string_digitized.replace(',','')
            tax_rate_info = float(re.findall(r"(\d+.?\d*){1}c", transformed_webcontent_string_no_comma)[0])/100
            tax_rate_base_unfiltered = re.findall(r"\$(\d+.?\d*)?.[plus]+", transformed_webcontent_string_no_comma)
            if len(tax_rate_base_unfiltered) != 0:
                tax_rate_base = float(tax_rate_base_unfiltered[0])
            else:
                tax_rate_base = 0
            # print(tax_rate_info, tax_rate_base)

            income_range_rate.append(tax_rate_info)
            income_range_rate.append(tax_rate_base)
            result.append(tuple(income_range_rate))
        print('#' * 80)
        print('tax rate extracted is as follow list:')
        print(result)
        print('#' * 80)
        self._taxrate_list = result

    def calculate_tax(self, salary):
        """calculate_tax according to input tax rate

        Args:
            salary: individual salary for calculation
        """
        steps_low = [level[0] for level in self._taxrate_list]
        steps_rate = [level[2] for level in self._taxrate_list]
        steps_base = [level[3] for level in self._taxrate_list]
        for index in range(len(steps_low)):
            if steps_low[index] >= salary:
                matching_index = index - 1
                break
        tax = round(steps_rate[matching_index] * (salary - steps_low[matching_index]) + steps_base[matching_index])
        return float(tax)


if __name__ == '__main__':
    tax_rate_instance = TaxRate('https://www.ato.gov.au/rates/individual-income-tax-rates')
    print(tax_rate_instance.calculate_tax(40000))
