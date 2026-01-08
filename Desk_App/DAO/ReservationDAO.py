from Entity.Reservation import Reservation
import mysql.connector

class ReservationDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all(self):
        self.cursor.execute("SELECT * FROM reservations")
        return [Reservation(**r) for r in self.cursor.fetchall()]

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM reservations WHERE id=%s", (id,))
        row = self.cursor.fetchone()
        return Reservation(**row) if row else None

    def add(self, r: Reservation):
        sql = """INSERT INTO reservations
                 (customer_id,reservation_date,reservation_time,people,confirmed,notes)
                 VALUES (%s,%s,%s,%s,%s,%s)"""
        self.cursor.execute(sql, (r.customer_id, r.reservation_date, r.reservation_time,
                                  r.people, r.confirmed, r.notes))
        self.conn.commit()
        r.id = self.cursor.lastrowid
        return r

    def update(self, r: Reservation):
        sql = """UPDATE reservations SET customer_id=%s,reservation_date=%s,reservation_time=%s,
                 people=%s,confirmed=%s,notes=%s WHERE id=%s"""
        self.cursor.execute(sql, (r.customer_id, r.reservation_date, r.reservation_time,
                                  r.people, r.confirmed, r.notes, r.id))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM reservations WHERE id=%s", (id,))
        self.conn.commit()
