
class OrderManager:
    
    def __init__(self, orderAccess, orderGroceries, paymentAccess):
        self.orderAccess = orderAccess
        self.orderGroceriesAccess = orderGroceries
        self.paymentAccess = paymentAccess
    
    def scheduleOrder(self, request):
        
        try:
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
            else:
                return {'msg':'issues with scheduling order'}
            
        except:
            return  {'msg':'failed request'}

    def checkOutOrder(self,user, request):

        try:
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
                    return {'msg':'issues with checking out order'}
            else:
                return {'msg':'no order found'}
        except:
            return {'msg':'failed request'}
        
    def getOrder(self, request):
        try:
            getParam = self.getRequestType(request)
            orderId = getParam('order_id')
            
            order = self.orderAccess.getOrderById(orderId)
            if order:
                empFname = order.employee
                empLname = order.employee
                if empFname:
                    empName = ( empFname.first_name+ " " +empLname.last_name )
                else:
                    empName = 'False'
    
                return {'order_details':self.__getOrderDetails(order,empName), 'groceries':self.__getOrderItemsDetails(order.id)}
            else:
                return {'msg':'no order found'}
        except:
            return {'msg':'failed request'}
        
    def getOrders(self):
        try:
            orders = self.orderAccess.getOrders()
            response = {}
            if orders:
                for order in orders:
                    empFname = order.employee
                    empLname = order.employee
                    if empFname:
                        empName = (empFname.first_name + " " + empLname.last_name)
                    else:
                        empName = 'False'
                    response[str(order.id)] = self.__getOrderDetails(order,empName)

                return {'msg':'success', 'items':response}
            else:
                return {'msg':'no order found'}
        except:
            return {'msg':'failed request'}

    def getTotalOnOrder(self):
        return self.orderGroceriesAccess.getTotalOnOrder(5)
    
    def recordPayment(self,user,request):
        try:
            getParam = self.getRequestType(request)
            orderId = int(getParam('order_id'))
            amountTendered = float(getParam('amount_tendered'))
            empId = user['emp_id']
            payment = self.paymentAccess.recordPayment(orderId, empId, amountTendered)
            if payment:
                return {'order_id': payment.order_id,'collected_by':payment.recorded_by, 'payment_date': str(payment.payment_date),\
                        'amount_tendered':str(payment.amount_tendered),'change':str(payment.change), 'customer':(payment.order.customer.first_name + " "+ \
                        payment.order.customer.last_name) }

            else:
                return {'msg':'payment not recorded'}
        except:
            return {'msg':' failed request'}

    def getSchedule(self):
        try:
            orders = self.orderAccess.getSchedule()
            response = {}
            if orders:
                for order in orders:
                    empFname = order.employee
                    empLname = order.employee
                    if empFname:
                        empName = (empFname.first_name + " " + empLname.last_name)
                    else:
                        empName = 'False'
                    response[str(order.id)] = self.__getOrderDetails(order,empName)
                return response
            else:
                return {'msg':'no order found'}
        except:
            return {'msg':'failed request'}

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
        print(type(orderItems))
        response = {}
        if orderItems:
            for grocery in orderItems:
                print(type(grocery))
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
        print(response)
        return response

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
