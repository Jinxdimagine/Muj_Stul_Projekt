import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class DayDetailView(tk.Frame):
    def __init__(self, parent, date, day_data, on_back, on_open_shift):
        """
        day_data: list of Shift objects for the day
        on_open_shift: callable(Shift or None) → called when a shift is clicked or new shift is added
        """
        super().__init__(parent)

        self.date = date
        self.day_data = day_data
        self.on_back = on_back
        self.on_open_shift = on_open_shift  # callback

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text=f"Detail dne: {self.date}", font=("Arial", 14, "bold")).pack(pady=5, anchor="w", padx=10)

        self.shifts_frame = tk.Frame(self)
        self.shifts_frame.pack(fill="both", expand=True, padx=10)

        self.display_shifts()

        # --- Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10, anchor="w", padx=10)

        tk.Button(
            btn_frame,
            text="+ Přidat směnu",
            width=12,
            bg="#4CAF50",
            fg="white",
            command=lambda: self.on_open_shift(None)  # None → create new shift
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Zpět",
            width=8,
            bg="#f44336",
            fg="white",
            command=self.on_back
        ).pack(side="left", padx=5)

    def display_shifts(self):
        # Clear previous shift widgets
        for widget in self.shifts_frame.winfo_children():
            widget.destroy()

        if not self.day_data:
            tk.Label(self.shifts_frame, text="Žádné směny.", fg="gray").pack(anchor="w")
            return

        for shift in self.day_data:
            start_time = shift.start_time.strftime("%H:%M") if hasattr(shift.start_time, "strftime") else str(shift.start_time)
            end_time = shift.end_time.strftime("%H:%M") if hasattr(shift.end_time, "strftime") else str(shift.end_time)
            shift_type = getattr(shift, "type_name", "")  # optional
            employees = ", ".join([f"{e.first_name} {e.last_name}" for e in getattr(shift, "employees", [])])

            text = f"{start_time} - {end_time} | {shift_type} | {employees}"

            # Each shift is a button to open for editing
            btn = tk.Button(
                self.shifts_frame,
                text=text,
                anchor="w",
                command=lambda s=shift: self.on_open_shift(s)
            )
            btn.pack(fill="x", pady=2)
