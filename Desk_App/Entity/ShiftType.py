class ShiftType:
    def __init__(self, shift_type_id=None, name=""):
        self.shift_type_id = shift_type_id  # corresponds to `id` in DB
        self.name = name

    def __str__(self):
        return self.name

    def values(self):
        return (self.name,)
