from Entity.EmployeeShift import EmployeeShift
import mysql.connector

class EmployeeShiftDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all(self):
        self.cursor.execute("SELECT * FROM employee_shifts")
        return [EmployeeShift(**r) for r in self.cursor.fetchall()]

    def add(self, es: EmployeeShift):
        sql = "INSERT INTO employee_shifts (employee_id, shift_id) VALUES (%s,%s)"
        self.cursor.execute(sql, (es.employee_id, es.shift_id))
        self.conn.commit()

    def delete(self, employee_id, shift_id):
        self.cursor.execute("DELETE FROM employee_shifts WHERE employee_id=%s AND shift_id=%s",
                            (employee_id, shift_id))
        self.conn.commit()
