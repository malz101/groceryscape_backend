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

    def deleteEmployee(self, empId):
        employee = self.getEmployee(empId)
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return self.getEmployees()
        else:
            return False

    def getEmployees(self):
        employees = Employee.query.filter_by().all()
        try:
            if employees[0].id:
                return employees
            else:
                return False
        except:
            return False
        
    def getEmployee(self, empId):
        employee = Employee.query.filter_by(id=empId).first()
        try:
            if employee.id == empId:
                return employee
            else:
                return False
        except:
            return False

    def updateEmployee(self, empId, attribute, value):

        employee = self.getEmployee(empId)
        if employee:
            if attribute == 'first_name':
                employee.first_name = value
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'last_name':
                employee.last_name = value
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'email':
                employee.email = value
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'password':
                employee.password = value
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'role':
                employee.role = value
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'salary':
                employee.cost_per_unit = float(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'address':
                employee.address = value
                db.session.commit()
                return self.getEmployee(empId)
        return False
