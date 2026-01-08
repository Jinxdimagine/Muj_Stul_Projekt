class Customer:
    def __init__(self, id, first_name, last_name, email, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
