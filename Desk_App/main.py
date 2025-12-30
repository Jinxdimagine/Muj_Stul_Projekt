from application.Application import Application

#from controller.employee_controller import EmployeeController
#from controller.reservation_controller import ReservationController
#from dao.dao import DAO

def main():
    # DAO – přístup k databázi
    #dao = DAO()

    # Controller-y pro jednotlivé entity
    #employee_controller = EmployeeController(dao)
    #reservation_controller = ReservationController(dao)

    # Hlavní aplikace – GUI + swap view
    #app = Application(employee_controller, reservation_controller)
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
