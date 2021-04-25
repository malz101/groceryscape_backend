
class OrderManager:
    
    def __init__(self, orderAccess, orderGroceries, paymentAccess):
        self.orderAccess = orderAccess
        self.orderGroceriesAccess = orderGroceries
        self.paymentAccess = paymentAccess
    
    def scheduleOrder(self, request):
        
        getParam = self.getRequestType(request)
        deliverydate = getParam('date')
        orderId = getParam('order_id')
        
        order = self.orderAccess.scheduleDelivery(orderId,deliverydate)
        if order:
            empFname = order.employee
            empLname = order.employee
            if empFname:
                empName = (empFname.first_name + " " + empLname.last_name)
            else:
                empName = 'False'
            return self.__getOrderDetails(order,empName)
        return False 
            

    def checkOutOrder(self,user, request):

        getParam = self.getRequestType(request)
        orderId = getParam('order_id')

        empId = user['emp_id']

        if orderId:
            order = self.orderAccess.checkoutOrder(orderId, empId)
            if order:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                return self.__getOrderDetails(order,empName)
            else:
                return order
        return False
        
    def getOrder(self, orderId):
        # getParam = self.getRequestType(request)
        # orderId = getParam('order_id')
        
        order = self.orderAccess.getOrderById(orderId)
        if order:
            empFname = order.employee
            empLname = order.employee
            if empFname:
                empName = ( empFname.first_name+ " " +empLname.last_name )
            else:
                empName = 'False'

            return {'summary':self.__getOrderDetails(order,empName), 'groceries':self.__getOrderItemsDetails(order.id)}
        return False
        
    def getOrders(self):
        orders = self.orderAccess.getOrders()
        response = []
        if orders:
            for order in orders:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                response.append(self.__getOrderDetails(order,empName))

        return response

    def getTotalOnOrder(self, order_id):
        return self.orderGroceriesAccess.getTotalOnOrder(order_id)
    
    def recordPayment(self,user,request):
        getParam = self.getRequestType(request)
        orderId = int(getParam('order_id'))
        amountTendered = float(getParam('amount_tendered'))
        empId = user['emp_id']
        payment = self.paymentAccess.recordPayment(orderId, empId, amountTendered)
        if payment:
            return {'order_id': payment.order_id,'collected_by':payment.recorded_by, 'payment_date': str(payment.payment_date),\
                    'amount_tendered':str(payment.amount_tendered),'change':str(payment.change), 'customer':(payment.order.customer.first_name + " "+ \
                    payment.order.customer.last_name) }

        return False

    def getSchedule(self):
        orders = self.orderAccess.getSchedule()
        response = []
        if orders:
            for order in orders:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = (empFname.first_name + " " + empLname.last_name)
                else:
                    empName = 'False'
                response.append(self.__getOrderDetails(order,empName))
        return response


    def __getOrderDetails(self, order,empName):
        return {'order_id': str(order.id), 'order_date': str(order.orderdate), \
                                               'status': str(order.status), 'customer_id': str(order.customer_id), \
                                               'customer': (order.customer.first_name + " " + \
                                                            order.customer.last_name),\
                                               'delivery_date': str(order.deliverydate), \
                                               'delivery_town': str(order.deliveryTown), 'delivery_parish': \
                                                   str(order.deliveryParish), 'checkout_by': empName,\
                                                'total':self.orderAccess.getTotalOnOrder(order.id),\
                                                'delivery_cost':self.orderAccess.getDeliveryCost(int(order.id))}

    def __getOrderItemsDetails(self,orderId):
        orderItems = self.orderAccess.getItemsInOrder(orderId)
        # print(type(orderItems))
        response = []
        if orderItems:
            for grocery in orderItems:
                # print(type(grocery))
                cost_before_tax = grocery.quantity * grocery.groceries.cost_per_unit
                GCT = self.orderAccess.getTax(grocery.grocery_id, 'GCT') * grocery.quantity
                SCT = self.orderAccess.getTax(grocery.grocery_id, 'SCT') * grocery.quantity
                total = float(cost_before_tax) + float(GCT) + float(SCT)
                total_weight = str(grocery.quantity * grocery.groceries.grams_per_unit) + " grams"
                response.append({'grocery_id': str(grocery.grocery_id), \
                                                  'quantity': str(grocery.quantity), \
                                                  'cost_before_tax': str(cost_before_tax), \
                                                  'name': grocery.groceries.name, \
                                                  'total_weight': total_weight, 'GCT': str(GCT), 'SCT': str(SCT), \
                                                  'total': str(total)})
        # print(response)
        return response

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
