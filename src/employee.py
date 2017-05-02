import config.settings
from rounding import Rounding

class Employee(object):
    """
        The Employee Class is responsible to obtain infomation about
        employee salary from varies of sources, including Interactive
        Console and CSV file and moore
    """
    def __init__(self, person):
        self.person = person
        self.personal_info_dic = {}
        self.full_name = ''
        self.validate_input_data()

    def assemble_full_name(self,person, delimeter='.'):

        # if last name is missing, do not output any delimeter
        if len(person['last_name']) == 0:
            delimeter = ''
        return person['first_name'] + delimeter + person['last_name']

    def _compile_personal_info(self,person):
        self.person['annual_salary'] = self.convert_salary(self.person['annual_salary'])
        self.full_name = ''
        self.personal_info_dic = person
        self.personal_info_dic['full_name'] = self.assemble_full_name(person,'.')
        return self.personal_info_dic

    def convert_salary(self,input_salary):
        return float(input_salary)

    def validate_input_data(self):
        # TODO: add input data validation
        salary = self.person.get('annual_salary')
        if salary is None:
            print "salary missing"
            return False
        else:
            return True

    def get_salary(self):
        self.person['annual_salary'] = self.convert_salary(self.person['annual_salary'])
        return self.person['annual_salary']

    def get_personal_info(self):
        return self._compile_personal_info(self.person)

    def __str__(self):
        return str(self.person)
