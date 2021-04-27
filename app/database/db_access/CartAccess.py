from ... import db
from ..Models import Cart
from ..Models import Grocery
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class CartAccess:

    def __init__(self, groceryAccess, orderAccess, customerAccess):
        self.groceryAccess = groceryAccess
        self.orderAccess = orderAccess
        self.customerAccess = customerAccess

    def addToCart(self, itemId, cartId, quantity):
        try:
            # 1) get both get both customer and grocery from the db to ensure that they are valid
            grocery = self.groceryAccess.searchForGrocery(itemId)
            customer = self.customerAccess.getCustomerById(cartId)

            if grocery and customer:
                
                if (grocery.quantity > 0) and (quantity <= grocery.quantity):
                    self.groceryAccess.updateGrocery(grocery.id,'quantity', grocery.quantity - quantity)
                    cart = Cart(cart_id=customer.id, quantity=quantity)
                    cart.cart_items = grocery
                    customer.cart_items.append(cart)
                    db.session.add(cart)
                    db.session.commit()
                    return self.getAllCartItems(cartId)
                else:
                    return False
            # 3) if grocery or customer is not valid, abort the operation
            else:
                return False
        except IntegrityError as e:
            db.session.rollback()
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
            grocery = self.groceryAccess.searchForGrocery(cartEntry.item_id)
            self.groceryAccess.updateGrocery(grocery.id, 'quantity', grocery.quantity + cartEntry.quantity)
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
            grocery = self.groceryAccess.searchForGrocery(cartItem.item_id)
            self.groceryAccess.updateGrocery(grocery.id, 'quantity', grocery.quantity + cartItem.quantity)
            grocery = self.groceryAccess.searchForGrocery(cartItem.item_id)
            if (grocery.quantity > 0) and (quantity <= grocery.quantity):
                if quantity < 1:
                    quantity = 1
                self.groceryAccess.updateGrocery(grocery.id, 'quantity', grocery.quantity - quantity)
                cartItem.quantity = quantity
                db.session.commit()
                return self.getCartItem(cartId, itemId)
            else:
                return False
        else:
            return False
        
    def getTotalOnCart(self, cartId):
        items = self.getAllCartItems(cartId)
        total = 0
        if items:
            for item in items:
                cost_before_tax = item.quantity * item.cart_items.cost_per_unit
                GCT = self.groceryAccess.getTax(item.item_id, 'GCT') * item.quantity
                SCT = self.groceryAccess.getTax(item.item_id, 'SCT') * item.quantity
                total_on_item = float(cost_before_tax) + float(GCT) + float(SCT)
                total += total_on_item
            return total
        else:
            return False





