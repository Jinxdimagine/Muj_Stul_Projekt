from application.Application import Application

from Controller.EmployeeController import EmployeeController
from Controller.ReservationController import ReservationController
from Controller.ShiftController import ShiftController
from Controller.PositionController import PositionController
from DAO.Database import Database
from DAO.EmployeeDAO import EmployeeDAO
from DAO.ShiftDAO import ShiftDAO
from DAO.EmployeeShiftDAO import EmployeeShiftDAO
from DAO.ReservationDAO import ReservationDAO
from DAO.CustomerDAO import CustomerDAO
from DAO.PositionDAO import PositionDAO
def main():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Martinvucz2007",
        "database": "mujstul"
    }

    # DAO – přístup k databázi
    employee_dao = EmployeeDAO(db_config)
    shift_dao = ShiftDAO(db_config)
    employee_shift_dao = EmployeeShiftDAO(db_config)
    customer_dao = CustomerDAO(db_config)
    reservation_dao = ReservationDAO(db_config)
    position_dao = PositionDAO(db_config)
    # CONTROLLERY
    employee_controller = EmployeeController(employee_dao)
    reservation_controller = ReservationController(reservation_dao)
    shift_controller = ShiftController(shift_dao, employee_shift_dao)
    position_controller=PositionController(position_dao)

    # APLIKACE
    app = Application(
        employee_controller=employee_controller,
        reservation_controller=reservation_controller,
        shift_controller=shift_controller,
        position_controller=position_controller
    )
    app.run()
if __name__ == "__main__":
    main()