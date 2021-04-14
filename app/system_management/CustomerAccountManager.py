class AccountManager:

    def __init__(self, customer_access, MLManager, orderAccess):
        self.MLManager = MLManager
        self.customer_access = customer_access
        self.orderAccess = orderAccess

    def createAccount(self, request):

        """extract details from the request"""
        # try:
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
            return {"id": str(customer.id), 'firstName': customer.first_name, 'lastName': customer.last_name, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}
        else:
            return False
        # except:
        #     return False

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
    
    def getRecommendedGroceries(self, session):
        
        try:
            custId = session['cust_id']
            print(custId)
            if self.customer_access.getCustomerById(custId):
                groceries = self.MLManager.getRecommendGroceries(custId)
                if groceries:
                    return str(groceries)
                else:
                    return {'msg':'no groceries recommended'}
            else:
                return {'msg':'customer not found'}
        except:
            return {'msg':'failed request'}
        
    def cancelOrder(self,request):
        try:
            getParam = self.getRequestType(request)
            orderId = int(getParam('order_id'))
            
            cancelled = self.orderAccess.cancelOrder(orderId)
            if cancelled:
                return {'msg':'Order has been cancelled'}
            else:
                return {'msg':'failed request'}
        except:
            return {'msg':'failed request'}
        
    def getMyOrders(self, session):
        # try:
            cust_id = session['cust_id']
            orders = self.orderAccess.getCustomerOrders(cust_id)
            response = {}
            if orders:
                for order in orders:
                    empFname = order.employee
                    empLname = order.employee
                    if empFname:
                        empName = (empFname.first_name + " " + empLname.last_name)
                    else:
                        empName = 'False'
                    response[str(order.id)] = {'order_id': str(order.id), 'order_date': str(order.orderdate), \
                                               'status': str(order.status), 'customer_id': str(order.customer_id), \
                                               'customer': (order.customer.first_name + " " + \
                                                            order.customer.last_name),
                                               'delivery_date': str(order.deliverydate), \
                                               'delivery_town': str(order.deliverytown), 'delivery_parish': \
                                                   str(order.deliveryparish), 'checkout_by': empName}
                return response
            else:
                return {'msg': 'no order found'}
        # except:
        #     return {'msg':'failed request'}
    
    def getMyPendingOrders(self, session):
        # try:
        cust_id = session['cust_id']
        response = {}
        orders = self.orderAccess.getCustomerPendingOrder(cust_id)
        if orders:
            for order in orders:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                response[str(order.id)] = {'order_id': str(order.id), 'order_date': str(order.orderdate), \
                                            'status': str(order.status), 'customer_id': str(order.customer_id), \
                                            'customer': (order.customer.first_name + " " + \
                                                        order.customer.last_name),
                                            'delivery_date': str(order.deliverydate), \
                                            'delivery_town': str(order.deliverytown), 'delivery_parish': \
                                                str(order.deliveryparish), 'checkout_by': empName}
            return response
        else:
            return {'msg': 'no order found'}
        # except:
        #     return {'msg': 'failed request'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get