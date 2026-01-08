# DAO/BaseDAO.py
import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Martinvucz2007",
            database="mujstul"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()