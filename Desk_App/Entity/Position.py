class Position:
    def __init__(self, id, name, is_active=True):
        self.id = id
        self.name = name
        self.is_active = is_active
    def __str__(self):
        return f"{self.name}"