class AccountManager:

    def __init__(self, customer_access):

        self.customer_access = customer_access

    def createAccount(self, request):

        """extract details from the request"""
        try:
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
            customer = self.customer_access.registerCustomer(firstName, lastName, int(telephone), email, gender, password, town, parish)
            if customer:
                return {"id": str(customer.id), 'firstName': customer.first_name, 'lastName': customer.last_name, \
                         'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                         'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return False
        except:
            return False

    def login(self, request):

        try:
            getParam = self.getRequestType(request)
            email = getParam('email')
            password = getParam('password')

            """sanitize email and password"""

            """get the customer's account"""
            customer = self.customer_access.login(email, password)
            if customer:
                return {"id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': str(customer.telephone), 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return False
        except:
            return False

    def getCustomer(self, customerId):

        try:
            customer = self.customer_access.getCustomerById(int(customerId))
            if customer:
                return {"id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': str(customer.telephone), 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return {'msg':'customer not found'}
        except:
            return {'msg':'failed request'}

    def updateAccount(self, request, session):

        try:
            getParam = self.getRequestType(request)
            customerId = session['cust_id']
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            customer = self.customer_access.updateAccount(int(customerId), attribute, value)
            if customer:
                return {"id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': str(customer.telephone), 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
            else:
                return {'msg':'customer account was not found'}
        except:
            return {'msg':'request failed'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get