from application.Application import Application
from Controller.EmployeeController import EmployeeController
from Controller.ShiftController import ShiftController
from Controller.PositionController import PositionController
from Controller.Shift_typeController import Shift_typeController
from DAO.EmployeeDAO import EmployeeDAO
from DAO.ShiftDAO import ShiftDAO
from DAO.EmployeeShiftDAO import EmployeeShiftDAO
from DAO.Shift_typeDAO import ShiftTypeDAO
from DAO.PositionDAO import PositionDAO
from config import DB_CONFIG

def main():

    db_config = DB_CONFIG
    # DAO – database access
    employee_dao = EmployeeDAO(db_config)
    shift_dao = ShiftDAO(db_config)
    employee_shift_dao = EmployeeShiftDAO(db_config)
    position_dao = PositionDAO(db_config)
    shift_type_dao = ShiftTypeDAO(db_config)

    # Controllers
    employee_controller = EmployeeController(employee_dao)
    shift_controller = ShiftController(shift_dao, employee_shift_dao)
    position_controller = PositionController(position_dao)
    shift_type_controller = Shift_typeController(shift_type_dao)

    print(employee_dao.get_view_all())

    # Application
    app = Application(
        employee_controller=employee_controller,
        shift_controller=shift_controller,
        position_controller=position_controller,
        shift_type_controller=shift_type_controller,
    )
    app.run()

if __name__ == "__main__":
    main()
