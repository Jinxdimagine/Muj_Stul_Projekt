class Shift:
    def __init__(self, shift_id, shift_date, start_time, end_time, type, notes=None):
        self.shift_id = self.check_id(shift_id)
        self.shift_date = shift_date
        self.start_time = start_time
        self.end_time = end_time
        self.type = type
        self.notes = notes
    def check_id(self, shift_id):
       if  shift_id is not  None:
           return shift_id
       else:
           return None