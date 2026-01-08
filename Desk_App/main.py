from application.Application import Application

from Controller.EmployeeController import EmployeeController
from Controller.ReservationController import ReservationController
from Controller.ShiftController import ShiftController

from DAO.EmployeeDAO import EmployeeDAO
from DAO.ShiftDAO import ShiftDAO
from DAO.EmployeeShiftDAO import EmployeeShiftDAO


def main():
    # ---------- DAO ----------
    employee_dao = EmployeeDAO()
    shift_dao = ShiftDAO()
    employee_shift_dao = EmployeeShiftDAO()

    # ---------- CONTROLLERY ----------
    employee_controller = EmployeeController(employee_dao)
    reservation_controller = ReservationController()
    shift_controller = ShiftController(
        shift_dao=shift_dao,
        employee_shift_dao=employee_shift_dao
    )

    # ---------- APLIKACE ----------
    app = Application(
        employee_controller=employee_controller,
        reservation_controller=reservation_controller,
        shift_controller=shift_controller
    )
    app.run()


if __name__ == "__main__":
    main()
