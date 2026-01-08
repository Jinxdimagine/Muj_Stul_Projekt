class EmployeeController:
    def __init__(self, dao):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, id):
        return self.dao.get_by_id(id)

    def add(self, employee):
        return self.dao.add(employee)

    def update(self, employee):
        self.dao.update(employee)

    def delete(self, id):
        self.dao.delete(id)
