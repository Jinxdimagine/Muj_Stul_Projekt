import tkinter as tk
from tkinter import ttk
import re
from Entity.Employee import Employee
class EmployeeDetailView(tk.Frame):
    def __init__(self, parent, employee, positions, on_back, on_delete, on_save):
        super().__init__(parent)

        self.employee = employee
        self.positions = positions  # list of Position objects
        self.on_back = on_back
        self.on_delete = on_delete
        self.on_save = on_save

        tk.Label(self, text="Profil zaměstnance", font=("Arial", 18)).pack(pady=10)
        print(employee.birth_date)
        # Variables
        self.first_name_var = tk.StringVar(value=employee.first_name)
        self.last_name_var = tk.StringVar(value=employee.last_name)
        self.birth_date_var = tk.StringVar(value=employee.birth_date)  # 'YYYY-MM-DD'
        self.hour_rate_var = tk.StringVar(value=str(employee.hour_rate))
        self.active_var = tk.BooleanVar(value=bool(employee.active))
        self.is_full_time_var = tk.StringVar(value=employee.is_full_time)
        self.position_var = tk.StringVar(value=self.get_position_name(employee.position_id))

        # Form rows
        self._row("Jméno", self.first_name_var)
        self._row("Příjmení", self.last_name_var)
        self._row("Datum narození (YYYY-MM-DD)", self.birth_date_var)
        self._row("Hodinová sazba", self.hour_rate_var)

        # Position combo
        tk.Label(self, text="Pozice").pack(pady=2)
        self.position_combo = ttk.Combobox(
            self,
            textvariable=self.position_var,
            state="readonly",
            values=[p.name for p in positions]
        )
        self.position_combo.pack()

        # Full-time / Part-time
        tk.Label(self, text="Typ zaměstnání").pack(pady=2)
        tk.Radiobutton(self, text="Plný úvazek", variable=self.is_full_time_var, value="FULL_TIME").pack()
        tk.Radiobutton(self, text="Částečný úvazek", variable=self.is_full_time_var, value="PART_TIME").pack()

        # Active checkbox
        tk.Checkbutton(self, text="Aktivní", variable=self.active_var).pack(pady=5)

        # Buttons
        tk.Button(self, text="Uložit změny", command=self.save).pack(pady=5)
        tk.Button(self, text="Smazat zaměstnance", command=self.delete).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack(pady=10)

    def _row(self, label, var):
        frame = tk.Frame(self)
        frame.pack(pady=2)
        tk.Label(frame, text=label, width=20, anchor="w").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=var, width=30).pack(side=tk.LEFT)

    def get_position_name(self, position_id):
        for p in self.positions:
            if p.id == position_id:
                return p.name
        return ""

    def save(self):
        # Validate birth_date format YYYY-MM-DD
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.birth_date_var.get()):
            tk.messagebox.showerror("Chyba", "Datum narození musí být ve formátu YYYY-MM-DD")
            return

        # Map position name back to ID
        position_name = self.position_var.get()
        position_id = next((p.id for p in self.positions if p.name == position_name), None)
        if position_id is None:
            tk.messagebox.showerror("Chyba", "Neplatná pozice")
            return

        updated_employee = Employee(
            employee_id=self.employee.employee_id,
            first_name=self.first_name_var.get(),
            last_name=self.last_name_var.get(),
            birth_date=self.birth_date_var.get(),
            hour_rate=float(self.hour_rate_var.get()),
            position_id=position_id,
            is_full_time=self.is_full_time_var.get(),
            active=int(self.active_var.get())
        )

        self.on_save(updated_employee)

    def delete(self):
        self.on_delete(self.employee.employee_id)
