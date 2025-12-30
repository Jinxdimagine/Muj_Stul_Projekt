import tkinter as tk


class DayDetailView(tk.Frame):
    def __init__(self, parent, date, day_data, on_back):
        super().__init__(parent)

        self.date = date
        self.day_data = day_data
        self.on_back = on_back

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text=f"Detail dne {self.date}",
            font=("Arial", 16)
        ).pack(pady=10)

        content = tk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ---------- Rezervace ----------
        res_frame = tk.LabelFrame(content, text="Rezervace")
        res_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        res_list = tk.Listbox(res_frame)
        res_list.pack(fill=tk.BOTH, expand=True)

        for r in self.day_data.get("reservations", []):
            res_list.insert(tk.END, f"{r['name']} – {r['time']}")

        # ---------- Směny ----------
        shift_frame = tk.LabelFrame(content, text="Směny")
        shift_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        shift_list = tk.Listbox(shift_frame)
        shift_list.pack(fill=tk.BOTH, expand=True)

        for s in self.day_data.get("shifts", []):
            shift_list.insert(
                tk.END, f"{s['employee']} {s['from']}–{s['to']}"
            )

        # ---------- Ovládání ----------
        bottom = tk.Frame(self)
        bottom.pack(fill=tk.X, pady=10)

        tk.Button(bottom, text="⬅ Zpět na kalendář", command=self.on_back) \
            .pack(side=tk.LEFT, padx=10)
