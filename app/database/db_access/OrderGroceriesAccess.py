from ... import db
from ..Models import OrderGroceries
from ..Models import DeliveryParish

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
                # print(item.orders.deliveryparish)
                delivery_cost = float(self.getParish(str(item.orders.deliveryparish)).delivery_rate)
                cost_before_tax = item.quantity * item.groceries.cost_per_unit
                GCT = self.groceryAccess.getTax(item.grocery_id, 'GCT') * item.quantity
                SCT = self.groceryAccess.getTax(item.grocery_id, 'SCT') * item.quantity
                total_on_item = float(cost_before_tax) + float(GCT) + float(SCT) + delivery_cost
                total += total_on_item
            return total
        else:
            return False

    def getParish(self,parish):
        par = DeliveryParish.query.filter_by(parish=parish).first()
        return par

    def getDeliveryCost(self,orderId):
        order = self.orderAccess.getOrderById(orderId)
        if order:
            return float(self.getParish(str(order.deliveryparish)).delivery_rate)
        else:
            return False

