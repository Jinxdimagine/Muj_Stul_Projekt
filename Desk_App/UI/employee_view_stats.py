import tkinter as tk
from tkinter import ttk

class EmployeeStatsView(tk.Frame):
    def __init__(self, parent, stats, on_back):
        super().__init__(parent)

        print("STATS IN VIEW:", stats)

        tk.Label(
            self,
            text="Statistika zaměstnanců podle pozic",
            font=("Arial", 18)
        ).pack(pady=10)

        if not stats:
            tk.Label(self, text="Žádná data k zobrazení").pack()
            return

        columns = ("position", "employees", "shifts")

        tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=8
        )

        # Nadpisy a centrování sloupců
        tree.heading("position", text="Pozice", anchor="center")
        tree.heading("employees", text="Počet zaměstnanců", anchor="center")
        tree.heading("shifts", text="Počet směn", anchor="center")

        tree.column("position", anchor="center", width=150)
        tree.column("employees", anchor="center", width=120)
        tree.column("shifts", anchor="center", width=100)

        # Vkládání dat
        for row in stats:
            tree.insert(
                "",
                "end",
                values=(
                    row["position_name"],
                    row["employee_count"],
                    row["total_shifts"]
                )
            )

        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Button(self, text="Zpět", command=on_back).pack(pady=10)
