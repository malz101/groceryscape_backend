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
