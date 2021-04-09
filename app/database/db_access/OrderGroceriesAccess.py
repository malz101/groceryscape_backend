from ... import db
from ..Models import OrderGroceries

class OrderGroceriesAccess:

    def __init__(self, orderAccess, groceryAccess, customerAccess):
        self.orderAccess = orderAccess
        self.groceryAccess = groceryAccess
        self.customerAccess = customerAccess

    def getAllItemsOnOrder(self, orderId):

        order = self.orderAccess.getOrderById(orderId)
        if order:
            items = OrderGroceries.query.filter_by(order_id=orderId).all()

            try:
                if items[0].order_id:
                    return items
            except:
                return False

    def getTotalOnOrder(self, orderId):
        items = self.getAllItemsOnOrder(orderId)
        total = 0
        if items:
            for item in items:
                total += item.price
            return total
        else:
            return False



