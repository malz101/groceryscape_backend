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
        return self.getOrderbyId(order.id)

    def getOrderbyId(self, orderId):
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
        return True

    def cancelOrder(self, orderId):
        pass

    def getOrderById(self, orderId):
        pass

    def getAllOrders(self):
        pass

    def scheduleDelivery(self, orderId, date, town, parish):
        pass

    def checkoutBy(self, orderId, employee):
        pass



