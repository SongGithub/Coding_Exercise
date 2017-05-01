#!/usr/bin/python

from src.employee import Employee
import unittest


class TestEmployee(unittest.TestCase):
    """desc!"""
    def setUp(self):
        self.instance = Employee(
                {
                    'first_name':'John',
                    'last_name':'Smith',
                    'annual_salary':'60012',
                    'super_rate':'9',
                    'start_date':'1/1/85'}
            )
        test_name = self.shortDescription()
        print 'outstanding test= ', test_name

    def test_is_instance(self):
        """test if the instance exists"""
        self.assertIsInstance(self.instance,Employee)

    def test_assemble_full_name(self):
        """assemble_full_name should assemble the full name"""
        assert self.instance.assemble_full_name(self.instance.person,'.') == 'John.Smith'

    def test_assemble_full_name_default_delimeter(self):
        """assemble_full_name should assemble the full name and handle default delimeter"""
        assert self.instance.assemble_full_name(self.instance.person) == 'John.Smith'

    def test_assemble_full_name_missing_last_name(self):
        """assemble_full_name should assemble the full name and handle missing lastname"""
        test_fixture_1 = self.instance.person
        test_fixture_1['last_name'] = ''
        assert self.instance.assemble_full_name(test_fixture_1,'.') == 'John'

    def test_getting_personal_info(self):
        """correct info can be retrieved from the object"""

        assert self.instance.get_personal_info() == {
            'first_name': 'John',
            'last_name': 'Smith',
            'super_rate': '9',
            'annual_salary': 60012.0,
            'full_name': 'John.Smith',
            'start_date': '1/1/85'}

    def test_get_salary(self):
        """should be able to get correct salary from input object"""
        assert self.instance.get_salary() == float(self.instance.person['annual_salary'])

    def test_convert_salary(self):
        """should return: float format of the input salary"""
        input_salary = '50021'
        assert self.instance.convert_salary(input_salary) == float('50021')

    def test_compile_personal_info(self):
        """ it should take raw input data, and convert data in relevant fields
        to desirable formats."""
        assert self.instance._compile_personal_info(self.instance.person) == {
            'first_name': 'John',
            'last_name': 'Smith',
            'super_rate': '9',
            'annual_salary': 60012.0,
            'full_name': 'John.Smith',
            'start_date': '1/1/85'}