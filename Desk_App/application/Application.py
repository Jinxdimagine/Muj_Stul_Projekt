import tkinter as tk
from Entity.Shift import Shift  # make sure this import is at the top
from UI.main_view import MainView
from UI.employee_new_form import EmployeeForm
from UI.day_detail_view import DayDetailView
from UI.employee_list_view import EmployeeListView
from UI.employee_detail_view import EmployeeDetailView
from UI.ShiftFormView import ShiftFormView

class Application:

    def __init__(self,employee_controller,shift_controller,position_controller,shift_type_controller):
        self.employee_controller = employee_controller
        self.shift_controller = shift_controller
        self.position_controller = position_controller
        self.shift_type_controller = shift_type_controller
        self.root = tk.Tk()
        self.root.title("Desk GUI – DEMO")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

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
            on_new_employee=self.show_employee_form,
            on_open_day=self.show_day_detail,
            on_employee_list=self.show_employee_list,
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)


    def show_employee_form(self):
        self.clear_view()

        self.current_view = EmployeeForm(
            parent=self.root,
            on_save=self.save_employee,
            on_back=self.show_main_view,
            positions=self.position_controller.get_all()
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)


    def show_shift_form(self, shift_or_date, date):
        self.clear_view()

        # Check if we are editing an existing shift
        is_editing = isinstance(shift_or_date, Shift)
        shift = shift_or_date if is_editing else None

        # on_delete callback
        on_delete_callback = None
        if is_editing:
            def on_delete_callback(shift_to_delete):
                self.shift_controller.delete_shift(shift_to_delete.shift_id)
                self.show_day_detail(date)  # refresh the day view

        # Assigned employees (only if editing)
        assigned_employee_ids = getattr(shift, "employee_ids", []) if is_editing else []

        self.current_view = ShiftFormView(
            parent=self.root,
            date=date,
            shift_types=self.shift_type_controller.get_all(),
            employees=self.employee_controller.get_all(),
            shift=shift,
            assigned_employee_ids=assigned_employee_ids,
            on_save=self.save_shift,
            on_cancel=lambda d=date: self.show_day_detail(d),
            on_delete=on_delete_callback
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)



    def show_employee_list(self):
            self.clear_view()
            self.current_view = EmployeeListView(
                parent=self.root,
                employees=self.employee_controller.get_all(),
                employee_show=self.employee_controller.get_all_view(),
                on_open_employee=self.show_employee_detail,
                on_back=self.show_main_view
            )
            self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_day_detail(self, date):
        self.clear_view()

    # Fetch shifts for the day
        day_data = self.shift_controller.get_shifts_by_date(date)

        # If there are no shifts, do nothing (or optionally show a message)
        if not day_data:
            print(f"No shifts for {date}")  # simple console log
            # Optionally, you could show a messagebox:
            # messagebox.showinfo("Info", f"No shifts scheduled for {date}")
            return

        # If there are shifts, show them
        self.current_view = DayDetailView(
            parent=self.root,
            date=date,
            day_data=day_data,
            on_back=self.show_main_view,
            on_open_shift=lambda shift: self.show_shift_form(shift, date)
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)



    def show_employee_detail(self, employee_id):
        self.clear_view()
        self.current_view = EmployeeDetailView(
            parent=self.root,
            employee=self.employee_controller.get_by_id(employee_id),
            positions=self.position_controller.get_all(),
            on_back=self.show_employee_list,
            on_delete=self.delete_employee,
            on_save=self.update_employee
        )
        self.current_view.pack(fill=tk.BOTH, expand=True)


    def update_employee(self, employee_data):
        self.employee_controller.update(employee_data)
        self.show_employee_list()

    def delete_employee(self, employee_id):
        print(employee_id)
        self.employee_controller.delete(employee_id)
        self.show_employee_list()


    def save_shift(self, shift_data,selected_employess):
        if shift_data.shift_id is not None:
            self.shift_controller.update(shift_data,selected_employess)
        else:
            self.shift_controller.add_shift(shift_data,selected_employess)
        self.show_main_view()


    # -------------------------------------------------
    # CALLBACKS
    # -------------------------------------------------

    def save_employee(self, employee_data):
        print("Nový zaměstnanec:", employee_data)
        self.employee_controller.add(employee_data)
        self.show_main_view()

    # -------------------------------------------------
    def run(self):
        self.root.mainloop()
