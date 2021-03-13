from ... import db
from ..Models import Cart
from datetime import datetime



class CartAccess:

    def __init__(self, groceryAccess, orderAccess, customerAccess):
        self.groceryAccess = groceryAccess
        self.orderAccess = orderAccess
        self.customerAccess = customerAccess

    def addToCart(self, itemId, cartId, quantity):

        grocery = self.groceryAccess.searchForGrocery(itemId)
        userId = self.customerAccess.getCustomer(cartId)

        if grocery and userId:
            pass

        # Cart(cart_id=cartId, item_id=itemId, quantity=quantity, cost=cost)
        #
        #
        # db.session.add(customer)
        # db.session.commit()
