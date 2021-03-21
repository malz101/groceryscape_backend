from ... import db
from ..Models import Cart
from ..Models import Grocery
from datetime import datetime


class CartAccess:

    def __init__(self, groceryAccess, orderAccess, customerAccess):
        self.groceryAccess = groceryAccess
        self.orderAccess = orderAccess
        self.customerAccess = customerAccess

    def addToCart(self, itemId, cartId, quantity):

        # 1) get both get both customer and grocery from the db to ensure that they are valid
        grocery = self.groceryAccess.searchForGrocery(itemId)
        customer = self.customerAccess.getCustomerById(cartId)

        # 2) if grocery and cust are valid make an entry into the cart table
        if grocery and customer:

            cart = Cart(cart_id=customer.id, quantity=quantity, cost=grocery.cost_per_unit*quantity )
            cart.cart_items = grocery
            customer.cart_items.append(cart)
            db.session.add(cart)
            db.session.commit()

            return self.getAllCartItems(cartId)

        # 3) if grocery or customer is not valid, abort the operation
        else:
            return False

    def emptyCart(self, cartId):

        # 1) check if there are atleast one cart entry for customer
        cart = Cart.query.filter_by(cart_id=cartId).first()

        try:
            if cart.cart_id:
                # 2) if there is atleast one cart entry for customer
                cartItems = Cart.query.filter_by(cart_id=cartId).all()
                for entry in cartItems:
                    db.session.delete(entry)
                    db.session.commit()
                return True
            else:
                return False

        except:
            return False

    def removeItem(self, cartId, itemId):

        # 1) check if the grocery is already in the customers cart
        cartEntry = self.getCartItem(cartId, itemId)
        if cartEntry:
            # 2) if entry is in customer's cart, remove entry
            db.session.delete(cartEntry)
            db.session.commit()
            return self.getAllCartItems(cartId)
        else:
            # 3) otherwise return error msg
            return False


    def checkoutCart(self, custId):

        # 1) check if customer exits
        customer = self.customerAccess.getCustomerById(custId)
        if customer:
            # 2) get all cart items
            cartItems = self.getAllCartItems(customer.id)
            if cartItems:
                orderId = self.orderAccess.dumpCart(cartItems)
                # self.emptyCart(custId)
                return self.orderAccess.getOrderById(orderId)
            return False
        return False

    def getCartItem(self, cartId, itemId):

        # 1) check if cart entry is in db
        cart = Cart.query.filter_by(cart_id=cartId, item_id=itemId).first()

        # 2) if the cart entry found return the cart
        try:
            if cart.cart_id:
                return cart
        except:
            return False

    def getAllCartItems(self, cartId):

        cartItems = Cart.query.filter_by(cart_id=cartId).all()

        try:
            if cartItems[0].cart_id:
                return cartItems
        except:
            return False

    def updateCartItem(self, cartId, itemId, quantity):

        cartItem = self.getCartItem(cartId, itemId)
        if cartItem:
            if quantity < 1:
                quantity = 1
            cartItem.quantity = quantity
            cartItem.cost = cartItem.cart_items.cost_per_unit * quantity
            db.session.commit()
            return self.getCartItem(cartId, itemId)
        else:
            return False





