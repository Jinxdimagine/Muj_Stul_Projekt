import tkinter as tk
from tkinter import ttk


class ShiftFormView(tk.Frame):
    def __init__(
            self,
            parent,
            date,
            employees,
            on_save,
            on_cancel,
            shift=None
    ):
        """
        shift = None → vytváření nové směny
        shift != None → editace existující směny
        """
        super().__init__(parent)

        self.date = date
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.employees = employees
        self.shift = shift

        self.employee_vars = {}

        self.build_ui()

    def build_ui(self):
        title = "Upravit směnu" if self.shift else "Přidat směnu"
        tk.Label(self, text=title, font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text=f"Datum: {self.date}").pack(pady=5)

        # --- Časy ---
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Od:").grid(row=0, column=0, sticky="e")
        self.from_entry = tk.Entry(form, width=10)
        self.from_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Do:").grid(row=1, column=0, sticky="e")
        self.to_entry = tk.Entry(form, width=10)
        self.to_entry.grid(row=1, column=1, padx=5)

        if self.shift:
            self.from_entry.insert(0, self.shift["from"])
            self.to_entry.insert(0, self.shift["to"])

        # --- Zaměstnanci ---
        tk.Label(self, text="Zaměstnanci:", font=("Arial", 12)).pack(pady=5)

        emp_frame = tk.Frame(self)
        emp_frame.pack()

        for emp in self.employees:
            var = tk.BooleanVar()

            if self.shift and emp["id"] in self.shift["employee_ids"]:
                var.set(True)

            cb = tk.Checkbutton(
                emp_frame,
                text=f"{emp['first_name']} {emp['last_name']}",
                variable=var
            )
            cb.pack(anchor="w")

            self.employee_vars[emp["id"]] = var

        # --- Tlačítka ---
        btns = tk.Frame(self)
        btns.pack(pady=15)

        tk.Button(btns, text="Uložit", command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Zrušit", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

    def save(self):
        selected_employees = [
            emp_id for emp_id, var in self.employee_vars.items() if var.get()
        ]

        data = {
            "date": self.date,
            "from": self.from_entry.get(),
            "to": self.to_entry.get(),
            "employees": selected_employees,
            "shift_id": self.shift["id"] if self.shift else None
        }

        self.on_save(data)
