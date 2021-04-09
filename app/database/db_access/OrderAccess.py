from ... import db
from datetime import datetime
from ..Models import Order
from ..Models import OrderGroceries
from ..Models import Cart
from sqlalchemy import and_, or_, not_

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

    def getOrders(self):
        orders = Order.query.filter_by().all()
        try:
            if orders[0].id:
                return orders
        except:
            return False

    def scheduleDelivery(self, orderId, date, town, parish):
        
        order = self.getOrderById(orderId)
        if order:
            order.deliveryDate = date
            order.deliveryTown = town
            order.deliveryParish = parish
            db.session.commit()
            return order
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
        orders = Order.query.filter(or_(Order.status.like('PENDING'),Order.status.like('CHECKED OUT'))).all()
        try:
            if orders[0].id:
                return orders
        except:
            return False

    def getCustomerOrders(self,custId):
        orders = Order.query.filter_by(customer_id=custId).all()
        try:
            if orders[0].id:
                return orders
        except:
            return False

    def getCustomerPendingOrder(self,custId):
        orders = Order.query.filter(and_(or_(Order.status.like('PENDING'),Order.status.like('CHECKED OUT')),Order.customer_id.like(custId))).all()
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

    def cancelOrder(self, orderId):
        return self.updateStatus(orderId,'CANCELED')


