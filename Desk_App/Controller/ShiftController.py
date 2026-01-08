class ShiftController:
    def __init__(self, shift_dao, employee_shift_dao):
        self.shift_dao = shift_dao
        self.employee_shift_dao = employee_shift_dao

    def create_shift_with_employees(self, date, time_from, time_to, employee_ids):
        shift_id = self.shift_dao.create_shift(date, time_from, time_to, "")
        for emp_id in employee_ids:
            self.employee_shift_dao.assign_employee(emp_id, shift_id)

    def update_shift(self, shift_id, date, time_from, time_to):
        self.shift_dao.update_shift(shift_id, date, time_from, time_to)

    def delete_shift(self, shift_id):
        self.shift_dao.delete_shift(shift_id)

    def add_employee_to_shift(self, shift_id, employee_id):
        self.employee_shift_dao.assign_employee(employee_id, shift_id)

    def remove_employee_from_shift(self, shift_id, employee_id):
        self.employee_shift_dao.remove_employee(employee_id, shift_id)

    def save_shift(self, shift_data):
        shift_id = self.shift_dao.create(shift_data)
        for emp_id in shift_data["employees"]:
            self.employee_shift_dao.assign(emp_id, shift_id)