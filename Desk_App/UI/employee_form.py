import tkinter as tk
from tkinter import messagebox,ttk
import re
class EmployeeForm(tk.Frame):
    def __init__(self, parent, on_save, on_back):
        super().__init__(parent)

        self.on_save = on_save
        self.on_back = on_back

        tk.Label(self, text="Nový zaměstnanec", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Jméno").pack()
        self.name = tk.Entry(self)
        self.name.pack()

        tk.Label(self, text="Příjmení").pack()
        self.surname = tk.Entry(self)
        self.surname.pack()

        tk.Label(self, text="Pozice").pack()
        self.position = tk.Entry(self)
        self.position.pack()

        tk.Label(self,text=" Datum Narozeni(DD.MM.RRRR) ").pack()
        self.birth_date=tk.Entry(self)
        self.birth_date.pack()
        tk.Label(self, text="Pozice").pack()

        self.position_var = tk.StringVar()
        self.position_combo = ttk.Combobox(
            self,
            textvariable=self.position_var,
            state="readonly",
            values=["Číšník", "Barman", "Kuchař"]
        )
        self.position_combo.pack()
        self.position_combo.current(0)
        tk.Button(self, text="Uložit", command=self.save).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack()

    def save(self):
        if (
                not self.name.get() or
                not self.surname.get() or
                not self.position.get() or
                not self.birth_date.get()
        ):
            messagebox.showerror("Chyba", "Vyplň všechna pole")
            return

        date_pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"

        if not re.match(date_pattern, self.birth_date.get()):
            messagebox.showerror(
                "Chyba",
                "Datum narození musí být ve formátu DD.MM.RRRR"
            )
            return

        self.on_save({
            "name": self.name.get(),
            "surname": self.surname.get(),
            "position": self.position.get(),
            "birth_date": self.birth_date.get()
        })


    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
