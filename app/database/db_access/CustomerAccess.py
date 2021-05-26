from sqlalchemy import exc
from ... import db, encrypter
from ..Models import Customer, Order, OrderGroceries, TotalAmountPurchased
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

class CustomerAccess:

    """retrieve a customer record from the database given their email and password"""
    def login(self,data):
        customer = Customer.query.filter_by(email=encrypter.encrypt(data['email'])).first()
        # print(customer)
        if customer is not None and check_password_hash(encrypter.decrypt(customer.password), data['password']):
            return customer
        else:
            return False

    """register a customer to the db"""
    def registerCustomer(self,data):
        customer = {}
        try:
            customer = Customer(
                data['first_name'],
                data['last_name'],
                data['telephone'],
                data['email'],
                data['gender'],
                data['password'],
                data['street'],
                data['town'],
                data['parish']
            )
            db.session.add(customer)
            db.session.commit()
            customer = self.getCustomerById(customer.id)
            return customer
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return False

    def confirmEmail(self,email):
        customer = Customer.query.filter_by(email=encrypter.encrypt(email)).first()
        if customer:
            customer.email_confirmed = True
            db.session.commit()
            return True
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
                customer.first_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'last_name':
                customer.last_name = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'telephone':
                customer.telephone = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'email':
                customer.email = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'gender':
                customer.gender = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'password':
                customer.password = generate_password_hash(value, method='pbkdf2:sha256:310000', salt_length=256)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'street':
                customer.street = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'town':
                customer.town = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
            if attribute == 'parish':
                customer.parish = encrypter.encrypt(value)
                db.session.commit()
                return self.getCustomerById(customerId)
        return False


    def getCart(self, cartId):

        customer = self.getCustomerById(cartId)
        if customer:
            return customer.cart_items
        else:
            return False

    def getTotalAmtPurchased(self, custId=None):
        """ Returns the total amount of each item a customer has purchased \
            over the lifetime of the account. If a list of IDs is provided \
            then it returns the total amount purchased for all those customers. \
            If an empty list is passed then it returns the total purchased for \
            all customers in the system """

        result = {}
        quantities = []
        if (type(custId) == int):
            quantities = TotalAmountPurchased.query.\
                    filter(TotalAmountPurchased.cust_id == custId).all()
            result[custId] = {}
            for q in quantities:
                result[custId][q.grocery_id] = q.total
        else:
            if (custId == None):
                quantities = TotalAmountPurchased.query.all()
            elif (type(custId) == list):
                quantities = TotalAmountPurchased.query.\
                        filter(TotalAmountPurchased.cust_id.in_(custId)).all()

            for q in quantities:
                try:
                    result[q.cust_id][q.grocery_id] = q.total
                except KeyError:
                    result[q.cust_id] = {q.grocery_id: q.total}
        return result
