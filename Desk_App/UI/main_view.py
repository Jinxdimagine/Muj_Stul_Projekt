import tkinter as tk
from datetime import datetime, timedelta

class MainView(tk.Frame):
    def __init__(self, parent, on_approve, on_deny, on_new_employee, get_reservations):
        super().__init__(parent)
        self.parent = parent
        self.on_approve = on_approve
        self.on_deny = on_deny
        self.on_new_employee = on_new_employee
        self.get_reservations = get_reservations

        self.current_month = datetime.now().replace(day=1)
        self.build_ui()

    def build_ui(self):
        # levý panel – rezervace
        self.left = tk.LabelFrame(self, text="Rezervace na vyřízení", width=300)
        self.left.place(x=10, y=10)
        self.left.pack_propagate(False)

        self.listbox = tk.Listbox(self.left)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btns = tk.Frame(self.left)
        btns.pack(fill=tk.X)
        tk.Button(btns, text="Approve", command=self.approve).grid(row=0, column=0, sticky="w")
        tk.Button(btns, text="Deny", command=self.deny).grid(row=0, column=1, sticky="e")
        btns.grid_columnconfigure(0, weight=1)
        btns.grid_columnconfigure(1, weight=1)

        tk.Button(self.left, text="Nový zaměstnanec", command=self.on_new_employee).pack(pady=5)

        # pravý panel – kalendář
        self.right = tk.Frame(self, bg="white")
        self.right.place(x=320, y=10, relwidth=1, width=-330, relheight=1, height=-20)

        nav = tk.Frame(self.right)
        nav.pack()
        tk.Button(nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav, font=("Arial", 14))
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.days_frame = tk.Frame(self.right)
        self.days_frame.pack(fill=tk.BOTH, expand=True)

        self.refresh_calendar()

    # ---------- API ----------
    def set_reservations(self, reservations):
        self.listbox.delete(0, tk.END)
        for r in reservations:
            self.listbox.insert(tk.END, f"{r['name']} {r['surname']} – {r['date']} {r['time']}")
        self.refresh_calendar()

    # ---------- callbacks ----------
    def approve(self):
        if self.listbox.curselection():
            self.on_approve(self.listbox.curselection()[0])

    def deny(self):
        if self.listbox.curselection():
            self.on_deny(self.listbox.curselection()[0])

    # ---------- kalendář ----------
    def refresh_calendar(self):
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    def draw_calendar(self):
        for w in self.days_frame.winfo_children():
            w.destroy()

        days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, d in enumerate(days):
            tk.Label(self.days_frame, text=d, width=15, relief="solid").grid(row=0, column=i)

        start = self.current_month.weekday()
        next_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        days_in_month = (next_month - timedelta(days=1)).day

        grouped = self.get_reservations()

        row, col = 1, start
        for day in range(1, days_in_month + 1):
            date_str = self.current_month.replace(day=day).strftime("%Y-%m-%d")
            text = str(day)
            for r in grouped.get(date_str, []):
                text += f"\n{r['name']} ({r['people']})"

            tk.Label(
                self.days_frame,
                text=text,
                width=15,
                height=5,
                anchor="nw",
                justify="left",
                relief="solid"
            ).grid(row=row, column=col)

            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.refresh_calendar()

    def next_month(self):
        self.current_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.refresh_calendar()

    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
