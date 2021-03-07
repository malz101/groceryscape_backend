from database.Models import db
from database.Models import Employee

class EmployeeAccess:

    def registerEmployee(self, firstName, lastName, email, password, address, role, salary, branch_work):

        new_employee = Employee(firstName=firstName, lastName=lastName, email=email, password=password, address=address, role=role, salary=salary, branch_work=int(branch_work))
        db.session.add(new_employee)
        db.session.commit()

        return new_employee

    def getEmployee(self, email, password):
        employee = Employee.query.filter_by(email=email).first()
        try:
            if employee.email == email and employee.password == password:
                return employee
            else:
                return False
        except:
            return False
