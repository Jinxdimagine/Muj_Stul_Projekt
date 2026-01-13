class Shift:
    def __init__(self, shift_id=None, shift_date=None, start_time=None, end_time=None, type_shift_id=None):
        self.shift_id = shift_id          # corresponds to `id` in DB
        self.shift_date = shift_date      # datetime.date or string 'YYYY-MM-DD'
        self.start_time = start_time      # datetime.time or string 'HH:MM:SS'
        self.end_time = end_time          # datetime.time or string 'HH:MM:SS'
        self.type_shift_id = type_shift_id  # foreign key to ShiftType.id

    def __str__(self):
        return f"{self.shift_date} {self.start_time}-{self.end_time}"

    def values(self):
        return self.shift_id