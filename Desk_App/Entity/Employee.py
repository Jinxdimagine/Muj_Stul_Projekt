class Employee:
    def __init__(self, employee_id=None, first_name="", last_name="", position_id=None,
                 birth_date=None, hour_rate=0.0, is_full_time="FULL_TIME", active=1,position_name=None,):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.position_id = position_id
        self.birth_date = birth_date  # format 'YYYY-MM-DD' for MySQL
        self.hour_rate = hour_rate
        self.is_full_time = is_full_time  # 'FULL_TIME' or 'PART_TIME'
        self.active = active
        self.position_name=position_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def values(self):
        return (self.first_name, self.last_name, self.position_id,
                self.birth_date, self.hour_rate, self.is_full_time, self.active)
