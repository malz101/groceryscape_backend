import stripe
import os
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
class AccountManager:

    def __init__(self, customer_access, MLManager):
        self.MLManager = MLManager
        self.customer_access = customer_access

    def createAccount(self, request):

        """extract details from the request"""
        getParam = self.getRequestType(request)
        firstName = getParam('first_name')
        lastName = getParam('last_name')
        telephone = getParam('telephone')
        email = getParam('email')
        gender = getParam('gender')
        password = getParam('password')
        town = getParam('town')
        parish = getParam('parish')

        """sanitize and verify details"""

        """create account with sanitized data"""
        customer = self.customer_access.registerCustomer(firstName, lastName, telephone, email, gender, password, town, parish)
        if customer:
            return True
        return False

    def login(self, request):

        getParam = self.getRequestType(request)
        email = getParam('email')
        password = getParam('password')
        
        """sanitize email and password"""

        """get the customer's account"""
        customer = self.customer_access.login(email, password)
        if customer:
            return {
                "cust_id": str(customer.id),
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'telephone': customer.telephone,
                'town': customer.town,
                'parish': customer.parish
            }
        return False

    def getCustomer(self, customerId):

        customer = self.customer_access.getCustomerById(int(customerId))
        if customer:
            return self.__getCustomerDetails(customer)
        return False


    def updateAccount(self, request, user):

        getParam = self.getRequestType(request)
        customerId = user['cust_id']
        attribute = getParam('attribute')
        value = getParam('value')

        '''validate and sanitize data'''
        
        '''perform update'''
        customer = self.customer_access.updateAccount(int(customerId), attribute, value)
        if customer:
            return self.__getCustomerDetails(customer)
        return False


    def getRecommendedGroceries(self, custId):
        groceries = ''
        if self.customer_access.getCustomerById(custId):
            groceries = self.MLManager.getRecommendGroceries(custId)
            if groceries:
                return str(groceries)
            return False
        raise NameError


    def __getCustomerDetails(self, customer):

        return {"cust_id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'town': customer.town, 'parish': customer.parish}

                
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get