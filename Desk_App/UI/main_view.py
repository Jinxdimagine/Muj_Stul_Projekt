import tkinter as tk
from datetime import datetime, timedelta


class MainView(tk.Frame):
    def __init__(self, parent, on_approve, on_deny, on_new_employee, on_open_day, get_reservations):
        super().__init__(parent)
        self.parent = parent
        self.on_approve = on_approve
        self.on_deny = on_deny
        self.on_new_employee = on_new_employee
        self.get_reservations = get_reservations
        self.on_open_day = on_open_day
        self.current_month = datetime.now().replace(day=1)

        self.build_ui()
        self.pack(fill=tk.BOTH, expand=True)

    def build_ui(self):
        # ---------------- levý panel ----------------
        self.left = tk.LabelFrame(
            self.parent, text="Rezervace na vyřízení", width=300, height=400
        )
        self.left.place(x=10, y=10)
        self.left.pack_propagate(False)

        self.listbox = tk.Listbox(self.left)
        self.listbox.place(x=10, y=10, width=280, height=250)

        tk.Button(self.left, text="Approve", command=self.approve).place(
            x=10, y=270, width=135, height=30
        )
        tk.Button(self.left, text="Deny", command=self.deny).place(
            x=155, y=270, width=135, height=30
        )

        tk.Label(self.left, text="Správa zaměstnanců").place(x=10, y=320)
        tk.Button(
            self.left, text="Nový zaměstnanec", command=self.on_new_employee
        ).place(x=10, y=350, width=280, height=30)

        # ---------------- pravý panel (kalendář) ----------------
        self.right = tk.Frame(self.parent, bg="white", width=650, height=500)
        self.right.place(x=320, y=10)
        self.right.pack_propagate(False)

        nav = tk.Frame(self.right)
        nav.pack(fill=tk.X, pady=5)

        tk.Button(nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav, font=("Arial", 14))
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.days_frame = tk.Frame(self.right, bg="white")
        self.days_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.refresh_calendar()

    # ---------------- Rezervace ----------------
    def set_reservations(self, reservations):
        self.listbox.delete(0, tk.END)
        for r in reservations:
            self.listbox.insert(
                tk.END, f"{r['name']} {r['surname']} – {r['date']} {r['time']}"
            )

    def approve(self):
        if self.listbox.curselection():
            self.on_approve(self.listbox.curselection()[0])

    def deny(self):
        if self.listbox.curselection():
            self.on_deny(self.listbox.curselection()[0])

    # ---------------- Kalendář ----------------
    def refresh_calendar(self):
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    def draw_calendar(self):
        for w in self.days_frame.winfo_children():
            w.destroy()

        days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, d in enumerate(days):
            tk.Label(
                self.days_frame, text=d, relief="solid"
            ).grid(row=0, column=i, sticky="nsew")

        start = self.current_month.weekday()
        next_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(
            day=1
        )
        days_in_month = (next_month - timedelta(days=1)).day

        grouped = self.get_reservations()

        row, col = 1, start
        for day in range(1, days_in_month + 1):
            date = self.current_month.replace(day=day)
            date_str = date.strftime("%Y-%m-%d")

            cell = tk.Frame(self.days_frame, relief="solid", borderwidth=1)
            cell.grid(row=row, column=col, sticky="nsew")

            # lambda fix pro předání date_str a day_data
            def on_click(d=date_str):
                day_data = self.get_day_data(d)
                self.open_day(d, day_data)

            cell.bind("<Button-1>", lambda e, f=on_click: f())

            tk.Label(cell, text=str(day), anchor="nw").pack(anchor="nw")

            for r in grouped.get(date_str, []):
                tk.Label(
                    cell,
                    text=f"{r['name']} ({r['people']})",
                    font=("Arial", 8),
                    anchor="w",
                ).pack(anchor="w")

            col += 1
            if col > 6:
                col = 0
                row += 1

        for i in range(row + 1):
            self.days_frame.rowconfigure(i, weight=1)
        for i in range(7):
            self.days_frame.columnconfigure(i, weight=1)

    def get_day_data(self, date_str):
        # dummy data pro testování
        return {
            "reservations": [
                {"name": "Novák", "time": "14:00"},
                {"name": "Svoboda", "time": "17:30"},
            ],
            "shifts": [
                {"employee": "Petr", "from": "8:00", "to": "16:00"},
                {"employee": "Eva", "from": "12:00", "to": "20:00"},
            ],
        }

    def open_day(self, date_str, day_data):
        self.on_open_day(date_str, day_data)

    # ---------- Navigace měsíců ----------
    def prev_month(self):
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.refresh_calendar()

    def next_month(self):
        self.current_month = (
                self.current_month.replace(day=28) + timedelta(days=4)
        ).replace(day=1)
        self.refresh_calendar()

    # ---------------- zobrazení / skrytí ----------------
    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
