from ... import db
from datetime import datetime, timedelta, timezone
from ..Models import Order
from ..Models import OrderGroceries
from .OrderGroceriesAccess import OrderGroceriesAccess
from .CustomerAccess import CustomerAccess
from .GroceryAccess import GroceryAccess
from ..Models import Cart
from sqlalchemy import and_, or_, not_
import time

class OrderAccess:

    def createOrder(self, custId):
        order = Order(customer_id=custId)
        db.session.add(order)
        db.session.commit()
        return self.getOrderById(order.id)

    def getOrderById(self, orderId):
        order = Order.query.filter_by(id=orderId).first()
        try:
            if order.id:
                return order
        except:
            return False

    def dumpCart(self, cartItems):

        order = self.createOrder(cartItems[0].cart_id)

        for item in cartItems:
            orderGroceries = OrderGroceries(order_id=order.id, grocery_id=item.item_id, quantity=item.quantity)
            db.session.add(orderGroceries)
            db.session.commit()
        return order.id
    
    def updateStatus(self,orderId, status):
        order = self.getOrderById(orderId)
        if order:
            order.status = status
            db.session.commit()
            return True
        else:
            return  False


    def scheduleDelivery(self, orderId, date,custId):
        
        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                order.deliveryDate = date
                db.session.commit()
                return order
            else:
                return False #raise an exception error here to indicate auth error
        else:
            return False
            
    def checkoutOrder(self, orderId, employee):
        order = self.getOrderById(orderId)
        if order:
            order.checkout_by = employee
            order.status = 'CHECKED OUT'
            db.session.commit()
            return  order
        else:
            return False

    def getSchedule(self):
        orders = Order.query.filter(or_(Order.status=='PENDING',Order.status=='CHECKED OUT')).all()
        try:
            if orders[0].id:
                return orders
        except:
            return False

    def getOrders(self,custId=None, status=None, min_order_timestamp=None,\
                            max_order_timestamp=None, min_delivery_timestamp=None,\
                            max_delivery_timestamp=None, delivery_town=None,delivery_parish=None):
        
        if status is None:
            status = ''
        status = '%{}%'.format(status)

        if min_order_timestamp is None:
            min_order_timestamp = datetime(1970, 1, 1,tzinfo=timezone.utc)
        
        if min_delivery_timestamp is None:
            min_delivery_timestamp = datetime(1970, 1, 1,tzinfo=timezone.utc)

        current_time = datetime.utcnow() # get current date and time
        # min_order_timestamp =  '%{}%'.format(min_order_timestamp)
        if max_order_timestamp is None:
            max_order_timestamp = current_time#.strftime('%Y-%m-%d %H:%M:%S')
        else:
            max_order_timestamp = datetime.strptime(max_order_timestamp, '%Y-%m-%d %H:%M:%S')

        delivery_range_provided = datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        if max_delivery_timestamp is None:
            max_delivery_timestamp =  current_time + timedelta(days=2)
            delivery_range_provided = None
        else:
            max_delivery_timestamp = datetime.strptime(max_delivery_timestamp, '%Y-%m-%d %H:%M:%S')


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

        if custId is not None:
            orders = Order.query.filter(
                and_(
                    Order.customer_id==custId,\
                    Order.status.ilike(status),\
                    or_(Order.deliverytown.ilike(delivery_town), Order.deliverytown == town_provided),\
                    or_(Order.deliveryparish.ilike(delivery_parish), Order.deliveryparish == parish_provided),\
                    and_(Order.orderdate >= min_order_timestamp, Order.orderdate <= max_order_timestamp),\
                    or_(
                        and_(Order.deliverydate >= min_delivery_timestamp, Order.deliverydate <= max_delivery_timestamp),\
                        Order.deliverydate == delivery_range_provided\
                    )
                )
            ).all()
        else:
            orders = Order.query.filter(
                and_(
                    Order.status.ilike(status),\
                    or_(Order.deliverytown.ilike(delivery_town), Order.deliverytown == town_provided),\
                    or_(Order.deliveryparish.ilike(delivery_parish), Order.deliveryparish == parish_provided),\
                    and_(Order.orderdate >= min_order_timestamp, Order.orderdate <= max_order_timestamp),\
                    or_(
                        and_(Order.deliverydate >= min_delivery_timestamp, Order.deliverydate <= max_delivery_timestamp),\
                        Order.deliverydate == delivery_range_provided\
                    )
                )
            ).all()            
        
        # try:
        if orders:
            return orders
        # except:
        return False


    def getCustomerPendingOrder(self,custId):
        orders = Order.query.filter(and_(Order.customer_id==int(custId),\
                                            or_(Order.status=='PENDING',Order.status=='CHECKED OUT'))).all()
        try:
            if orders[0].id:
                # orders = [order for order in orders if order.customer_id == custId]
                newOrder = []
                for order in orders:
                    if order.status == 'PENDING':
                        newOrder.append(order)
                if not newOrder == []:
                    return newOrder
                else:
                    return False
            else:
                return False
        except:
            return False

    def cancelOrder(self, custId, orderId):
        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                self.updateStatus(orderId,'CANCELED')
                return order
            else:
                return  False
        else:
            return False

    def setDeliveryLocation(self, custId, orderId, parish, town):
        order = self.getOrderById(orderId)
        if order:
            if order.customer_id == custId:
                order.deliveryparish = parish
                order.deliverytown = town
                db.session.commit()
                return order
            else:
                return False
        else:
            return False

    def getItemsInOrder(self, orderId):
        return OrderGroceriesAccess(self, GroceryAccess(), CustomerAccess()).getAllItemsOnOrder(orderId)

    def getTax(self,groceryId, type):
        return GroceryAccess().getTax(groceryId,type)

    def getTotalOnOrder(self, orderId):
        return OrderGroceriesAccess(self, GroceryAccess(), CustomerAccess()).getTotalOnOrder(orderId)

    def getDeliveryCost(self,orderId):
        return OrderGroceriesAccess(self, GroceryAccess(), CustomerAccess()).getDeliveryCost(orderId)

