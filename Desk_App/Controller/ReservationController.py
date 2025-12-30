from collections import defaultdict

class ReservationController:
    def __init__(self, dao=None):
        self.dao = dao

    def get_reservations_by_date(self):
        # Dummy data pro testování
        dummy_reservations = [
            {"name": "Jan", "surname": "Novák", "people": 2, "date": "2025-12-05", "time": "18:00"},
            {"name": "Petra", "surname": "Svobodová", "people": 4, "date": "2025-12-05", "time": "19:00"},
            {"name": "Karel", "surname": "Novotný", "people": 3, "date": "2025-12-10", "time": "17:30"},
        ]

        grouped = defaultdict(list)
        for r in dummy_reservations:
            grouped[r["date"]].append(r)

        return grouped  # dict: { '2025-12-05': [reservation1, reservation2], ... }

    def get_all(self):
        # Pro listbox, vrací seznam všech rezervací
        return [
            {"name": "Jan", "surname": "Novák", "people": 2, "date": "2025-12-05", "time": "18:00"},
            {"name": "Petra", "surname": "Svobodová", "people": 4, "date": "2025-12-05", "time": "19:00"},
            {"name": "Karel", "surname": "Novotný", "people": 3, "date": "2025-12-10", "time": "17:30"},
        ]
