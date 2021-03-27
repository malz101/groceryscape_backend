from ... import db
from datetime import datetime
from ..Models import Order
from ..Models import OrderGroceries
from ..Models import Cart

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
            orderGroceries = OrderGroceries(order_id=order.id, grocery_id=item.item_id, quantity=item.quantity, price=item.cost)
            db.session.add(orderGroceries)
            db.session.commit()
        return order.id

    def cancelOrder(self, orderId):
        pass

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
            db.session.commit()
            return  order
        else:
            return False




