import json

class DsHandler:
    def __init__(self):
        self.filename="ds_client"
        self.reservations=None

    def read_all(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)
    def write_all(self, reservations):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=4, ensure_ascii=False)

    def add_reservation(self, reservation):
        reservations = self.read_all()
        reservation["status"] = "pending"  # default
        reservations.append(reservation)
        self.write_all(reservations)