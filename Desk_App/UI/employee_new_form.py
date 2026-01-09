import tkinter as tk
from tkinter import messagebox,ttk
import re
class EmployeeForm(tk.Frame):
    def __init__(self, parent, on_save, on_back,position_all):
        super().__init__(parent)

        self.on_save = on_save
        self.on_back = on_back
        self.position_all = position_all
        tk.Label(self, text="Nový zaměstnanec", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Jméno").pack()
        self.name = tk.Entry(self)
        self.name.pack()

        tk.Label(self, text="Příjmení").pack()
        self.surname = tk.Entry(self)
        self.surname.pack()
        tk.Label(self,text=" Datum Narozeni(DD.MM.RRRR) ").pack()
        self.birth_date=tk.Entry(self)
        self.birth_date.pack()
        list_positions=self.position_names(position_all)
        tk.Label(self, text="Pozice").pack()
        self.position_var = tk.StringVar()
        self.position_combo = ttk.Combobox(
            self,
            textvariable=self.position_var,
            state="readonly",
            values=list_positions
        )
        self.position_combo.pack()
        self.position_combo.current(0)

        tk.Label(self, text="Hodinova sazba").pack()
        self.hour_rate = tk.Entry(self)
        self.hour_rate.pack()

        tk.Button(self, text="Uložit", command=self.save).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack()

    def save(self):
        if (
                not self.name.get() or
                not self.surname.get() or
                not self.position_combo.get() or
                not self.birth_date.get() or
                not self.hour_rate.get()
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
        hour_rate_patern="^[0-9]+$"
        if not re.match(hour_rate_patern,self.hour_rate.get()):
            messagebox.showerror(
                "Chyba",
                "Hodinova sazba musi byt cislo"
            )
            return
        self.on_save({
            "first_name": self.name.get(),
            "last_name": self.surname.get(),
            "position": self.position_combo.get(),
            "birth_date": self.birth_date.get(),
            "hour_rate": self.hour_rate.get()
        })


    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()

    def position_names(self,positions):
        list=[]
        for r in positions:
            list.append(str(r))
        return list