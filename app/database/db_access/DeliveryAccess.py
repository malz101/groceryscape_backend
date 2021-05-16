from ... import db
from ..Models import DeliveryTimeSlot, MaxDeliveriesPerSlot,DeliveryParish, OrderGroceries 

class DeliveryAccess:

    def getDeliveryTimeSlot(self,id):
        '''returns a delivery time specified by id'''
        timeslot = DeliveryTimeSlot.query.filter_by(id=id).first()
        return timeslot
        
    def getDeliveryTimeSlots(self):
        '''return all valid delivery time slots in the database'''
        timeslots = DeliveryTimeSlot.query.all()
        return timeslots

    def getDeliveryParish(self,parish):
        '''return a delivery parish specified by id'''
        parish = DeliveryParish.query.filter_by(parish=parish).first()
        return parish
        
    def getDeliveryParishes(self):
        '''return all delivery parishes in the database'''
        parishes = DeliveryParish.query.all()
        return parishes
    
    def getMaxDeliveriesPerTimeSlot(self):
        '''returns maximum allowed deliveries perslot'''
        max_deliveries_per_slot = MaxDeliveriesPerSlot.query.first()
        return max_deliveries_per_slot.max_deliveries_per_time_slot

    # def getTotalOnOrder(self, orderId):
    #     items = self.getAllItemsOnOrder(orderId)
    #     total = 0
    #     if items:
    #         for item in items:
    #             # print(item.orders.deliveryparish)
    #             delivery_cost = float(self.getParish(str(item.orders.deliveryparish)).delivery_rate)
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

    # def getDeliveryCost(self,orderId):
    #     order = self.orderAccess.getOrderById(orderId)
    #     if order:
    #         return float(self.getParish(str(order.deliveryparish)).delivery_rate)
    #     else:
    #         return False