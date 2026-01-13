import tkinter as tk
from tkinter import messagebox, ttk
import re

class EmployeeForm(tk.Frame):
    def __init__(self, parent, on_save, on_back, positions):
        super().__init__(parent)
        self.on_save = on_save
        self.on_back = on_back
        self.positions = positions  # list of dicts: {"id":1,"name":"Manager"}

        tk.Label(self, text="Nový zaměstnanec", font=("Arial", 18)).pack(pady=10)

        # First Name
        tk.Label(self, text="Jméno").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        # Last Name
        tk.Label(self, text="Příjmení").pack()
        self.surname_entry = tk.Entry(self)
        self.surname_entry.pack()

        # Birth Date
        tk.Label(self, text="Datum narození (DD.MM.RRRR)").pack()
        self.birth_date_entry = tk.Entry(self)
        self.birth_date_entry.pack()

        # Position Combo
        tk.Label(self, text="Pozice").pack()
        self.position_var = tk.StringVar()
        self.position_combo = ttk.Combobox(
            self,
            textvariable=self.position_var,
            state="readonly",
            values=[p.name for p in positions]
        )
        self.position_combo.pack()
        if positions:
            self.position_combo.current(0)

        # Hour rate
        tk.Label(self, text="Hodinová sazba").pack()
        self.hour_rate_entry = tk.Entry(self)
        self.hour_rate_entry.pack()

        # Full-time / Part-time
        tk.Label(self, text="Typ zaměstnání").pack()
        self.fulltime_var = tk.StringVar(value="FULL_TIME")
        tk.Radiobutton(self, text="Plný úvazek", variable=self.fulltime_var, value="FULL_TIME").pack()
        tk.Radiobutton(self, text="Částečný úvazek", variable=self.fulltime_var, value="PART_TIME").pack()

        # Buttons
        tk.Button(self, text="Uložit", command=self.save).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack()

    def save(self):
        # Validate fields
        if not self.name_entry.get() or not self.surname_entry.get() or not self.birth_date_entry.get() or not self.hour_rate_entry.get():
            messagebox.showerror("Chyba", "Vyplňte všechna pole")
            return

        # Validate date DD.MM.RRRR
        date_pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"
        if not re.match(date_pattern, self.birth_date_entry.get()):
            messagebox.showerror("Chyba", "Datum narození musí být ve formátu DD.MM.RRRR")
            return

        # Validate hour rate
        try:
            hour_rate = float(self.hour_rate_entry.get())
        except ValueError:
            messagebox.showerror("Chyba", "Hodinová sazba musí být číslo")
            return

        # Map position name to position_id
        position_name = self.position_var.get()
        position_id = next((p.id for p in self.positions if p.name == position_name), None)
        if position_id is None:
            messagebox.showerror("Chyba", "Neplatná pozice")
            return

        # Convert date to YYYY-MM-DD
        day, month, year = self.birth_date_entry.get().split(".")
        birth_date_mysql = f"{year}-{month}-{day}"

        employee_data = {
            "first_name": self.name_entry.get(),
            "last_name": self.surname_entry.get(),
            "position_id": position_id,
            "birth_date": birth_date_mysql,
            "hour_rate": hour_rate,
            "is_full_time": self.fulltime_var.get(),
            "active": 1
        }

        self.on_save(employee_data)

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
