class Employee:
    def __init__(self, id, first_name, last_name, position_id, is_full_time=True, hour_rate=0.0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.position_id = position_id
        self.is_full_time = is_full_time
        self.hour_rate = hour_rate

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
