from Entity.Shift import Shift
import mysql.connector
import csv
class ShiftDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    # Get all shifts
    def get_all(self):
        sql = """
            SELECT s.id, s.shift_date, s.start_time, s.end_time, s.type_shift_id,
                   t.name AS type_name
            FROM shifts s
            JOIN shift_type t ON s.type_shift_id = t.id
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        shifts = []
        for r in rows:
            shift = Shift(
                shift_id=r['id'],
                shift_date=r['shift_date'],
                start_time=r['start_time'],
                end_time=r['end_time'],
                type_shift_id=r['type_shift_id']
            )
            shifts.append(shift)
        return shifts

    # Get shift by ID
    def get_by_id(self, shift_id):
        sql = "SELECT * FROM shifts WHERE id=%s"
        self.cursor.execute(sql, (shift_id,))
        row = self.cursor.fetchone()
        if row:
            return Shift(
                shift_id=row['id'],
                shift_date=row['shift_date'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                type_shift_id=row['type_shift_id']
            )
        return None

    # Get shifts by date
    def get_shifts_by_date(self, date):
        sql = "SELECT * FROM shifts WHERE shift_date=%s"
        self.cursor.execute(sql, (date,))
        rows = self.cursor.fetchall()
        shifts = []
        for r in rows:
            shifts.append(Shift(
                shift_id=r['id'],
                shift_date=r['shift_date'],
                start_time=r['start_time'],
                end_time=r['end_time'],
                type_shift_id=r['type_shift_id']
            ))
        return shifts

    def add(self, s: Shift, employee_ids: list):
        for emp_id in employee_ids:
            self.cursor.callproc(
                "add_shift_to_employee",
                (emp_id, s.shift_date, s.start_time, s.end_time, s.type_shift_id)
            )
        self.conn.commit()


    # Update existing shift
    def update(self, s: Shift, employee_ids: list):
        for emp_id in employee_ids:
            self.cursor.callproc(
                "update_employee_shift",
                (emp_id, s.shift_id, s.start_time, s.end_time, s.type_shift_id)
            )
        self.conn.commit()


    def delete(self, shift_id):
        self.cursor.callproc(
            "delete_shift",
            (shift_id,)  # comma makes it a tuple
        )
        self.conn.commit()
    def import_from_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 1️⃣ vložíme samotnou směnu
                sql_shift = """
                    INSERT INTO shifts (shift_date, start_time, end_time, type_shift_id)
                    VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(sql_shift, (
                    row['shift_date'],
                    row['start_time'],
                    row['end_time'],
                    row['type_shift_id']
                ))
            self.conn.commit()