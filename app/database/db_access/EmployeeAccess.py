from ... import db
from ..Models import Employee
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from app import encrypter
class EmployeeAccess:

    def registerEmployee(self, first_name, last_name, telephone, email, password, street, town, parish, role, salary):

        new_employee = Employee(self, first_name, last_name, telephone, email, password, street, town, parish, role, salary)
        db.session.add(new_employee)
        db.session.commit()

        return new_employee

    def login(self, email, password):
        employee = Employee.query.filter_by(email=encrypter.decrypt(email)).first()
        try:
            if employee is not None and check_password_hash(employee.password, password):
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
                employee.first_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'last_name':
                employee.last_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'email':
                employee.email = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'password':
                employee.password = generate_password_hash(value, method='pbkdf2:sha256:310000', salt_length=256)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'role':
                employee.role = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'salary':
                employee.cost_per_unit = float(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'street':
                employee.street = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'town':
                employee.town = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
            if attribute == 'parish':
                employee.parish = encrypter.encrypt(value)
                db.session.commit()
                return self.getEmployee(empId)
        return False
