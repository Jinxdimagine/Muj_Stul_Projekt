from Entity.Employee import Employee

class EmployeeController:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id):
        return self.dao.get_by_id(id)

    def add(self, employee_data):
        # převedeme dict na Employee entity# pokud máš seznam pozic
        employee = Employee(
            id=None,
            first_name=employee_data["first_name"],
            last_name=employee_data["last_name"],
            position_id=employee_data["position"],
            birth_date=employee_data["birth_date"],   # správně formát date
            hour_rate=float(employee_data["hour_rate"])
        )
        return self.dao.add(employee)

    def update(self, employee):
        self.dao.update(employee)

    def delete(self, id):
        self.dao.delete(id)
