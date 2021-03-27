from ... import db
from ..Models import Employee

class EmployeeAccess:

    def registerEmployee(self, firstName, lastName, email, password, address, role, salary):

        new_employee = Employee(first_name=firstName, last_name=lastName, email=email, password=password, address=address,\
                                role=role, salary=salary)
        db.session.add(new_employee)
        db.session.commit()

        return new_employee

    def login(self, email, password):
        employee = Employee.query.filter_by(email=email).first()
        try:
            if employee.email == email and employee.password == password:
                return employee
            else:
                return False
        except:
            return False
        
    def getEmployee(self, empId):
        employee = Employee.query.filter_by(id=empId).first()
        try:
            if employee.id == id:
                return employee
            else:
                return False
        except:
            return False
