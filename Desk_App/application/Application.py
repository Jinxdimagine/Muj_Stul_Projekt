import tkinter as tk
from UI.main_view import MainView
from UI.employee_form import EmployeeForm
from UI.day_detail_view import DayDetailView


class Application:
    def __init__(self, employee_controller, reservation_controller):
        self.employee_controller = employee_controller
        self.reservation_controller = reservation_controller

        self.root = tk.Tk()
        self.root.title("Desk GUI – DEMO")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        # 🔑 DŮLEŽITÉ
        self.current_view = None

        self.show_main_view()

    # -------------------------------------------------
    # VIEW MANAGEMENT
    # -------------------------------------------------
    def clear_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def show_main_view(self):
        self.clear_view()

        self.current_view = MainView(
            parent=self.root,
            on_approve=self.approve_reservation,
            on_deny=self.deny_reservation,
            on_new_employee=self.show_employee_form,
            on_open_day=self.show_day_detail,
            get_reservations=self.reservation_controller.get_reservations_by_date
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

        self.refresh_main_view()

    def show_employee_form(self):
        self.clear_view()

        self.current_view = EmployeeForm(
            parent=self.root,
            on_save=self.save_employee,
            on_back=self.show_main_view
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_day_detail(self, date, day_data):
        self.clear_view()

        self.current_view = DayDetailView(
            parent=self.root,
            date=date,
            day_data=day_data,
            on_back=self.show_main_view
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    # -------------------------------------------------
    # CALLBACKS
    # -------------------------------------------------
    def refresh_main_view(self):
        if isinstance(self.current_view, MainView):
            self.current_view.set_reservations(
                self.reservation_controller.get_all()
            )

    def approve_reservation(self, index):
        self.reservation_controller.approve(index)
        self.refresh_main_view()

    def deny_reservation(self, index):
        self.reservation_controller.deny(index)
        self.refresh_main_view()

    def save_employee(self, employee_data):
        self.employee_controller.add_employee(employee_data)
        print("Nový zaměstnanec:", employee_data)
        self.show_main_view()

    # -------------------------------------------------
    def run(self):
        self.root.mainloop()
