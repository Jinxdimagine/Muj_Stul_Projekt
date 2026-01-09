import tkinter as tk


class EmployeeListView(tk.Frame):
    def __init__(self, parent, employees, on_open_employee, on_back):
        super().__init__(parent)
        self.on_open_employee = on_open_employee
        self.on_back = on_back
        self.employees = list(employees)

        tk.Label(self, text="Seznam zaměstnanců", font=("Arial", 18)).pack(pady=10)

        self.listbox = tk.Listbox(self, width=40, height=15)
        self.listbox.pack(pady=10)

        for employee in self.employees:
            self.listbox.insert(
                tk.END, f"{employee.employee_id} – {employee.first_name} {employee.last_name}")

        tk.Button(self, text="Otevřít profil", command=self.open_selected).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack(pady=5)

    def open_selected(self):
        if not self.listbox.curselection():
            return

        index = self.listbox.curselection()[0]
        employee = self.employees[index]
        self.on_open_employee(employee.employee_id)
