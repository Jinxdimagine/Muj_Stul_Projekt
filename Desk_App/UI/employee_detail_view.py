import tkinter as tk


class EmployeeDetailView(tk.Frame):
    def __init__(self, parent, employee, on_back, on_delete, on_save):
        super().__init__(parent)

        self.employee = employee
        self.on_back = on_back
        self.on_delete = on_delete
        self.on_save = on_save

        tk.Label(self, text="Profil zaměstnance", font=("Arial", 18)).pack(pady=10)

        self.first_name = tk.StringVar(value=employee["first_name"])
        self.last_name = tk.StringVar(value=employee["last_name"])
        self.position = tk.StringVar(value=employee["position"])
        self.hour_rate = tk.StringVar(value=str(employee["hour_rate"]))
        self.active = tk.BooleanVar(value=employee["active"])

        self._row("Jméno", self.first_name)
        self._row("Příjmení", self.last_name)
        self._row("Pozice", self.position)
        self._row("Hodinová sazba", self.hour_rate)

        tk.Checkbutton(self, text="Aktivní", variable=self.active).pack(pady=5)

        tk.Button(self, text="Uložit změny", command=self.save).pack(pady=5)
        tk.Button(self, text="Smazat zaměstnance", command=self.delete).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack(pady=10)

    def _row(self, label, var):
        frame = tk.Frame(self)
        frame.pack(pady=2)
        tk.Label(frame, text=label, width=15, anchor="w").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=var, width=30).pack(side=tk.LEFT)

    def save(self):
        updated = {
            "id": self.employee["id"],
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "position": self.position.get(),
            "hour_rate": float(self.hour_rate.get()),
            "active": self.active.get()
        }
        self.on_save(updated)

    def delete(self):
        self.on_delete(self.employee["id"])
