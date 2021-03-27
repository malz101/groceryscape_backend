
class OrderManager:
    
    def __init__(self, orderAccess):
        self.orderAccess = orderAccess
    
    def scheduleOrder(self, request):
        
        try:
            getParam = self.getRequestType(request)
            deliveryDate = getParam('date')
            deliveryTown = getParam('town')
            deliveryParish = getParam('parish')
            orderId = getParam('order_id')
            
            order = self.orderAccess.scheduleDelivery(orderId,deliveryDate,deliveryTown,deliveryParish)
            if order:
                return {'order_id':str(order.id), 'order_date':str(order.orderDate), 'status':str(order.status), \
                        'customer_id':str(order.customer_id), 'customer':(order.customer.first_name + " "+ \
                        order.customer.last_name), 'delivery_date':str(order.deliveryDate), 'delivery_town':str(order.deliveryTown),\
                        'delivery_parish':str(order.deliveryParish)}
            else:
                return {'msg':'issues with scheduling order'}
            
        except:
            return  {'msg':'failed request'}

    def checkOutOrder(self,session, request):

        try:
            getParam = self.getRequestType(request)
            orderId = getParam('order_id')
            if 'admin_id' in session:
                empId = session['admin_id']
            if 'staff_id' in session:
                empId = session['staff_id']
    
            if empId:
                order = self.orderAccess.checkoutOrder(orderId, empId)
                if order:
                    return {'order_id':str(order.id), 'order_date':str(order.orderDate), 'status':str(order.status), \
                        'customer_id':str(order.customer_id), 'customer':(order.customer.first_name + " "+ \
                        order.customer.last_name), 'delivery_date':str(rder.deliveryDate), 'delivery_town':str(order.deliveryTown),\
                        'delivery_parish':str(order.deliveryParish),'checkout_by':(order.employee.first_name + " "+ \
                        order.employee.last_name)}
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
    
                return {'order_id': str(order.id), 'order_date': str(order.orderDate), 'status': str(order.status), \
                        'customer_id': str(order.customer_id), 'customer': (order.customer.first_name + " " + \
                                                                            order.customer.last_name),
                        'delivery_date': str(order.deliveryDate), 'delivery_town': str(order.deliveryTown), \
                        'delivery_parish': str(order.deliveryParish), 'checkout_by': empName}
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
                    response[str(order.id)] = {'order_id': str(order.id), 'order_date': str(order.orderDate),\
                                               'status': str(order.status),'customer_id': str(order.customer_id),\
                                               'customer': (order.customer.first_name + " " + \
                                                order.customer.last_name),'delivery_date': str(order.deliveryDate),\
                                               'delivery_town': str(order.deliveryTown), 'delivery_parish': \
                                                str(order.deliveryParish), 'checkout_by': empName}
                return response
            else:
                return {'msg':'no order found'}
        except:
            return {'msg':'failed request'}
        
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
