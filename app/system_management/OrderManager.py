
class OrderManager:
    
    def __init__(self, orderAccess, orderGroceries, paymentAccess):
        self.orderAccess = orderAccess
        self.orderGroceriesAccess = orderGroceries
        self.paymentAccess = paymentAccess
    
    def scheduleOrder(self, request, user):
        
        getParam = self.getRequestType(request)
        deliverydate = getParam('date')
        orderId = getParam('order_id')
        custId = user['cust_id']
        
        order = self.orderAccess.scheduleDelivery(orderId,deliverydate,int(custId))
        if order:
            emp = order.employee
            if emp:
                empName = (emp.first_name + " " + emp.last_name)
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

            return self.__getOrderDetails(order,empName)
        return False
        
    def getOrders(self, request, cust_id=None):
        getParam = self.getRequestType(request)

        if cust_id is None:
            cust_id = getParam('cust_id')
            
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


        orders = self.orderAccess.getOrders(cust_id, status, order_start_date, order_end_date,\
                                                    delivery_start_date, delivery_end_date, delivery_town,\
                                                    delivery_parish)

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
