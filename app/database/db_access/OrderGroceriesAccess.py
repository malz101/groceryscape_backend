from sqlalchemy import exc
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

    def getGroceryPairFreq(self, groceryId):
        """ Returns a list of the number of times a pair of groceries
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

        # Maping groceries to orders and vice versa
        groceries = OrderGroceries.query.all()
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
