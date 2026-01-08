from Entity.Shift import Shift
import mysql.connector

class ShiftDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all(self):
        self.cursor.execute("SELECT * FROM shifts")
        return [Shift(**r) for r in self.cursor.fetchall()]

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM shifts WHERE id=%s", (id,))
        row = self.cursor.fetchone()
        return Shift(**row) if row else None

    def add(self, s: Shift):
        sql = """INSERT INTO shifts (shift_date,start_time,end_time,type,notes)
                 VALUES (%s,%s,%s,%s,%s)"""
        self.cursor.execute(sql, (s.shift_date, s.start_time, s.end_time, s.type, s.notes))
        self.conn.commit()
        s.id = self.cursor.lastrowid
        return s

    def update(self, s: Shift):
        sql = """UPDATE shifts SET shift_date=%s,start_time=%s,end_time=%s,type=%s,notes=%s WHERE id=%s"""
        self.cursor.execute(sql, (s.shift_date, s.start_time, s.end_time, s.type, s.notes, s.id))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM shifts WHERE id=%s", (id,))
        self.conn.commit()
