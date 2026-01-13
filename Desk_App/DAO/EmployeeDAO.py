from Entity.Employee import Employee
import mysql.connector

class EmployeeDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    # Get all active employees
    def get_all(self):
        sql = """
            SELECT 
                e.id,
                e.first_name,
                e.last_name,
                e.position_id,
                p.name AS position_name,
                e.is_full_time,
                e.hour_rate,
                e.birth_date,
                e.active
            FROM employee e
            JOIN employee_position p ON e.position_id = p.id
            WHERE e.active = 1
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    # Get employee by ID
    def get_by_id(self, employee_id):
        sql = """
            SELECT 
                e.id,
                e.first_name,
                e.last_name,
                e.position_id,
                p.name AS position_name,
                e.is_full_time,
                e.hour_rate,
                e.birth_date,
                e.active
            FROM employee e
            JOIN employee_position p ON e.position_id = p.id
            WHERE e.id = %s
        """
        self.cursor.execute(sql, (employee_id,))
        row = self.cursor.fetchone()
        return row

    # Add a new employee
    def add(self, e: Employee):
        sql = """
            INSERT INTO employee 
            (first_name, last_name, position_id, is_full_time, hour_rate, birth_date, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            (
                e.first_name,
                e.last_name,
                e.position_id,
                e.is_full_time,
                e.hour_rate,
                e.birth_date,
                e.active
            )
        )
        self.conn.commit()
        e.employee_id = self.cursor.lastrowid
        return e

    # Update existing employee
    def update(self, e: Employee):
        sql = """
            UPDATE employee 
            SET first_name=%s, last_name=%s, position_id=%s, is_full_time=%s, hour_rate=%s, birth_date=%s, active=%s
            WHERE id=%s
        """
        self.cursor.execute(
            sql,
            (
                e.first_name,
                e.last_name,
                e.position_id,
                e.is_full_time,
                e.hour_rate,
                e.birth_date,
                e.active,
                e.employee_id
            )
        )
        self.conn.commit()

    # Delete (hard delete)
    def delete(self, employee_id):
        self.cursor.execute("DELETE FROM employee WHERE id=%s", (employee_id,))
        self.conn.commit()

    # Optional: soft delete (set active=0)
    def deactivate(self, employee_id):
        self.cursor.execute("UPDATE employee SET active=0 WHERE id=%s", (employee_id,))
        self.conn.commit()
