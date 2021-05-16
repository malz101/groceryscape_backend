<<<<<<< HEAD
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
    def registerCustomer(self, firstName, lastName, telephone, email, gender, password,street, town, parish):
        customer = {}
        try:
            customer = Customer(first_name=firstName, last_name=lastName, telephone=telephone, email=email, gender=gender, password=password,street=street, town=town, parish=parish)
            db.session.add(customer)
            db.session.commit()
            customer = self.getCustomerById(customer.id)
            return customer
        except IntegrityError as e:
            db.session.rollback()
            return False
        
    def confirmEmail(self,email):
        customer = Customer.query.filter_by(email=email).first()
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
=======
from sqlalchemy import exc
from ... import db
from ..Models import Customer
from ..Models import Order
from ..Models import OrderGroceries
from sqlalchemy.exc import IntegrityError
#from sqlalchemy import in_

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
          
          
    def getTotalAmtPurchased(self, custId):
        """ Returns the total amount of each item a customer has
            purchased over the lifetime of the account. If a list
            of IDs is provided then it returns the total amount
            purchased for all those customers. If an empty list is
            passed then it returns the total purchased for all
            customers in the system """
        result = {}
        if (type(custId) == str):
            orders = Order.query.filter(Order.customer_id==custId).all()
            orderLst = [o.id for o in orders]
            groceries = OrderGroceries.query.filter(OrderGroceries.order_id.in_(orderLst)).all()
            for g in groceries:
                try:
                    temp = result[custId][g.grocery_id]
                except KeyError:
                    result[custId] = {}
                    result[custId][g.grocery_id] = 0
                result[custId][g.grocery_id] += g.quantity
        elif (type(custId) == list):
            if (len(custId) == 0):
                orders = Order.query.all()
            else:
                orders = Order.query.filter(Order.customer_id.in_(custId)).all()


            # Sum up the quantities of each item purchased for each customer
            orderCust = {o.id: o.customer_id for o in orders}
            groceries = OrderGroceries.query.\
                        filter(OrderGroceries.order_id.in_(orderCust.keys())).all()
            for g in groceries:
                try:
                    temp = result[orderCust[g.order_id]][g.grocery_id]
                except KeyError:
                    result[orderCust[g.order_id]] = {}
                    result[orderCust[g.order_id]][g.grocery_id] = 0
                result[orderCust[g.order_id]][g.grocery_id] += g.quantity
        return result
>>>>>>> merge_recommender-dev
