import tkinter as tk
from UI.main_view import MainView
from UI.employee_new_form import EmployeeForm
from UI.day_detail_view import DayDetailView
from UI.employee_list_view import EmployeeListView
from UI.employee_detail_view import EmployeeDetailView
from UI.ShiftFormView import ShiftFormView

class Application:

    def __init__(self,employee_controller,reservation_controller,shift_controller,position_controller):
        self.employee_controller = employee_controller
        self.reservation_controller = reservation_controller
        self.shift_controller = shift_controller
        self.position_controller = position_controller
        self.root = tk.Tk()
        self.root.title("Desk GUI – DEMO")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        self.current_view = None
        self.show_main_view()
        self.employees = [
            {
                "id": 1,
                "first_name": "Petr",
                "last_name": "Novák",
                "position": "Číšník",
                "hour_rate": 180,
                "active": True
            },
            {
                "id": 2,
                "first_name": "Eva",
                "last_name": "Svobodová",
                "position": "Kuchař",
                "hour_rate": 220,
                "active": True
            }
        ]
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
            get_reservations=self.reservation_controller.get_reservations_by_date,
            on_employee_list=self.show_employee_list,
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

        self.refresh_main_view()

    def show_employee_form(self):
        self.clear_view()

        self.current_view = EmployeeForm(
            parent=self.root,
            on_save=self.save_employee,
            on_back=self.show_main_view,
            position_all=self.position_controller.get_all()
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_day_detail(self, date, day_data):
        self.clear_view()
        self.current_view = DayDetailView(
            parent=self.root,
            date=date,
            day_data=day_data,
            on_back=self.show_main_view,
            on_add_shift=self.show_shift_form
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_employee_list(self):
            self.clear_view()

            self.current_view = EmployeeListView(
                parent=self.root,
                employees=self.employee_controller.get_all,           # tvá dummy list / DAO data
                on_open_employee=self.show_employee_detail,
                on_back=self.show_main_view
            )
            self.current_view.pack(fill=tk.BOTH, expand=True)




    def show_employee_detail(self, employee_id):
        self.clear_view()

        employee = next(e for e in self.employees if e["id"] == employee_id)

        self.current_view = EmployeeDetailView(
            parent=self.root,
            employee=employee,
            on_back=self.show_employee_list,
            on_delete=self.delete_employee,
            on_save=self.save_employee_changes
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)


    def update_employee(self, employee_data):
        self.employee_controller.update(employee_data)
        self.show_employee_list()


    def save_employee_changes(self, updated):
        for i, e in enumerate(self.employees):
            if e["id"] == updated["id"]:
                self.employees[i] = updated
        self.show_employee_list()

    def delete_employee(self, employee_id):
        self.employees = [e for e in self.employees if e["id"] != employee_id]
        self.show_employee_list()

    def show_shift_form(self, date, shift=None):
        self.clear_view()

        employees = self.employee_controller.get_all()

        self.current_view = ShiftFormView(
            parent=self.root,
            date=date,
            employees=employees,
            shift=shift,
            on_save=self.save_shift,
            on_cancel=self.show_main_view
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def save_shift(self, shift_data):
        self.shift_controller.save_shift(shift_data)
        self.show_main_view()


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
        employee_data["position"]=self.position_controller.get_id_by_name(employee_data["position"])
        print("Nový zaměstnanec:", employee_data)
        self.employee_controller.add(employee_data)
        self.show_main_view()

    # -------------------------------------------------
    def run(self):
        self.root.mainloop()
