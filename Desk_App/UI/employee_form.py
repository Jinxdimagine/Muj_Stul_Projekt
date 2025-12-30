import tkinter as tk
from tkinter import messagebox

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

        tk.Button(self, text="Uložit", command=self.save).pack(pady=5)
        tk.Button(self, text="Zpět", command=self.on_back).pack()

    def save(self):
        if not self.name.get() or not self.surname.get() or not self.position.get():
            messagebox.showerror("Chyba", "Vyplň všechna pole")
            return
        self.on_save({
            "name": self.name.get(),
            "surname": self.surname.get(),
            "position": self.position.get()
        })

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
