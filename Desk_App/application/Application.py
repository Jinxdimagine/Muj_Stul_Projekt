import tkinter as tk
from UI.main_view import MainView
from UI.employee_form import EmployeeForm

class Application:
    def __init__(self,employee_controller,reservation_controller):
        self.employee_controller = employee_controller
        self.reservation_controller = reservation_controller

        self.root = tk.Tk()
        self.root.title("Desk GUI – DEMO")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        # --- main view ---
        self.main_view = MainView(
            parent=self.root,
            on_approve=self.approve_reservation,
            on_deny=self.deny_reservation,
            on_new_employee=self.show_employee_form,
            get_reservations=self.reservation_controller.get_reservations_by_date
        )
        self.main_view.show()

        # --- employee form ---
        self.employee_form = EmployeeForm(
            parent=self.root,
            on_save=self.save_employee,
            on_back=self.show_main_view
        )
        self.refresh_main_view()

    # ---------- callbacks ----------
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

    # ---------- UI control ----------
    def refresh_main_view(self):
        self.main_view.set_reservations(self.reservation_controller.get_all())
        print(self.reservation_controller.get_all())
        print("Refresh main view")

    def show_main_view(self):
        self.employee_form.hide()
        self.main_view.show()
        self.refresh_main_view()

    def show_employee_form(self):
        self.main_view.hide()
        self.employee_form.show()

    def run(self):
        self.root.mainloop()
