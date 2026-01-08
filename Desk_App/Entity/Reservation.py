class Reservation:
    def __init__(self, id, customer_id, reservation_date, reservation_time, people, confirmed=False, notes=None):
        self.id = id
        self.customer_id = customer_id
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.people = people
        self.confirmed = confirmed
        self.notes = notes
