from Entity.Employee import Employee

class EmployeeController:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        rows = self.dao.get_all()
        employees = []
        for r in rows:
            employee = Employee(
                employee_id=r['id'],
                first_name=r["first_name"],
                last_name=r["last_name"],
                position_id=r["position_id"],
                is_full_time=r["is_full_time"],
                hour_rate=r["hour_rate"],
            )
            employees.append(employee)
        return employees

    def get_by_id(self, id):
        r=self.dao.get_by_id(id)
        employee = Employee(
            employee_id=r['id'],
            first_name=r["first_name"],
            last_name=r["last_name"],
            position_id=r["position_id"],
            is_full_time=r["is_full_time"],
            hour_rate=r["hour_rate"],
        )
        return employee

    def add(self, employee_data):
        # převedeme dict na Employee entity# pokud máš seznam pozic
        employee = Employee(
            employee_id=None,
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
