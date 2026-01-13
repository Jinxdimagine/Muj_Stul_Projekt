from Entity import ShiftType
import mysql.connector

class ShiftTypeDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    # Get all shift types
    def get_all(self):
        self.cursor.execute("SELECT * FROM shift_type")
        rows = self.cursor.fetchall()
        return rows

    # Get shift type by ID
    def get_by_id(self, type_id):
        self.cursor.execute("SELECT * FROM shift_type WHERE id=%s", (type_id,))
        row = self.cursor.fetchone()
        return row

    # Add new shift type
    def add(self, t: ShiftType):
        sql = "INSERT INTO shift_type (name) VALUES (%s)"
        self.cursor.execute(sql, (t.name,))
        self.conn.commit()
        t.shift_type_id = self.cursor.lastrowid
        return t

    # Update shift type
    def update(self, t: ShiftType):
        sql = "UPDATE shift_type SET name=%s WHERE id=%s"
        self.cursor.execute(sql, (t.name, t.shift_type_id))
        self.conn.commit()

    # Delete shift type
    def delete(self, type_id):
        self.cursor.execute("DELETE FROM shift_type WHERE id=%s", (type_id,))
        self.conn.commit()
