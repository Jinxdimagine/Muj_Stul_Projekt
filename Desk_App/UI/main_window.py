import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from collections import defaultdict


class DeskGUI:
    def __init__(self, ws):
        self.ws = ws
        self.list = []

        # --- Hlavní okno ---
        self.root = tk.Tk()
        self.root.title("Muj_Stul-Viet_Fusion")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        # --- Hlavní obsahový frame ---
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.current_month = datetime.now().replace(day=1)

        self.show_main_view()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------------------------------------------
    # Pomocné funkce
    # -------------------------------------------------
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # -------------------------------------------------
    # HLAVNÍ POHLED
    # -------------------------------------------------
    def show_main_view(self):
        self.clear_content()

        # --- Levý panel ---
        self.left_panel = tk.LabelFrame(
            self.content_frame,
            text="Rezervace na vyřízení",
            width=300,
            height=500
        )
        self.left_panel.place(x=10, y=10)
        self.left_panel.pack_propagate(False)

        self.listbox = tk.Listbox(self.left_panel)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_frame = tk.Frame(self.left_panel)
        btn_frame.pack(fill=tk.X, pady=5, padx=5)

        tk.Button(btn_frame, text="Approve", command=self.approve).grid(row=0, column=0, sticky="w")
        tk.Button(btn_frame, text="Deny", command=self.deny).grid(row=0, column=1, sticky="e")

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        # --- Nový zaměstnanec ---
        tk.Button(
            self.left_panel,
            text="Nový zaměstnanec",
            command=self.show_employee_form
        ).pack(pady=5)

        # --- Pravý panel (kalendář) ---
        self.right_frame = tk.Frame(self.content_frame, bg="white")
        self.right_frame.place(x=320, y=10, relwidth=1, width=-330, relheight=1, height=-20)

        # Navigace kalendáře
        cal_nav = tk.Frame(self.right_frame)
        cal_nav.pack(pady=5)

        tk.Button(cal_nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(
            cal_nav,
            text=self.current_month.strftime("%B %Y"),
            font=("Arial", 14)
        )
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(cal_nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        self.days_frame = tk.Frame(self.right_frame)
        self.days_frame.pack(fill=tk.BOTH, expand=True)

        self.draw_calendar()

    # -------------------------------------------------
    # FORMULÁŘ ZAMĚSTNANCE
    # -------------------------------------------------
    def show_employee_form(self):
        self.clear_content()

        frame = tk.Frame(self.content_frame)
        frame.pack(expand=True)

        tk.Label(frame, text="Nový zaměstnanec", font=("Arial", 18)).pack(pady=10)

        tk.Label(frame, text="Jméno").pack()
        name_entry = tk.Entry(frame, width=30)
        name_entry.pack()

        tk.Label(frame, text="Příjmení").pack()
        surname_entry = tk.Entry(frame, width=30)
        surname_entry.pack()

        tk.Label(frame, text="Pozice").pack()
        position_entry = tk.Entry(frame, width=30)
        position_entry.pack()

        def save_employee():
            name = name_entry.get()
            surname = surname_entry.get()
            position = position_entry.get()

            if not name or not surname or not position:
                messagebox.showerror("Chyba", "Vyplň všechna pole")
                return

            print("NOVÝ ZAMĚSTNANEC:", name, surname, position)

            self.show_main_view()

        tk.Button(frame, text="Uložit", command=save_employee).pack(pady=10)
        tk.Button(frame, text="Zpět", command=self.show_main_view).pack()

    # -------------------------------------------------
    # REZERVACE
    # -------------------------------------------------
    def add_reservation(self, data):
        def add():
            if data in self.list:
                return

            name = data.get("name", "Unknown")
            surname = data.get("surname", "")
            people = data.get("people", "N/A")
            date = data.get("date", "N/A")
            time = data.get("time", "N/A")

            text = f"{name} {surname} - {people} lidí {date} {time}"
            self.list.append(data)
            self.listbox.insert(tk.END, text)
            self.draw_calendar()

        self.root.after(0, add)

    def approve(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.list.pop(idx)
        self.listbox.delete(idx)
        print("APPROVED:", item)
        self.ws.send_sync({"type": "decision", "status": "approved", "item": item})
        self.draw_calendar()

    def deny(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.list.pop(idx)
        self.listbox.delete(idx)
        print("DENIED:", item)
        self.ws.send_sync({"type": "decision", "status": "denied", "item": item})
        self.draw_calendar()

    # -------------------------------------------------
    # KALENDÁŘ
    # -------------------------------------------------
    def draw_calendar(self):
        for w in self.days_frame.winfo_children():
            w.destroy()

        days = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, d in enumerate(days):
            tk.Label(self.days_frame, text=d, width=15, relief="solid").grid(row=0, column=i)

        first_day = self.current_month
        start_col = first_day.weekday()
        next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
        days_in_month = (next_month - timedelta(days=1)).day

        res_by_date = defaultdict(list)
        for r in self.list:
            res_by_date[r["date"]].append(r)

        row, col = 1, start_col
        for day in range(1, days_in_month + 1):
            date_str = self.current_month.replace(day=day).strftime("%Y-%m-%d")
            text = str(day)

            if date_str in res_by_date:
                for r in res_by_date[date_str]:
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
        self.show_main_view()

    def next_month(self):
        self.current_month = (self.current_month.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.show_main_view()

    # -------------------------------------------------
    # UKONČENÍ
    # -------------------------------------------------
    def on_close(self):
        self.ws.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
