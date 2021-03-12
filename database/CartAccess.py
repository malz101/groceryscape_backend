from database.Models import db
from datetime import datetime
from database.Models import Cart


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
