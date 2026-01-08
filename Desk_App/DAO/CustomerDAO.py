from Entity.Customer import Customer
import mysql.connector

class CustomerDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)

    def get_all(self):
        self.cursor.execute("SELECT * FROM customers")
        return [Customer(**r) for r in self.cursor.fetchall()]

    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM customers WHERE id=%s", (id,))
        row = self.cursor.fetchone()
        return Customer(**row) if row else None

    def add(self, c: Customer):
        sql = "INSERT INTO customers (first_name,last_name,email,phone) VALUES (%s,%s,%s,%s)"
        self.cursor.execute(sql, (c.first_name, c.last_name, c.email, c.phone))
        self.conn.commit()
        c.id = self.cursor.lastrowid
        return c

    def update(self, c: Customer):
        sql = "UPDATE customers SET first_name=%s,last_name=%s,email=%s,phone=%s WHERE id=%s"
        self.cursor.execute(sql, (c.first_name, c.last_name, c.email, c.phone, c.id))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM customers WHERE id=%s", (id,))
        self.conn.commit()
