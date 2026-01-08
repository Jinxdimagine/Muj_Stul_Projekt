class Shift:
    def __init__(self, id, shift_date, start_time, end_time, type, notes=None):
        self.id = id
        self.shift_date = shift_date
        self.start_time = start_time
        self.end_time = end_time
        self.type = type
        self.notes = notes
