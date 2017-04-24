

class Employee(object):
    """
        The Employee Class is responsible to obtain infomation about
        employee salary from varies of sources, including Interactive
        Console and CSV file and moore

    """
    def __init__(self, personal_info_set):
        super(Employee, self).__init__()
        self.personal_info_set = personal_info_set

        f_name, l_name, annual_salary, super_rate, pay_start_date