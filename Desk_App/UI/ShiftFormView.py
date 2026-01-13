import tkinter as tk
from tkinter import ttk, messagebox
from Entity.Shift import Shift
from datetime import datetime, time


class ShiftFormView(tk.Frame):
    def __init__(
            self,
            parent,
            date,                  # string 'YYYY-MM-DD'
            shift_types,           # list of ShiftType objects
            employees,             # list of Employee objects
            on_save,
            on_cancel,
            on_delete=None,        # callable(Shift) → delete shift
            shift=None,            # existing Shift object or None
            assigned_employee_ids=None  # list of employee_ids already assigned
    ):
        super().__init__(parent)

        self.date = date
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.on_delete = on_delete
        self.shift_types = shift_types
        self.employees = employees
        self.shift = shift
        self.assigned_employee_ids = assigned_employee_ids or []

        # Dictionary: employee_id -> BooleanVar
        self.employee_vars = {}

        self.build_ui()

    def build_ui(self):
        title = "Upravit směnu" if self.shift else "Přidat směnu"
        tk.Label(self, text=title, font=("Arial", 18)).pack(pady=10)
        tk.Label(self, text=f"Datum: {self.date}").pack(pady=5)

        # --- Times ---
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Od (HH:MM):").grid(row=0, column=0, sticky="e")
        self.from_entry = tk.Entry(form, width=10)
        self.from_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Do (HH:MM):").grid(row=1, column=0, sticky="e")
        self.to_entry = tk.Entry(form, width=10)
        self.to_entry.grid(row=1, column=1, padx=5)

        if self.shift:
            if isinstance(self.shift.start_time, (str, time)):
                self.from_entry.insert(0, str(self.shift.start_time))
            if isinstance(self.shift.end_time, (str, time)):
                self.to_entry.insert(0, str(self.shift.end_time))

        # --- Shift type ---
        tk.Label(form, text="Typ směny:").grid(row=2, column=0, sticky="e", pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(
            form,
            textvariable=self.type_var,
            state="readonly",
            values=[t.name for t in self.shift_types]
        )
        self.type_combo.grid(row=2, column=1, padx=5, pady=5)

        if self.shift:
            for t in self.shift_types:
                if t.shift_type_id == self.shift.type_shift_id:
                    self.type_var.set(t.name)
                    break
        else:
            if self.shift_types:
                self.type_var.set(self.shift_types[0].name)

        # --- Employees ---
        tk.Label(self, text="Přiřadit zaměstnance:", font=("Arial", 12)).pack(pady=10)
        emp_frame = tk.Frame(self)
        emp_frame.pack()

        for employee in self.employees:
            var = tk.BooleanVar(value=employee.employee_id in self.assigned_employee_ids)
            cb = tk.Checkbutton(
                emp_frame,
                text=f"{employee.first_name} {employee.last_name}",
                variable=var
            )
            cb.pack(anchor="w")
            self.employee_vars[employee.employee_id] = var

        # --- Buttons ---
        btns = tk.Frame(self)
        btns.pack(pady=15)

        tk.Button(btns, text="Uložit", command=self.save).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Zrušit", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

        # --- Delete button (only if editing existing shift) ---
        if self.shift and self.on_delete:
            tk.Button(
                btns,
                text="Smazat",
                bg="#f44336",
                fg="white",
                command=self.delete_shift
            ).pack(side=tk.LEFT, padx=5)

    def save(self):
        # Validate time format HH:MM
        try:
            start_time = datetime.strptime(self.from_entry.get(), "%H:%M").time()
            end_time = datetime.strptime(self.to_entry.get(), "%H:%M").time()
        except ValueError:
            messagebox.showerror("Chyba", "Časy musí být ve formátu HH:MM")
            return

        # Map shift type name to ID
        type_name = self.type_var.get()
        type_shift_id = next((t.shift_type_id for t in self.shift_types if t.name == type_name), None)
        if type_shift_id is None:
            messagebox.showerror("Chyba", "Vyberte typ směny")
            return

        # Get selected employees
        selected_employee_ids = [
            emp_id for emp_id, var in self.employee_vars.items() if var.get()
        ]

        # Create or update Shift object
        shift_id = self.shift.shift_id if self.shift else None
        shift = Shift(
            shift_id=shift_id,
            shift_date=self.date,
            start_time=start_time,
            end_time=end_time,
            type_shift_id=type_shift_id
        )

        # Pass both shift and selected employees to the callback
        self.on_save(shift, selected_employee_ids)

    def delete_shift(self):
        if messagebox.askyesno("Potvrdit smazání", "Opravdu chcete smazat tuto směnu?"):
            self.on_delete(self.shift)
