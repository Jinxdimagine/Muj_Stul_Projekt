from application.Application import Application
from Controller.EmployeeController import EmployeeController
from Controller.ReservationController import ReservationController
#from dao.dao import DAO

def main():
    # DAO – přístup k databázi
    #dao = DAO()

    # Controller-y pro jednotlivé entity
    employee_controller = EmployeeController()
    reservation_controller = ReservationController()

    # Hlavní aplikace – GUI + swap view
    app = Application(employee_controller, reservation_controller)
    app.run()

if __name__ == "__main__":
    main()
