from Entity.Employee import Employee
import mysql.connector
import csv
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
    def get_view_all(self):
        """
        Returns a list of all employees with their position info.
        """
        sql = "SELECT * FROM vw_employee_overview"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def get_all_stats(self):
        sql = "SELECT * FROM vw_employee_stats"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def import_from_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sql = """
                    INSERT INTO employee (first_name, last_name, position_id, birth_date, hour_rate, is_full_time, active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(sql, (
                    row['first_name'],
                    row['last_name'],
                    row['position_id'],
                    row['birth_date'],
                    row['hour_rate'],
                    row['is_full_time'],
                    row['active']
                ))
            self.conn.commit()