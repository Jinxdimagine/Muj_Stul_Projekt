import tkinter as tk


class DayDetailView(tk.Frame):
    def __init__(self, parent, date, day_data, on_back, on_add_shift):
        super().__init__(parent)

        self.date = date
        self.day_data = day_data
        self.on_back = on_back
        self.on_add_shift = on_add_shift

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text=f"Detail dne: {self.date}", font=("Arial", 18)).pack(pady=10)

        # -------- REZERVACE --------
        tk.Label(self, text="Rezervace", font=("Arial", 14)).pack(pady=5)

        for r in self.day_data["reservations"]:
            tk.Label(self, text=f"{r['time']} – {r['name']}").pack(anchor="w")

        # -------- SMĚNY --------
        tk.Label(self, text="Směny", font=("Arial", 14)).pack(pady=10)

        for s in self.day_data["shifts"]:
            text = f"{s['from']} - {s['to']} | {', '.join(s['employees'])}"
            tk.Label(self, text=text).pack(anchor="w")

        # -------- AKCE --------
        tk.Button(self, text="+ Přidat směnu", command=self.add_shift).pack(pady=10)
        tk.Button(self, text="Zpět", command=self.on_back).pack(pady=5)

    def add_shift(self):
        self.on_add_shift(self.date)
