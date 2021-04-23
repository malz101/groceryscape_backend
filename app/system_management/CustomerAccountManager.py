
class AccountManager:

    def __init__(self, customer_access, MLManager, orderAccess):
        self.MLManager = MLManager
        self.customer_access = customer_access
        self.orderAccess = orderAccess

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
            customer = self.customer_access.registerCustomer(firstName, lastName, telephone, email, gender, password, town, parish)
            if customer:
                return self.__getCustomerDetails(customer)
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
                return self.__getCustomerDetails(customer)
            else:
                return False
        except:
            return False

    def getCustomer(self, customerId):

        try:
            customer = self.customer_access.getCustomerById(int(customerId))
            if customer:
                return self.__getCustomerDetails(customer)
            else:
                return {'msg':'customer not found'}
        except:
            return {'msg':'failed request'}

    def updateAccount(self, request, user):

        try:
            getParam = self.getRequestType(request)
            customerId = user['cust_id']
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            customer = self.customer_access.updateAccount(int(customerId), attribute, value)
            if customer:
                return self.__getCustomerDetails(customer)
            else:
                return {'msg':'customer account was not found'}
        except:
            return {'msg':'request failed'}

    def setDeliveryLocation(self, user, request):

        try:
            getParam = self.getRequestType(request)
            parish = getParam('parish')
            town = getParam('town')
            order_id = getParam('order_id')
            cust_id = user['cust_id']

            order = self.orderAccess.setDeliveryLocation(int(cust_id),int(order_id),parish,town)
            if order:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                return self.__getOrderDetails(order,empName)
            else:
                return {'msg':'order was not updated'}
        except:
            return {'msg': 'request failed'}

    def getRecommendedGroceries(self, session):
        
        try:
            custId = session['cust_id']
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
        
    def cancelOrder(self,user, request):
        try:
            getParam = self.getRequestType(request)
            orderId = int(getParam('order_id'))
            custId = user['cust_id']
            
            cancelled_order = self.orderAccess.cancelOrder(int(custId), orderId)
            if cancelled_order:
                empFname = cancelled_order.employee
                empLname = cancelled_order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                return self.__getOrderDetails(cancelled_order, empName)
            else:
                return {'msg':'order not canceled'}
        except:
            return {'msg':'failed request'}
        
    def getMyOrders(self, user):
        try:
            cust_id = user['cust_id']
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
                    response[str(order.id)] = self.__getOrderDetails(order, empName),self.__getOrderItemsDetails(order.id)

                return response
            else:
                return {'msg': 'no order found'}
        except:
            return {'msg':'failed request'}
    
    def getMyPendingOrders(self, user):
        try:
            cust_id = user['cust_id']
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
                    response[str(order.id)] = self.__getOrderDetails(order, empName), self.__getOrderItemsDetails(order.id)
                return response
            else:
                return {'msg': 'no order found'}
        except:
            return {'msg': 'failed request'}

    def __getCustomerDetails(self, customer):

        return {"cust_id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'password': customer.password, 'town': customer.town, 'parish': customer.parish}

    def __getOrderDetails(self, order,empName):
        return {'order_id': str(order.id), 'order_date': str(order.orderDate), \
                                               'status': str(order.status), 'customer_id': str(order.customer_id), \
                                               'customer': (order.customer.first_name + " " + \
                                                            order.customer.last_name),\
                                               'delivery_date': str(order.deliveryDate), \
                                               'delivery_town': str(order.deliveryTown), 'delivery_parish': \
                                                   str(order.deliveryParish), 'checkout_by': empName,\
                                                'total':self.orderAccess.getTotalOnOrder(order.id)}
    def __getOrderItemsDetails(self,orderId):
        orderItems = self.orderAccess.getItemsInOrder(orderId)
        response = {}
        if orderItems:
            for grocery in orderItems:
                cost_before_tax = grocery.quantity * grocery.groceries.cost_per_unit
                GCT = self.orderAccess.getTax(grocery.grocery_id, 'GCT') * grocery.quantity
                SCT = self.orderAccess.getTax(grocery.grocery_id, 'SCT') * grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity * grocery.groceries.grams_per_unit) + " grams"
                response[str(grocery.grocery_id)] = {'grocery_id': str(grocery.grocery_id), \
                                                  'quantity': str(grocery.quantity), \
                                                  'cost_before_tax': str(cost_before_tax), \
                                                  'name': grocery.groceries.name, \
                                                  'total_weight': total_weight, 'GCT': str(GCT), 'SCT': str(SCT), \
                                                  'total': str(total)}
            return response
        else:
            return {orderId:'no groceries on order'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get