from datetime import datetime, timedelta
from flask import render_template, url_for
from flask_weasyprint import HTML, render_pdf



class OrderManager:
    
    def __init__(self, orderAccess, paymentAccess, deliveryAccess):
        self.orderAccess = orderAccess
        self.paymentAccess = paymentAccess
        self.deliveryAccess = deliveryAccess


    def getOrderPreview(self,request,order_preview):
        '''returns a preview or the order details from item in cart'''
        getParam = self.getRequestType(request)
        parish = str(getParam('parish'))
        
        if order_preview:
            deliveryparish = self.deliveryAccess.getDeliveryParish(parish)
            order_preview['delivery_parish'] = str(deliveryparish.parish) 
            delivery_cost = deliveryparish.delivery_rate
            order_preview['delivery_cost'] = str(delivery_cost)
            order_preview['total'] = order_preview['sub_total']+order_preview['total_sct']+order_preview['total_gct']+ float(delivery_cost)
            return order_preview
        return False



    def create_order(self,user,cart_items):
        '''create an order from the cart items'''
        cust_id = user['cust_id']

        # 2) get all cart items
        if cart_items:
            order = self.orderAccess.addItemsToOrder(cart_items,int(cust_id))
            if order:
                return {
                    'order_id':str(order.id),
                    'order_date':order.orderdate,
                    'status':str(order.status),
                    'customer_id':str(order.customer_id), 
                    'customer':(order.customer.first_name + " "+ order.customer.last_name)
                }
        return False
    

    def cancelOrder(self,user, order_id):
        '''cancels an order'''
        orderId = int(order_id)
        custId = user['cust_id']

        cancelled_order = self.orderAccess.cancelOrder(int(custId), orderId)
        if cancelled_order:
            emp = cancelled_order.employee
            if emp:
                emp = (emp.first_name + " " + emp.last_name)
            else:
                empName = 'False'
            return self.__getOrderDetails(cancelled_order, empName)
        return False


    def scheduleOrder(self, request, user):
        '''schedules the date and time that customer wants order to be delivered'''
        getParam = self.getRequestType(request)
        deliverytimeslot = getParam('timeslot')
        deliverydate = getParam('date')
        orderId = getParam('order_id')
        custId = user['cust_id']
        
        if custId and deliverydate and deliverytimeslot and orderId:
            if datetime.strptime(deliverydate,'%Y-%m-%d').date() < (datetime.now().date()+timedelta(days=2)):
                if self.validSlot(deliverytimeslot, deliverydate):
                    order = self.orderAccess.scheduleDelivery(orderId,int(deliverytimeslot),deliverydate,int(custId))
                    if order:
                        emp = order.employee
                        if emp:
                            empName = (emp.first_name + " " + emp.last_name)
                        else:
                            empName = 'False'
                        return {'msg':'success','data':{'order':self.__getOrderDetails(order,empName)}}, 200
                return {'msg':'no more orders can be scheduled for this slot', 'error':'create-0001'}, 200
            return {'msg':'a slot cannot be booked more than two days in advance', 'error':'create-0001'}, 200
        return  {'msg':'either date, timeslot or order_id is empty', 'error':'create-0001'}, 200
    

    def getDeliveryTimeSlots(self):
        '''get all valid time slots within two days'''
        try:
            valid_slots=[]
            today = datetime.now().date()
            #for all dates within two days
            for i in range(3):
                ddate = datetime.now().date() + timedelta(days=i) #create date obj
                timeslots = self.deliveryAccess.getDeliveryTimeSlots() #get time slots company offers

                if timeslots:
                    for timeslot in timeslots:
                        #if timeslot is valid
                        if self.validSlot(timeslot.id, ddate):
                            temp = {
                                'date': str(ddate),
                                'timeslot': {
                                    'id':str(timeslot.id),
                                    'start_time':str(timeslot.start_time),
                                    'end_time':str(timeslot.end_time)
                                }
                            }
                            #if date is the current date
                            if today==ddate:
                                if timeslot.end_time > datetime.now().time():
                                    valid_slots.append(temp)
                            else:
                                valid_slots.append(temp)
                else:
                    return {'msg':'no timeslots were found', 'error':'notfound-0001'}, 404
            return {'msg':'success', 'data':{'slots':valid_slots}}, 200
        except Exception as e:
            print(e)
            return {'msg':'', 'error':'ise-0001'}, 500


    def validSlot(self,deliverytimeslot, deliverydate):
        '''determines whether a slot is a valid delivery time slot.
            It is a valid slot if the time of day is offered and it hasn't reach capacity'''

        max_deliveries_per_slot = self.deliveryAccess.getMaxDeliveriesPerTimeSlot()
        # print('max deliveries per slot',max_deliveries_per_slot)
        slot_count = self.orderAccess.getDeliveryTimeSlotCount(int(deliverytimeslot),deliverydate)
        # print('slot count', slot_count)
        return slot_count < max_deliveries_per_slot

    def setDeliveryLocation(self, user, request, order_id):
        getParam = self.getRequestType(request)
        street = getParam('street')
        parish = getParam('parish')
        town = getParam('town')
        cust_id = user['cust_id']
        

        order = self.orderAccess.setDeliveryLocation(int(cust_id),int(order_id),street, parish,town)
        if order:
            emp = order.employee
            if emp:
                empName = (emp.first_name + " " + emp.last_name)
            else:
                empName = 'False'
            return self.__getOrderDetails(order,empName)
        return False


    def checkOutOrder(self,user, request):
        '''used to attached employee that packaged the order to the order'''
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
    
    def getOrderCustomer(self,user, orderId):
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
    

    def getOrdersCustomer(self, user, request):
        '''return all the customers orders, filtered by criteria if provided'''
        getParam = self.getRequestType(request)
            
        status = getParam('status')

        order_start_date = getParam('order_start_date')
        if order_start_date is not None:
            order_start_date = order_start_date + " 00:00:00"
        
        order_end_date = getParam('order_end_date')
        if order_end_date is not None:
            order_end_date = order_end_date+" 23:59:59"

        delivery_start_date = getParam('delivery_start_date')
        delivery_end_date = getParam('delivery_end_date')
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

    def getOrder(self, orderId):
        '''returns an order with the specified order id'''
        # getParam = self.getRequestType(request)
        # orderId = getParam('order_id')
        
        order = self.orderAccess.getOrderById(orderId)
        if order:
            emp = order.employee
            if empFname:
                empName = ( emp.first_name+ " " +emp.last_name )
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
        delivery_end_date = getParam('delivery_end_date')
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
    

    def recordCashPayment(self,user,request, mail):
        '''employee records cash payment'''
        getParam = self.getRequestType(request)
        orderId = int(getParam('order_id'))
        amountTendered = float(getParam('amount_tendered'))
        empId = user['emp_id']
        order = self.getOrder(orderId)
        
        if order:
            payment = self.paymentAccess.recordCashPayment(order['total'], empId, amountTendered)
            if payment:
                self.orderAccess.updateStatus(orderId,'served')
                self.__sendEmail(order_id, mail)

                return {'order_id': payment.order_id,'collected_by':payment.recorded_by, 'payment_date': str(payment.payment_date),\
                        'amount_tendered':str(payment.amount_tendered),'change':str(payment.change), 'customer':(payment.order.customer.first_name + " "+ \
                        payment.order.customer.last_name) }
            return False
        return False


    def processCardPayment(self, user, request,mail):
        '''processes credit card payment'''
        getParam = self.getRequestType(request)
        payment_method_id = getParam('payment_method_id')
        payment_intent_id = getParam('payment_intent_id')
        order_id = getParam('order_id')
        intent = None
        try:
            if  payment_method_id:
                order = self.getOrderCustomer(user,order_id)
                
                if order:
                    print('Order Total',order['total'])
                    print('Order TotalA',int(round(order['total'],2)*100))
                    
                    # Create the PaymentIntent
                    intent = stripe.PaymentIntent.create(
                        payment_method = payment_method_id,
                        amount = int(round(order['total'],2)*100),
                        currency = 'jmd',
                        confirmation_method = 'manual',
                        confirm = True,
                        metadata={
                            'order_id': order['order_id'],
                        }
                    )
                else:
                    return {'msg':'order does not exist','error':'notfound-0001'}, 200
            elif payment_intent_id:
                intent = stripe.PaymentIntent.confirm(payment_intent_id)
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print(e.message)
            # Display error on client
            return {'msg': e.user_message, 'error':e.code}, 200
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            print(e.message)
            return {'msg':e.user_message, 'error':e.code}, 200
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e.message)
            return {'msg':e.user_message, 'error':e.code}, 200
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            print(e.message)
            return {'msg':e.user_message, 'error':e.code}, 200
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            print(e.message)
            return {'msg':e.user_message, 'error':e.code}, 200

        return self.__generate_response(intent,mail)


    def __generate_response(self,intent,mail):
        '''helper function for processCardPayment. It decides what action to do or response to return
        to the customer based on status of the payment intent'''

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
            order_id = int(intent.metadata['order_id'])
            self.paymentAccess.recordCardPayment(order_id, intent.amount/100, intent_id)
            self.orderAccess.updateStatus(order_id,'served')

            self.__sendEmail(order_id,mail)

            return {'msg':'success','data':{}}, 200
        else:
            # Invalid status
            return {'msg': 'Invalid PaymentIntent status', 'error':'ise-0001'}, 500


    def __sendEmail(self,order_id,mail):
        '''send invoice to customer for completed payment'''
        order = self.orderAccess.getOrderById(order_id)
        order_details = self.__getOrderDetails(order,'')
        customer = order.customer

        msg = Message(recipients=[str(customer.email)])
        msg.subject = "Payment Confirmation for Order "+str(order_id)
        if order:
            html = render_template('invoice.html', order=order_details, customer=customer)
            pdf = render_pdf(HTML(string=html))
            msg.attach(filename="invoice_"+order['order_id']+".pdf",disposition="attachment",content_type="application/pdf",data=pdf)
            msg.body=""" Dear {},
                        your order has been completed and payment received for {}, please find the attachment for the same""".format(customer.first_name,order['order_id'])
        else:
            msg.body=""" Dear {},
                        Your order has been completed and payment received for {}. An error has occured while generating pdf, please contact customer service""".format(customer.first_name,order['order_id'])
        mail.send(msg)


    def getSchedule(self):
        '''returns the delivery schedule'''
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

        def getOrderItems():
            # orderItems = self.orderAccess.getItemsInOrder(orderId)
            orderItems = order.groceries
            nonlocal order_total_before_delivery_cost
            if orderItems:
                for order_item in orderItems:
                    cost_before_tax = order_item.quantity * order_item.groceries.cost_per_unit
                    GCT = self.orderAccess.getTax(order_item.grocery_id, 'GCT') * order_item.quantity
                    SCT = self.orderAccess.getTax(order_item.grocery_id, 'SCT') * order_item.quantity
                    item_total = float(cost_before_tax) + float(GCT) + float(SCT)
                    order_total_before_delivery_cost += item_total
                    total_weight = str(order_item.quantity * order_item.groceries.grams_per_unit) + " grams"
                    order_items.append({
                        'grocery_id': str(order_item.grocery_id),
                        'sku': str(order_item.groceries.sku),
                        'quantity': str(order_item.quantity),
                        'cost_before_tax': str(cost_before_tax),
                        'name': order_item.groceries.name,
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
            'formatted_delivery_date': order.deliverydate.strftime("%B %d %Y") if order.deliverydate else str(None),
            'delivery_timeslot': str(order.timeslot.start_time)+"-"+str(order.timeslot.end_time) if order.timeslot else str(None),
            'delivery_date': str(order.deliverydate),
            'delivery_town': str(order.deliverytown), 
            'delivery_parish': str(order.deliveryparish), 
            'checkout_by': empName
        }
        getOrderItems()
        result['order_items'] = order_items
        result['subtotal'] = order_total_before_delivery_cost
        delivery_cost = order.parish.delivery_rate
        result['delivery_cost'] = str(delivery_cost)
        result['total'] = order_total_before_delivery_cost + float(delivery_cost)
        return result


    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
