from ... import db
from ..Models import Customer
from sqlalchemy.exc import IntegrityError

class CustomerAccess:

    """retrieve a customer record from the database given their email and password"""
    def login(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        if customer:
            if customer.email == email and customer.password == password:
                return customer
        else:
            return False

    """register a customer to the db"""
    def registerCustomer(self, firstName, lastName, telephone, email, gender, password, town, parish):
        customer = {}
        try:
            customer = Customer(first_name=firstName, last_name=lastName, telephone=telephone, email=email, gender=gender, password=password, town=town, parish=parish)
            db.session.add(customer)
            db.session.commit()
            customer = self.getCustomerById(customer.id)
            return customer
        except IntegrityError as e:
            db.session.rollback()
            return False

    def getCustomerById(self, id):
        customer = Customer.query.filter_by(id=id).first()
        try:
            if customer.id == int(id):
                print(customer)
                return customer
            else:
                return False
        except:
            return False

    def updateAccount(self, customerId, attribute, value):
        customer = self.getCustomerById(customerId)
        if customer:
            if attribute == 'first_name':
                customer.first_name = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'last_name':
                customer.last_name = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'telephone':
                customer.telephone = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'email':
                customer.email = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'gender':
                customer.gender = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'password':
                customer.password = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'town':
                customer.town = value
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'parish':
                customer.parish = value
                db.session.commit()
                return self.getCustomerById(customerId)

        return False

    def getCart(self, cartId):

        customer = self.getCustomerById(cartId)
        if customer:
            return customer.cart_items
        else:
            return False