from app import db
from ..models import OrderGroceries
from ..models import DeliveryParish

class DeliveryParishAccess:

    def getDeliveryParish(self,parish):

        parish = DeliveryParish.query.filter_by(parish=parish).first()
        return parish
        
    def getDeliveryParishes(self):
        parishes = DeliveryParish.query.all()
        return parishes
        
    # def getTotalOnOrder(self, orderId):
    #     items = self.getAllItemsOnOrder(orderId)
    #     total = 0
    #     if items:
    #         for item in items:
    #             # print(item.orders.delivery_parish)
    #             delivery_cost = float(self.getParish(str(item.orders.delivery_parish)).delivery_rate)
    #             cost_before_tax = item.quantity * item.groceries.cost_per_unit
    #             GCT = self.groceryAccess.getTax(item.grocery_id, 'GCT') * item.quantity
    #             SCT = self.groceryAccess.getTax(item.grocery_id, 'SCT') * item.quantity
    #             total_on_item = float(cost_before_tax) + float(GCT) + float(SCT) + delivery_cost
    #             total += total_on_item
    #         return total
    #     else:
    #         return False

    # def getParish(self,parish):
    #     par = DeliveryParish.query.filter_by(parish=parish).first()
    #     return par

    def getDeliveryCost(self,orderId):
        order = self.orderAccess.getOrderById(orderId)
        if order:
            return float(self.getParish(str(order.delivery_parish)).delivery_rate)
        else:
            return False

