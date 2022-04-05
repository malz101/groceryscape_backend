from datetime import datetime, timedelta
from flask import render_template, url_for
from flask_weasyprint import HTML, render_pdf
import os
import stripe
from flask_mail import Message
from app import db,encryp
from app.database.models import Order, OrderLine, CartItem

stripe.api_key = app.config['STRIPE_SECRET_KEY']

def __init__(self, orderAccess, paymentAccess, deliveryAccess, cartAccess=None):
    self.orderAccess = orderAccess
    self.paymentAccess = paymentAccess
    self.deliveryAccess = deliveryAccess
    self.cartAccess = cartAccess

def create_order(new_order_data:dict):
    '''create an order from the cart items'''
    order = Order(**new_order_data)
    db.session.add(order)
    db.session.commit()
    return order

    cart_items = self.cartAccess.getAllCartItems(int(order_data['customer_id']))
    if cart_items:
        order = self.orderAcess.createOrder(order_data)
        if order:
            # 2) get all cart items
            self.orderAccess.addItemsToOrder(cart_items,order.id)
            
            return {
                'order_id':str(order.id),
                'order_date':order.orderdate,
                'status':str(encrypter.decrypt(order.status)),
                'customer_id':str(order.customer_id), 
                'customer':(encrypter.decrypt(order.customer.first_name) + " "+ encrypter.decrypt(order.customer.last_name))
            }
    return False


def updateStatus(self, request):
    '''Updates the status of an order. Status of an order can be Pending, Checkout, Delivered, Canceled'''
    getParam = self.getRequestType(request)
    order_id = getParam('order_id')
    status = getParam('status')

    if order_id and status:
        order = self.orderAccess.updateStatus(int(order_id), status)
        if order:
            return self.__getOrderDetails(order)
        return False
    raise ValueError

def getOrderPreview(self,request,order_preview):
    '''returns a preview or the order details from item in cart'''
    getParam = self.getRequestType(request)
    parish = str(getParam('parish'))
    
    if order_preview:
        delivery_parish = self.deliveryAccess.getDeliveryParish(parish)
        order_preview['delivery_parish'] = str(encrypter.decryt(delivery_parish.parish)) 
        delivery_cost = delivery_parish.delivery_rate
        order_preview['delivery_cost'] = str(delivery_cost)
        order_preview['total'] = order_preview['sub_total']+order_preview['total_sct']+order_preview['total_gct']+ float(delivery_cost)
        return order_preview
    return False



def cancelOrder(self,user, order_id):
    '''cancels an order'''
    orderId = int(order_id)
    custId = user['cust_id']

    cancelled_order = self.orderAccess.cancelOrder(int(custId), orderId)
    if cancelled_order:
        return self.__getOrderDetails(cancelled_order)
    return False


def scheduleOrder(self, request, user):
    '''schedules the date and time that customer wants order to be delivered'''
    getParam = self.getRequestType(request)
    delivery_timeslot = getParam('timeslot')
    delivery_date = getParam('date')
    order_id = getParam('order_id')
    custId = user['cust_id']
    
    state = True #tracks status order to knw if to delete
    if custId and delivery_date and delivery_timeslot and order_id:
        if datetime.strptime(delivery_date,'%Y-%m-%d').date() < (datetime.now().date()+timedelta(days=2)):
            if self.validSlot(delivery_timeslot, delivery_date):
                order = self.orderAccess.scheduleDelivery(order_id,int(delivery_timeslot),delivery_date,int(custId))
                if order:
                    return {'msg':'success','data':{'order':self.__getOrderDetails(order)}}, 200

                self.orderAccess.deleteOrderByID(int(order_id))
            return {'msg':'no more orders can be scheduled for this slot', 'error':'create-0001'}, 200
            self.orderAccess.deleteOrderByID(int(order_id))
        return {'msg':'a slot cannot be booked more than two days in advance', 'error':'create-0001'}, 200
        self.orderAccess.deleteOrderByID(int(order_id))
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


def validSlot(self,delivery_timeslot, delivery_date):
    '''determines whether a slot is a valid delivery time slot.
        It is a valid slot if the time of day is offered and it hasn't reach capacity'''

    max_deliveries_per_slot = self.deliveryAccess.getMaxDeliveriesPerTimeSlot()
    # print('max deliveries per slot',max_deliveries_per_slot)
    slot_count = self.orderAccess.getDeliveryTimeSlotCount(int(delivery_timeslot),delivery_date)
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
        return self.__getOrderDetails(order)
    try:
        self.orderAccess.deleteOrderByID(int(order_id))
    except Exception as e:
        print(e)
        return False
    return False


def checkOutOrder(self,user, request):
    '''used to attached employee that packaged the order to the order'''
    getParam = self.getRequestType(request)
    orderId = getParam('order_id')

    empId = user['emp_id']

    if orderId:
        order = self.orderAccess.checkoutOrder(orderId, empId)
        if order:
            return self.__getOrderDetails(order)
        else:
            return order
    return False


def getOrderCustomer(self,user, orderId):
    # getParam = self.getRequestType(request)
    # orderId = getParam('order_id')
    cust_id = user['cust_id']
    
    order = self.orderAccess.getOrderByIdCustomer(orderId, cust_id)
    if order:
        return self.__getOrderDetails(order)
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
    payment_type = getParam('payment_type')

    cust_id = user['cust_id']

    orders = self.orderAccess.getOrders(cust_id, status, order_start_date, order_end_date,\
                                                delivery_start_date, delivery_end_date, delivery_town,\
                                                delivery_parish, payment_type)
    response = []
    for order in orders:
        response.append(self.__getOrderDetails(order))
    return response

def getOrder(self, orderId):
    '''returns an order with the specified order id'''
    # getParam = self.getRequestType(request)
    # orderId = getParam('order_id')
    
    order = self.orderAccess.getOrderById(orderId)
    if order:
        return self.__getOrderDetails(order)
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
    delivery_street = getParam('delivery_street')
    delivery_town = getParam('delivery_town')
    delivery_parish = getParam('delivery_parish')
    payment_type = getParam('payment_type')


    orders = self.orderAccess.getOrders(cust_id, status, order_start_date, order_end_date,\
                                                delivery_start_date, delivery_end_date, delivery_town,\
                                                delivery_parish, payment_type)

    response = []
    for order in orders:
        response.append(self.__getOrderDetails(order))

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
            self.orderAccess.updateStatus(orderId,'delivered')
            self.__sendEmail(order_id, mail)
            return {
                'order_id': payment.order_id,
                'collected_by':payment.recorded_by, 
                'payment_date': str(payment.payment_date),
                'amount_tendered':str(payment.amount_tendered),
                'change':str(payment.change), 
                'customer':(encrypter.decrypt(payment.order.customer.first_name) + " "+ encrypter.decrypt(payment.order.customer.last_name)) 
            }
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
            order = self.getOrderCustomer(user,int(order_id))
            
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
        self.orderAccess.deleteOrderByID(int(intent.metadata['order_id']))
        return {'msg': e.user_message, 'error':e.code}, 200
    except stripe.error.APIConnectionError as e:

        # Network communication with Stripe failed
        print(e.message)
        self.orderAccess.deleteOrderByID(int(intent.metadata['order_id']))
        return {'msg':e.user_message, 'error':e.code}, 200
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print(e.message)
        self.orderAccess.deleteOrderByID(int(intent.metadata['order_id']))
        return {'msg':e.user_message, 'error':e.code}, 200
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print(e.message)
        self.orderAccess.deleteOrderByID(int(intent.metadata['order_id']))
        return {'msg':e.user_message, 'error':e.code}, 200
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print(e.message)
        self.orderAccess.deleteOrderByID(int(intent.metadata['order_id']))
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
        print('Payment intent', intent.amount)
        self.paymentAccess.recordCardPayment(order_id, intent.amount/100, encrypter.encrypt(intent.id))
        print("passed payment access")
        # self.orderAccess.updateStatus(order_id,'delivered')
        print("passed updatestatus")
        # self.__sendEmail(order_id,mail)
        print("passed send email")
        return {'msg':'success','data':{}}, 200
    else:
        # Invalid status
        return {'msg': 'Invalid PaymentIntent status', 'error':'ise-0001'}, 500


def __sendEmail(self,order_id,mail):
    '''send invoice to customer for completed payment'''
    order = self.orderAccess.getOrderById(order_id)
    print("passed get by order id")
    order_details = self.__getOrderDetails(order)
    print('passed get order details')
    customer = order.customer

    msg = Message(recipients=[str(encrypter.decrypt(customer.email))])
    print('passed Message')
    msg.subject = "Payment Confirmation for Order "+str(order_id)
    if order:
        html = render_template('base.html', order=order_details, customer=customer)
        print('passed render template')
        pdf = render_pdf(HTML(string=html))
        print(pdf)
        print('passed render pdf')
        msg.attach(filename="invoice_"+str(order.id)+".pdf",disposition="attachment",content_type="application/pdf",data=pdf)
        msg.body="""Dear {},\nyour order has been completed and payment received for {}, please find the attachment for the same""".format(customer.first_name,order.id)
    else:
        msg.body="""Dear {},\nYour order has been completed and payment received for {}. An error has occured while generating pdf, please contact customer service""".format(customer.first_name,order.id)
    mail.send(msg)


def getSchedule(self):
    '''returns the delivery schedule'''
    orders = self.orderAccess.getSchedule()
    response = []
    if orders:
        for order in orders:
            emp = order.employee

            if emp:
                empName = (encrypter.decrypt(emp.first_name) + " " + encrypter.decrypt(emp.last_name))
            else:
                empName = 'False'
            response.append(self.__getOrderDetails(order,empName))
    return response


def __getOrderDetails(self, order):
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
                total_weight = str(order_item.quantity * order_item.groceries.unit_weight) + " grams"
                order_items.append({
                    'grocery_id': str(order_item.grocery_id),
                    'photo': order_item.groceries.photo,
                    'category': order_item.groceries.category,
                    'unit_price':str(order_item.groceries.cost_per_unit),
                    'sku': str(order_item.groceries.sku),
                    'inventory': str(order_item.groceries.quantity),
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
        'payment_type': str(encrypter.decrypt(order.payment_type)), 
        'order_date': str(order.orderdate),
        'status': str(encrypter.decrypt(order.status)), 
        'customer_id': str(order.customer_id),
        'customer': encrypter.decrypt(order.customer.first_name) + " " + encrypter.decrypt(order.customer.last_name),
        'formatted_delivery_date': order.delivery_date.strftime("%B %d %Y") if order.delivery_date else str(None),
        'delivery_timeslot': str(order.timeslot.start_time)+"-"+str(order.timeslot.end_time) if order.timeslot else str(None),
        'delivery_date': str(order.delivery_date),
        'delivery_street': str(encrypter.decrypt(order.delivery_street)),
        'delivery_town': str(encrypter.decrypt(order.delivery_town)), 
        'delivery_parish': str(encrypter.decrypt(order.parish.name)), 
        'checkout_by': str(encrypter.decrypt(order.employee.first_name)) + " " + str(encrypter.decrypt(order.employee.last_name))
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
