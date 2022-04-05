from app import db
from ..Models import CashPayment, CardPayment
from datetime import datetime
class PaymentAccess:

    def recordCashPayment(self, order_total, empId, amountTendered):
        '''stores payment details of cash payment to database'''
        change = amountTendered - order_total 
        if change >= 0:
            payment = CashPayment(order_id=orderId,recorded_by=empId, amount_tendered=amountTendered,\
                            change=change)
            db.session.add(payment)
            db.session.commit()
            return payment
        else:
            return False
    

    def recordCardPayment(self, order_id, amount, intent_id):
        '''stores details of card payment to database'''
        payment = CardPayment(order_id,amount, intent_id)
        db.session.add(payment)
        db.session.commit()
        
  


