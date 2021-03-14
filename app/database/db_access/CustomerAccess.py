from ... import db
from ..Models import Customer


class CustomerAccess:

    """retrieve a customer record from the database given their email and password"""
    def getCustomer(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        try:
            if customer.email == email and customer.password == password:
                return {"id": customer.id, 'firstName': customer.first_name, 'lastName':customer.last_name,\
                        'telephone':customer.telephone, 'email':customer.email, 'gender':customer.gender,\
                        'password':customer.password, 'town':customer.town, 'parish':customer.parish}
            else:
                return False
        except:
            return False

    """register a customer to the db"""
    def registerCustomer(self, firstName, lastName, telephone, email, gender, password, town, parish):

        customer = Customer(first_name=firstName, last_name=lastName, telephone=telephone, email=email, gender=gender, password=password, town=town, parish=parish)
        db.session.add(customer)
        db.session.commit()

        return {"id": customer.id, 'firstName': customer.first_name, 'lastName':customer.last_name,\
                        'telephone':customer.telephone, 'email':customer.email, 'gender':customer.gender,\
                        'password':customer.password, 'town':customer.town, 'parish':customer.parish}

    def getCustomerById(self, id):

        customer = Customer.query.filter_by(id=id).first()
        try:
            if customer.id == id:
                return {"id": customer.id, 'firstName': customer.first_name, 'lastName': customer.last_name, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return False
        except:
            return False