import stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
class AccountManager:

    def __init__(self, customer_access, MLManager, orderAccess):
        self.MLManager = MLManager
        self.customer_access = customer_access
        self.orderAccess = orderAccess

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

    def setDeliveryLocation(self, user, request, order_id):
        getParam = self.getRequestType(request)
        parish = getParam('parish')
        town = getParam('town')
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
        return False


    def getRecommendedGroceries(self, custId):
        groceries = ''
        if self.customer_access.getCustomerById(custId):
            groceries = self.MLManager.getRecommendGroceries(custId)
            if groceries:
                return str(groceries)
            return False
        raise NameError

        
    def cancelOrder(self,user, order_id):
        orderId = int(order_id)
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
        return False


    def getOrder(self,user, orderId):
        # getParam = self.getRequestType(request)
        # orderId = getParam('order_id')
        cust_id = user['cust_id']
        
        order = self.orderAccess.getOrderByIdCustomer(orderId, cust_id)
        if order:
            empFname = order.employee
            empLname = order.employee
            if empFname:
                empName = ( empFname.first_name+ " " +empLname.last_name )
            else:
                empName = 'False'

            return self.__getOrderDetails(order,empName)
        return False
        
    def getMyOrders(self, user, request):
        getParam = self.getRequestType(request)
        status = getParam('status')

        order_start_date = getParam('order_start_date')
        if order_start_date is not None:
            order_start_date = order_start_date + " 00:00:00"
        
        order_end_date = getParam('order_end_date')
        if order_end_date is not None:
            order_end_date = order_end_date+" 23:59:59"

        delivery_start_date = getParam('delivery_start_date')
        if delivery_start_date is not None:
            delivery_start_date = delivery_start_date + " 00:00:00"
        
        delivery_end_date = getParam('delivery_end_date')
        if delivery_end_date is not None:
            delivery_end_date = delivery_end_date + " 23:59:59"

        delivery_town = getParam('delivery_town')
        delivery_parish = getParam('delivery_parish')
        
        cust_id = user['cust_id']

        orders = self.orderAccess.getOrders(cust_id, status, order_start_date, order_end_date,\
                                                    delivery_start_date, delivery_end_date, delivery_town,\
                                                    delivery_parish)
        response = []
        if orders:
            print('Orders',orders)
            for order in orders:
                emp = order.employee
                if emp:
                    empName = (emp.first_name + " " + emp.last_name)
                else:
                    empName = 'False'
                response.append(self.__getOrderDetails(order, empName))
        return response
    

    def make_payment(self, user, request):
        getParam = self.getRequestType(request)
        payment_method_id = getParam('payment_method_id')
        payment_intent_id = getParam('payment_intent_id')
        order_id = getParam('order_id')
        intent = None

        try:
            if  payment_method_id:
                order = self.getOrder(user,order_id)
                # Create the PaymentIntent
                if order:
                    intent = stripe.PaymentIntent.create(
                        payment_method = payment_method_id,
                        amount = order['total'],
                        currency = 'jmd',
                        confirmation_method = 'manual',
                        confirm = True,
                    )
                else:
                    return {'msg':'order does not exist','error':'notfound-0001'}, 200
            elif payment_intent_id:
                intent = stripe.PaymentIntent.confirm(payment_intent_id)
        except stripe.error.CardError as e:
            print(e)
            # Display error on client
            return {'error': e.user_message}, 200

        return self.__generate_response(intent)


    def __generate_response(self,intent):
        # Note that if your API version is before 2019-02-11, 'requires_action'
        # appears as 'requires_source_action'.
        if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
            # Tell the client to handle the action
            return {
                'requires_action': True,
                'payment_intent_client_secret': intent.client_secret,
            }, 200
        elif intent.status == 'succeeded':
            # The payment didn’t need any additional actions and completed!
            # Handle post-payment fulfillment
            return {'success': True}, 200
        else:
            # Invalid status
            return {'error': 'Invalid PaymentIntent status'}, 500



    def __getCustomerDetails(self, customer):

        return {"cust_id": str(customer.id), 'first_name': customer.first_name, 'last_name': customer.last_name, \
                        'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                        'town': customer.town, 'parish': customer.parish}
    

    def __getOrderDetails(self, order,empName):
        order_items = []
        order_total_before_delivery_cost = 0

        def getOrderItems(orderId):
            # print(type(orderId))
            orderItems = self.orderAccess.getItemsInOrder(orderId)
            nonlocal order_total_before_delivery_cost
            if orderItems:
                for grocery in orderItems:
                    # print(type(grocery))
                    cost_before_tax = grocery.quantity * grocery.groceries.cost_per_unit
                    GCT = self.orderAccess.getTax(grocery.grocery_id, 'GCT') * grocery.quantity
                    SCT = self.orderAccess.getTax(grocery.grocery_id, 'SCT') * grocery.quantity
                    item_total = float(cost_before_tax) + float(GCT) + float(SCT)
                    order_total_before_delivery_cost += item_total
                    total_weight = str(grocery.quantity * grocery.groceries.grams_per_unit) + " grams"
                    order_items.append({
                        'grocery_id': str(grocery.grocery_id),
                        'quantity': str(grocery.quantity),
                        'cost_before_tax': str(cost_before_tax),
                        'name': grocery.groceries.name,
                        'total_weight': total_weight,
                        'GCT': str(GCT), 
                        'SCT': str(SCT),
                        'total': str(item_total)
                    })

        result = {
            'order_id': str(order.id), 
            'order_date': str(order.orderdate),
            'status': str(order.status), 'customer_id': str(order.customer_id),
            'customer': (order.customer.first_name + " " + order.customer.last_name),
            'delivery_date': str(order.deliverydate),
            'delivery_town': str(order.deliverytown), 
            'delivery_parish': str(order.deliveryparish), 
            'checkout_by': empName
        }
        getOrderItems(order.id)
        result['order_items'] = order_items
        delivery_cost = order.parish.delivery_rate
        result['subtotal'] = order_total_before_delivery_cost
        result['delivery_cost'] = str(delivery_cost)
        result['total'] = order_total_before_delivery_cost + float(delivery_cost)
        return result

                
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get