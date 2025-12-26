import json

class DsHandler:
    def __init__(self):
        self.filename="ds_client"
        self.reservations=None
        self.read_all()
        self.checker=()

    def read_all(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)
    def write_all(self, reservations):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=4, ensure_ascii=False)

    def add_reservation(self, reservation,decision):
        reservations = self.read_all()
        reservation["status"] = decision  # default
        reservations.append(reservation)
        self.write_all(reservations)
    def check_reservation(self, reservation):
        reservations = self.read_all()   # list of dicts from JSON
        for r in reservations:
            if (r["name"] == reservation["name"] and
                    r["surname"] == reservation["surname"] and
                    r["date"] == reservation["date"] and
                    r["time"] == reservation["time"]):
                return False  # reservation already exists
        return True  # reservation is new
