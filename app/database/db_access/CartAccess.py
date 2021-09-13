from ... import db
from ..models import Cart
from ..models import Grocery
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_, func
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
                
                if (grocery.quantity > 0) and (quantity <= grocery.quantity) and quantity>-1:
                    # self.groceryAccess.updateGrocery(grocery.id,'quantity', grocery.quantity - quantity)
                    cart = Cart(cart_id=customer.id, quantity=quantity)
                    cart.cart_items = grocery
                    customer.cart_items.append(cart)
                    db.session.add(cart)
                    db.session.commit()
                    return True
                    # return self.getAllCartItems(cartId)
                else:
                    raise ValueError
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
        cart_item = Cart.query.filter_by(cart_id=cartId, item_id=itemId).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return True
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
        return cartItems


    def updateCart(self, cartId, new_values):
        item_ids = [int(key) for key in new_values.keys()]
        # print('item_ids',item_ids)
        cart_items = Cart.query.filter(and_(Cart.cart_id==cartId,Cart.item_id.in_(item_ids))).all()
        # print('cart items',str(cart_items))
        updated_cart = []
        for cartItem in cart_items:
            quantity = int(new_values[str(cartItem.item_id)])
            grocery = cartItem.cart_items
            
            if (grocery.quantity > 0) and (quantity <= grocery.quantity) and quantity>-1:
                    cartItem.quantity = quantity
                    if quantity > 0:
                        updated_cart.append(cartItem)
                    else:
                        db.session.delete(cartItem)
            else:
                # cartItem.quantity = quantity
                db.session.rollback()
                raise ValueError
        db.session.commit()
        return updated_cart
            

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
