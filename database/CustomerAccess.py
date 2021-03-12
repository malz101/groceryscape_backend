
from database.Models import db
from database.Models import Customer


class CustomerAccess:

    """retrieve a customer record from the database given their email and password"""
    def getCustomer(self, email, password):
        customer = Customer.query.filter_by(email=email).first()
        try:
            if customer.email == email and customer.password == password:
                return {"id": customer.id, 'firstName': customer.firstName, 'lastName':customer.lastName,\
                        'telephone':customer.telephone, 'email':customer.email, 'gender':customer.gender,\
                        'password':customer.password, 'town':customer.town, 'parish':customer.parish}
            else:
                return False
        except:
            return False

    """register a customer to the db"""
    def registerCustomer(self, firstName, lastName, telephone, email, gender, password, town, parish):

        customer = Customer(firstName=firstName, lastName=lastName, telephone=telephone, email=email, gender=gender, password=password, town=town, parish=parish)
        db.session.add(customer)
        db.session.commit()

        return {"id": customer.id, 'firstName': customer.firstName, 'lastName':customer.lastName,\
                        'telephone':customer.telephone, 'email':customer.email, 'gender':customer.gender,\
                        'password':customer.password, 'town':customer.town, 'parish':customer.parish}

    def getCustomer(self, id):

        customer = Customer.query.filter_by(id=id).first()
        try:
            if customer.id == id:
                return {"id": customer.id, 'firstName': customer.firstName, 'lastName': customer.lastName, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return False
        except:
            return False