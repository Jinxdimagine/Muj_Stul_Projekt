from Entity.Position import Position
import mysql.connector

class PositionDAO:
    def __init__(self, connection_params):
        self.conn = mysql.connector.connect(**connection_params)
        self.cursor = self.conn.cursor(dictionary=True)
    def get_all(self):
        self.cursor.execute("SELECT * FROM positions")
        rows = self.cursor.fetchall()
        list=[]
        for r in rows:
            list.append(Position(**r))
        return list

    def get_id_by_name(self, name):
        self.cursor.execute("SELECT id FROM positions WHERE name=%s", (name,))
        row = self.cursor.fetchone()

        return row["id"]
    def get_by_id(self, id):
        self.cursor.execute("SELECT * FROM positions WHERE id=%s", (id,))
        row = self.cursor.fetchone()
        return Position(**row) if row else None

    def add(self, position: Position):
        sql = "INSERT INTO positions (name,is_active) VALUES (%s,%s)"
        self.cursor.execute(sql, (position.name, position.is_active))
        self.conn.commit()
        position.id = self.cursor.lastrowid
        return position

    def update(self, position: Position):
        sql = "UPDATE positions SET name=%s,is_active=%s WHERE id=%s"
        self.cursor.execute(sql, (position.name, position.is_active, position.id))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute("DELETE FROM positions WHERE id=%s", (id,))
        self.conn.commit()
