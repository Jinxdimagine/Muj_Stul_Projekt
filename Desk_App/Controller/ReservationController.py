# Controller/ReservationController.py
class ReservationController:
    def __init__(self, reservation_dao):
        self.reservation_dao = reservation_dao

    def get_all(self):
        return self.reservation_dao.get_all()

    def get_reservations_by_date(self):
        """Vrátí rezervace seskupené podle data (pro kalendář)"""
        reservations = self.reservation_dao.get_all()
        grouped = {}
        for r in reservations:
            date_str = r.reservation_date.strftime("%Y-%m-%d")
            if date_str not in grouped:
                grouped[date_str] = []
            grouped[date_str].append({
                "name": r.customer.first_name,
                "surname": r.customer.last_name,
                "people": r.people,
                "time": r.reservation_time.strftime("%H:%M")
            })
        return grouped
