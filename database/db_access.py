
from database.schemas import *

class DataAccess:

    def customerLogin(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        try:
            if customer.email == email and customer.password == password:
                return customer.id
            else:
                return False
        except:
            return False

    def employeeLogin(self, email, password):
        employee = Employee.query.filter_by(email=email).first()
        try:
            if employee.email == email and employee.password == password:
                return employee.id
            else:
                return False
        except:
            return False


    def signup(self, firstName, lastName, email, password, address, town, parish):

        newCustomer = Customer(firstName=firstName, lastName=lastName, email=email, password=password, address=address,
                               town=town, parish=parish)
        db.session.add(newCustomer)
        db.session.commit()

        customer = self.getCustomer(email)

        return customer.id



    def addEmployee(self, firstName, lastName, email, password, address):
        newEmployee = Employee(firstName=firstName, lastName=lastName, email=email, password=password, address=address,
                               role='admin')
        db.session.add(newEmployee)
        db.session.commit()

    def getCustomer(self, email):
        customer = Customer.query.filter_by(email=email).first()
        try:
            if customer.firstName:
                return customer
            else:
                return False
        except:

            return False


if __name__ == "__main__":
    
    # addEmployee('milton', 'francis', 'francis@gmail.com', '1234', 'kingston')
    db_con = DataAccess()
    print(db_con.getCustomer('francis@gmail.com', '1234'))

