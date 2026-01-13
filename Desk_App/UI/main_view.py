import tkinter as tk
from datetime import datetime, timedelta


class MainView(tk.Frame):
    def __init__(
            self,
            parent,
            on_new_employee,
            on_open_day,
            on_employee_list,
    ):
        super().__init__(parent)

        self.on_new_employee = on_new_employee
        self.on_employee_list = on_employee_list
        self.on_open_day = on_open_day

        self.current_month = datetime.now().replace(day=1)

        self.build_ui()
        self.pack(fill=tk.BOTH, expand=True)

    def build_ui(self):
        # ================= LEFT PANEL =================
        self.left = tk.LabelFrame(
            self,
            text="Rezervace / Zaměstnanci",
            width=300,
            height=500
        )
        self.left.pack(side=tk.LEFT, padx=10, pady=10)
        self.left.pack_propagate(False)

        self.listbox = tk.Listbox(self.left)
        self.listbox.pack(padx=10, pady=10, fill=tk.X)

        btn_frame = tk.Frame(self.left)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)

        tk.Button(btn_frame, text="Approve", command=self.approve).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=2
        )
        tk.Button(btn_frame, text="Deny", command=self.deny).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=2
        )

        tk.Label(self.left, text="Správa zaměstnanců").pack(pady=(15, 5))

        tk.Button(
            self.left,
            text="Nový zaměstnanec",
            command=self.on_new_employee
        ).pack(padx=10, pady=5, fill=tk.X)

        tk.Button(
            self.left,
            text="Seznam zaměstnanců",
            command=self.on_employee_list
        ).pack(padx=10, pady=5, fill=tk.X)

        # ================= RIGHT PANEL =================
        self.right = tk.Frame(self, bg="white")
        self.right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        nav = tk.Frame(self.right)
        nav.pack(fill=tk.X)

        tk.Button(nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav, font=("Arial", 14))
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.days_frame = tk.Frame(self.right)
        self.days_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.refresh_calendar()

    # ================== REZERVACE ==================
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

    # ================== KALENDÁŘ ==================
    def refresh_calendar(self):
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    def draw_calendar(self):
        # Clear previous calendar
        for w in self.days_frame.winfo_children():
            w.destroy()

        # Weekday headers
        days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, d in enumerate(days):
            tk.Label(self.days_frame, text=d).grid(row=0, column=i, sticky="nsew")

        # First weekday of month (0=Monday)
        start = self.current_month.weekday()

        # Days in month
        next_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        days_in_month = (next_month - timedelta(days=1)).day

        row, col = 1, start
        for day in range(1, days_in_month + 1):
            # Get full date string
            date_obj = self.current_month.replace(day=day)
            date_str = date_obj.strftime("%Y-%m-%d")

            # Create cell
            cell = tk.Frame(self.days_frame, bd=1, relief="solid")
            cell.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

            # Bind click — capture current date with default argument
            cell.bind("<Button-1>", lambda e, ds=date_str: self.on_open_day(ds))

            # Show day number
            tk.Label(cell, text=str(day), anchor="nw").pack(anchor="nw")

            # Move to next column/day
            col += 1
            if col > 6:
                col = 0
                row += 1

        # Make columns and rows expandable
        for i in range(7):
            self.days_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            self.days_frame.rowconfigure(i, weight=1)


    def prev_month(self):
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.refresh_calendar()

    def next_month(self):
        self.current_month = (
                self.current_month.replace(day=28) + timedelta(days=4)
        ).replace(day=1)
        self.refresh_calendar()
