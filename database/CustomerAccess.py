
from database.Models import db
from database.Models import Customer


class CustomerManager:

    """retrieve a customer record from the database given their email and password"""
    def getCustomer(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        try:
            if customer.email == email and customer.password == password:
                return customer
            else:
                return False
        except:
            return False

    """register a customer to the db"""
    def registerCustomer(self, firstName, lastName, telephone, email, gender, password, town, parish):

        new_customer = Customer(firstName=firstName, lastName=lastName, telephone=telephone, email=email, gender=gender, password=password, town=town, parish=parish)
        db.session.add(new_customer)
        db.session.commit()

        return new_customer