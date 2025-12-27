import tkinter as tk
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

        # --- Levý panel (LabelFrame, fixní velikost) ---
        self.left_panel = tk.LabelFrame(self.root, text="Rezervace na vyřízení", width=300, height=500)
        self.left_panel.place(x=10, y=10)  # pevná pozice
        self.left_panel.pack_propagate(False)  # zachová pevnou velikost

        # Listbox uvnitř levého panelu
        self.listbox = tk.Listbox(self.left_panel)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tlačítka approve/deny - roztažená co nejvíce od sebe
        btn_frame = tk.Frame(self.left_panel)
        btn_frame.pack(fill=tk.X, pady=5, padx=5)

        tk.Button(btn_frame, text="Approve", command=self.approve).grid(row=0, column=0, sticky="w")
        tk.Button(btn_frame, text="Deny", command=self.deny).grid(row=0, column=1, sticky="e")

        # Roztažení sloupců
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

# --- Pravý panel (kalendář) ---
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.place(x=320, y=10, relwidth=1, width=-330, relheight=1, height=-20)

        self.current_month = datetime.now().replace(day=1)

        # Navigace kalendáře
        cal_nav = tk.Frame(self.right_frame)
        cal_nav.pack(pady=5)
        tk.Button(cal_nav, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(cal_nav, text=self.current_month.strftime("%B %Y"), font=("Arial", 14))
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(cal_nav, text=">", command=self.next_month).pack(side=tk.LEFT)

        # Mřížka dnů
        self.days_frame = tk.Frame(self.right_frame)
        self.days_frame.pack(fill=tk.BOTH, expand=True)

        self.draw_calendar()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- Rezervace ---
    def add_reservation(self, data):
        def add():
            if data in self.list:
                return
            name = data.get('name', 'Unknown')
            surname = data.get('surname', '')
            people = data.get('people', 'N/A')
            date = data.get('date', 'N/A')
            time = data.get('time', 'N/A')
            item_text = f"{name} {surname} - {people} people at {date} {time}"
            self.list.append(data)
            self.listbox.insert(tk.END, item_text)
            self.draw_calendar()
        self.root.after(0, add)

    def approve(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        data_item = self.list[idx]
        self.listbox.delete(idx)
        self.list.pop(idx)
        print("APPROVED:", data_item)
        self.ws.send_sync({"type": "decision", "status": "approved", "item": data_item})
        self.draw_calendar()

    def deny(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        data_item = self.list[idx]
        self.listbox.delete(idx)
        self.list.pop(idx)
        print("DENIED:", data_item)
        self.ws.send_sync({"type": "decision", "status": "denied", "item": data_item})
        self.draw_calendar()

    # --- Kalendář ---
    def draw_calendar(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        days_name = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
        for i, day_name in enumerate(days_name):
            tk.Label(self.days_frame, text=day_name, width=15, borderwidth=1, relief="solid").grid(row=0, column=i)

        first_day = self.current_month.replace(day=1)
        start_weekday = first_day.weekday()
        days_in_month = (self.current_month.replace(month=self.current_month.month % 12 + 1, day=1) - timedelta(days=1)).day

        res_by_date = defaultdict(list)
        for r in self.list:
            res_by_date[r['date']].append(r)

        row = 1
        col = start_weekday
        for day in range(1, days_in_month + 1):
            date_str = self.current_month.replace(day=day).strftime("%Y-%m-%d")
            day_res = res_by_date.get(date_str, [])
            text = str(day)
            if day_res:
                text += "\n" + "\n".join([f"{r['name']} {r.get('surname','')} ({r['people']})" for r in day_res])
            tk.Label(self.days_frame, text=text, width=15, height=5, borderwidth=1, relief="solid",
                     anchor="nw", justify="left").grid(row=row, column=col)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        self.current_month = (self.current_month.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    def next_month(self):
        next_month = self.current_month.replace(day=28) + timedelta(days=4)
        self.current_month = next_month.replace(day=1)
        self.month_label.config(text=self.current_month.strftime("%B %Y"))
        self.draw_calendar()

    # --- Ukončení aplikace ---
    def on_close(self):
        self.ws.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
