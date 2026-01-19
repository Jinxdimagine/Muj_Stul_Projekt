from Entity.Shift import Shift
class ShiftController:
    def __init__(self, shift_dao, employee_shift_dao):
        self.shift_dao = shift_dao
        self.employee_shift_dao = employee_shift_dao

    def get_all_shifts(self):
        return self.shift_dao.get_all()
    def get_shifts_by_date(self,date):
        return self.shift_dao.get_shifts_by_date(date)
    def add_shift(self, shift,selected_employee):
        return self.shift_dao.add(shift,selected_employee)
    def update_shift(self, shift,selected_employee):
        self.shift_dao.update(shift,selected_employee)
    def delete_shift(self, shift_id):
        self.shift_dao.delete(shift_id)

    def assign_employee(self, shift_id, employee_id):
        self.employee_shift_dao.assign(employee_id, shift_id)

    def remove_employee(self, shift_id, employee_id):
        self.employee_shift_dao.remove(employee_id, shift_id)
    def import_shifts(self, file_path):
        self.shift_dao.import_from_csv(file_path)