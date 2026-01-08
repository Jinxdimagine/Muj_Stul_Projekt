from Entity.Employee import Employee
import mysql.connector

class EmployeeDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all(self):
        self.cursor.execute("SELECT * FROM employees")
        return [Employee(**r) for r in self.cursor.fetchall()]

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
        row = self.cursor.fetchone()
        return Employee(**row) if row else None

    def add(self, e: Employee):
        print(e)
        print(e.first_name)
        sql = """INSERT INTO employees (first_name,last_name,position_id,is_full_time,hour_rate)
                 VALUES (%s,%s,%s,%s,%s)"""
        self.cursor.execute(sql, (e.first_name, e.last_name, e.position_id, e.is_full_time, e.hour_rate))
        self.conn.commit()
        e.id = self.cursor.lastrowid
        return e

    def update(self, e: Employee):
        sql = """UPDATE employees SET first_name=%s,last_name=%s,position_id=%s,is_full_time=%s,hour_rate=%s
                 WHERE id=%s"""
        self.cursor.execute(sql, (e.first_name, e.last_name, e.position_id, e.is_full_time, e.hour_rate, e.id))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
        self.conn.commit()
