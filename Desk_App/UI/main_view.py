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

        # definice atributů
        self.left = None
        self.listbox = None
        self.right = None
        self.days_frame = None
        self.month_label = None

        self.build_ui()
        self.pack(fill=tk.BOTH, expand=True)

    def build_ui(self):
        # ---------------- levý panel – fixní pozice vlevo nahoře ----------------
        self.left = tk.LabelFrame(self.parent, text="Rezervace na vyřízení", width=300, height=400)
        self.left.place(x=10, y=10)  # pevná pozice v okně
        self.left.pack_propagate(False)  # zachová pevnou velikost panelu

        # Listbox – nahoře v panelu
        self.listbox = tk.Listbox(self.left)
        self.listbox.place(x=10, y=10, width=280, height=250)  # pevná pozice a velikost

        # tlačítka approve/deny pod Listboxem
        btn_approve = tk.Button(self.left, text="Approve", command=self.approve)
        btn_deny = tk.Button(self.left, text="Deny", command=self.deny)
        btn_approve.place(x=10, y=270, width=135, height=30)
        btn_deny.place(x=155, y=270, width=135, height=30)

        # label a button pro nového zaměstnance – dole v panelu
        tk.Label(self.left, text="Správa zaměstnanců").place(x=10, y=320)
        tk.Button(self.left, text="Nový zaměstnanec", command=self.on_new_employee).place(x=10, y=350, width=280, height=30)
        # ---------------- pravý panel (kalendář) – fixní pozice vedle levého ----------------
        self.right = tk.Frame(self.parent, bg="white", width=650, height=500)
        self.right.place(x=320, y=10)  # pevná pozice vedle levého panelu
        self.right.pack_propagate(False)

        # navigace kalendáře
        nav = tk.Frame(self.right, height=30)
        nav.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Button(nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav, font=("Arial", 14))
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        # mřížka dnů – zabírá zbytek panelu
        self.days_frame = tk.Frame(self.right, bg="white")
        self.days_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # nakreslení kalendáře
        self.refresh_calendar()



    # ---------- Listbox ----------
    def set_reservations(self, reservations):
        self.listbox.delete(0, tk.END)
        for r in reservations:
            self.listbox.insert(tk.END, f"{r['name']} {r['surname']} – {r['date']} {r['time']}")
        self.refresh_calendar()

    def approve(self):
        if self.listbox.curselection():
            self.on_approve(self.listbox.curselection()[0])

    def deny(self):
        if self.listbox.curselection():
            self.on_deny(self.listbox.curselection()[0])

    # ---------- Kalendář ----------
    def refresh_calendar(self):
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    def draw_calendar(self):
        for w in self.days_frame.winfo_children():
            w.destroy()

        days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, d in enumerate(days):
            tk.Label(self.days_frame, text=d, width=15, relief="solid").grid(row=0, column=i, sticky="nsew")

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

            lbl = tk.Label(
                self.days_frame,
                text=text,
                width=15,
                height=5,
                anchor="nw",
                justify="left",
                relief="solid"
            )
            lbl.grid(row=row, column=col, sticky="nsew")  # přidán sticky

            col += 1
            if col > 6:
                col = 0
                row += 1

        # roztažení všech řádků a sloupců, aby se zobrazil celý obsah
        for i in range(row + 1):
            self.days_frame.rowconfigure(i, weight=1)
        for i in range(7):
            self.days_frame.columnconfigure(i, weight=1)

    # ---------- Navigace měsíců ----------
    def prev_month(self):
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.refresh_calendar()

    def next_month(self):
        self.current_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.refresh_calendar()
    # ---------------- zobrazení / skrytí ----------------
    def show(self):
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.pack_forget()
