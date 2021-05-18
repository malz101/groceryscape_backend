from ... import db
from datetime import datetime, timedelta, timezone, date
from ..Models import Order, OrderGroceries, Customer
# from .OrderGroceriesAccess import OrderGroceriesAccess
from .CustomerAccess import CustomerAccess
from .GroceryAccess import GroceryAccess
from ..Models import Cart
from sqlalchemy import and_, or_, not_, func
import time

class OrderAccess:

    def createOrder(self, custId, type_):
        order = Order(customer_id=custId, payment_type=type_)
        db.session.add(order)
        db.session.commit()
        # return self.getOrderById(order.id)
        return order
    

    def deleteOrderByID(self, order_id):
        Order.query.filter(id == order_id).delete()
        db.session.commit()


    def getOrderById(self, orderId):
        order = Order.query.filter_by(id=orderId).first()
        try:
            if order.id:
                return order
        except:
            return False
    
    def getOrderByIdCustomer(self, orderId, cust_id):
        order = Order.query.filter(and_(Order.customer_id==cust_id, Order.id==orderId)).first()
        try:
            if order.id:
                return order
        except:
            return False


    def addItemsToOrder(self, cart_summary,cust_id,type_):
        '''add items to created order'''
        order = self.createOrder(cust_id,type_)

        for item in cart_summary['items']:
            order_grocery = OrderGroceries(order_id=order.id, grocery_id=int(item['grocery_id']), quantity=int(item['quantity']))
            db.session.add(order_grocery)
            db.session.flush()
            # print(item)
            print('was here')
            print('Order id',order_grocery.order_id)
            print('Grocery id', order_grocery.grocery_id)
            order_grocery.groceries.quantity -= int(item['quantity'])
        db.session.commit()
        return order
    

    def updateStatus(self,orderId, status):
        order = self.getOrderById(orderId)
        if order:
            order.status = status
            db.session.commit()
            return order
        else:
            return  False


    def scheduleDelivery(self, orderId,timeslot, deliverydate,custId):

        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                date_obj = datetime.strptime(deliverydate,'%Y-%m-%d').date()
                order.deliverytimeslot = timeslot
                order.deliverydate = date_obj
                db.session.commit()
                return order
            else:
                return False #raise an exception error here to indicate auth error
        else:
            return False

    

    def getDeliveryTimeSlotCount(self, deliverytimeslot, deliverydate):
        date_obj = datetime.strptime('2020-02-02','%Y-%m-%d').date()
        count = db.session.query(func.count(Order.deliverytimeslot)).filter(and_(
            Order.deliverytimeslot==deliverytimeslot,Order.deliverydate==date_obj)).first()[0]
        return count


    def checkoutOrder(self, orderId, employee):
        order = self.getOrderById(orderId)
        if order:
            order.checkout_by = employee
            order.status = 'checked out'
            db.session.commit()
            return  order
        else:
            return False

    def getSchedule(self):
        orders = Order.query.filter(or_(Order.status.ilike('pending'),Order.status.ilike('checked out'))).all()
        try:
            if orders[0].id:
                return orders
        except:
            return False


    def getOrders(self,custId=None, status=None, min_order_timestamp=None,\
                            max_order_timestamp=None, min_delivery_date=None,\
                            max_delivery_date=None, delivery_town=None,delivery_parish=None, payment_type=None):
        
        if status is None:
            status = ''
        status = '%{}%'.format(status)

        if min_order_timestamp is None:
            min_order_timestamp = datetime(1970, 1, 1,tzinfo=timezone.utc)
        
        if min_delivery_date is None:
            min_delivery_date = date(1970, 1, 1)

        current_time = datetime.utcnow() # get current date and time
        # min_order_timestamp =  '%{}%'.format(min_order_timestamp)
        if max_order_timestamp is None:
            max_order_timestamp = current_time#.strftime('%Y-%m-%d %H:%M:%S')
        else:
            max_order_timestamp = datetime.strptime(max_order_timestamp, '%Y-%m-%d %H:%M:%S')

        # delivery_range_provided = datestrptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        delivery_range_provided = date(1,1,1)
        if max_delivery_date is None:
            max_delivery_date =  date.today() + timedelta(days=2)
            delivery_range_provided = None
        else:
            max_delivery_date = datetime.strptime(max_delivery_date, '%Y-%m-%d')

        town_provided = ''
        if delivery_town is None:
            town_provided = None
            delivery_town = ''
        delivery_town = '%{}%'.format(delivery_town)

        parish_provided = ''
        if delivery_parish is None:
            parish_provided = None
            delivery_parish = ''
        delivery_parish = '%{}%'.format(delivery_parish)

        payment_type_provided = ''
        if payment_type is None:
            payment_type_provided = None
            payment_type = ''
        payment_type = '%{}%'.format(payment_type)
        

        if custId is not None:
            orders = Order.query.filter(
                and_(
                    Order.customer_id==custId,\
                    Order.status.ilike(status),\
                    or_(Order.deliverytown.ilike(delivery_town), Order.deliverytown == town_provided),\
                    or_(Order.deliveryparish.ilike(delivery_parish), Order.deliveryparish == parish_provided),\
                    or_(Order.payment_type.ilike(payment_type), Order.payment_type == payment_type_provided),\
                    and_(Order.orderdate >= min_order_timestamp, Order.orderdate <= max_order_timestamp),\
                    or_(
                        and_(Order.deliverydate >= min_delivery_date, Order.deliverydate <= max_delivery_date),\
                        Order.deliverydate == delivery_range_provided\
                    )
                )
            ).order_by(Order.orderdate.desc()).all()
        else:
            orders = Order.query.join(Customer, Order.customer_id==Customer.id).filter(
                and_(
                    Order.status.ilike(status),\
                    or_(Order.deliverytown.ilike(delivery_town), Order.deliverytown == town_provided),\
                    or_(Order.deliveryparish.ilike(delivery_parish), Order.deliveryparish == parish_provided),\
                    or_(Order.payment_type.ilike(payment_type), Order.payment_type == payment_type_provided),\
                    and_(Order.orderdate >= min_order_timestamp, Order.orderdate <= max_order_timestamp),\
                    or_(
                        and_(Order.deliverydate >= min_delivery_date, Order.deliverydate <= max_delivery_date),\
                        Order.deliverydate == delivery_range_provided\
                    )
                )
            ).order_by(Order.orderdate.desc()).order_by(Customer.last_name).order_by(Customer.first_name).all()
        # try:
        if orders:
            return orders
        # except:
        return False


    def cancelOrder(self, custId, orderId):
        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                order.status = 'canceled'
                for order_grocery in order.groceries:
                    order_grocery.groceries.quantity += order_grocery.quantity
                # self.updateStatus(orderId,'CANCELED')
                db.session.commit()
                return order
            else:
                return  False
        else:
            return False

    def setDeliveryLocation(self, custId, orderId, street, parish, town):
        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                order.deliverystreet = street
                order.deliveryparish = parish
                order.deliverytown = town
                db.session.commit()
                return order
            else:
                return False
        else:
            return False

    # def getItemsInOrder(self, orderId):
    #     return OrderGroceriesAccess(self, GroceryAccess(), CustomerAccess()).getAllItemsOnOrder(orderId)

    def getTax(self, groceryId, type):
        return GroceryAccess().getTax(groceryId, type)

    
    # def getDeliveryCost(self,orderId):
    #     return OrderGroceriesAccess(self, GroceryAccess(), CustomerAccess()).getDeliveryCost(orderId)

    def getGroceryPairFreq(self, groceryId):
        """ Returns a dictionary of the number of times a pair of groceries
            occurs in the orders made """

        def countPairs(gid, groceryOrder, orderGrocery, result):
            try:
                for o in groceryOrder[gid]:
                    for g in orderGrocery[o]:
                        if (gid != g):
                            try:
                                temp = result[gid][g]
                            except KeyError:
                                result[gid] = {}
                                result[gid][g] = 0
                            result[gid][g] += 1
            except KeyError:
                # The grocery likely has never been purchased before
                result[gid] = {}
                pass

        orders = Order.query.filter(Order.status != 'cancelled').all()
        orderLst = [o.id for o in orders]
        groceries = OrderGroceries.query.filter(OrderGroceries.order_id.in_(orderLst)).all()

        # Maping groceries to orders and vice versa
        groceryOrder = {}
        orderGrocery = {}
        for g in groceries:
            try:
                groceryOrder[g.grocery_id].add(g.order_id)
            except KeyError:
                groceryOrder[g.grocery_id] = set()
                groceryOrder[g.grocery_id].add(g.order_id)

            try:
                orderGrocery[g.order_id].add(g.grocery_id)
            except KeyError:
                orderGrocery[g.order_id] = set()
                orderGrocery[g.order_id].add(g.grocery_id)

        result = {}
        if (type(groceryId) == str):
            countPairs(groceryId, groceryOrder, orderGrocery, result)
        elif (type(groceryId) == list):
            for gid in groceryId:
                countPairs(gid, groceryOrder, orderGrocery, result)
        return result


    def getTotalQuantityPurchased(groceryId=None):
        """ Returns a list of the total quantity of the grocery item that has
            ever been purchased """

        orders = Order.query.filter(Order.status != 'cancelled').all()
        orderLst = [o.id for o in orders]
        quantities = OrderGroceries.query.filter(OrderGroceries.order_id.in_(orderLst)).all()

        result = {}
        gids = set()
        if (groceryId == None):
            for q in quantities:
                try:
                    result[q.grocery_id] += q.quantity
                except KeyError:
                    result[q.grocery_id] = q.quantity
            return result
        elif (type(groceryId) == str):
            gids.add(groceryId)
        elif(type(groceryId) == list):
            gids.update(groceryId)

        for q in quantities:
            if (q.grocery_id in gids):
                try:
                    result[q.grocery_id] += q.quantity
                except KeyError:
                    result[q.grocery_id] = q.quantity
        return result