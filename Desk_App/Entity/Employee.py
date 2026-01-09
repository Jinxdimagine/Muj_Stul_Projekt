from distutils.command.check import check


class Employee:
    def __init__(self, employee_id, first_name, last_name, position_id, is_full_time=True, hour_rate=0.0,birth_date=""):
        self.employee_id = self.check_id(employee_id)
        self.first_name = first_name
        self.last_name = last_name
        self.position_id = position_id
        self.is_full_time = is_full_time
        self.hour_rate = hour_rate
        self.birth_date=birth_date
    def __str__(self):
        return self.first_name
    def values(self):
        return self.first_name, self.last_name, self.position_id, self.is_full_time, self.hour_rate, self.birth_date
    def check_id(self,employee_id):
        if not employee_id is None:
            return employee_id
        else:
            return None