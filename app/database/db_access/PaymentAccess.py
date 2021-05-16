from ... import db
from ..Models import Payment
from datetime import datetime
class PaymentAccess:
    
    def __init__(self, orderAccess,orderGroceriesAccess, employeeAccess):
        self.orderAccess = orderAccess
        self.orderGroceriesAccess = orderGroceriesAccess
        self.employeeAccess = employeeAccess
        
    def recordPayment(self, orderId, empId, amountTendered):

        total = self.orderGroceriesAccess.getTotalOnOrder(orderId)
        change = amountTendered - float(total) 
        if change >= 0:
            payment = Payment(order_id=orderId,recorded_by=empId, amount_tendered=amountTendered,\
                            change=change)
            self.orderAccess.updateStatus(orderId,'SERVED')
            db.session.add(payment)
            db.session.commit()
            return payment
        else:
            return False
    
    


