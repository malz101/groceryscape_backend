from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.CartManager import CartManager
from ..database.db_access import cart_access
from ..database.db_access import grocery_access

manage_cart = Blueprint("manage_cart", __name__)

cart_manager = CartManager(cart_access, grocery_access)

@manage_cart.route('/addToCart', methods=['POST','GET'])
def addToCart():

    if 'cust_id' in session:
        cart = cart_manager.addToCart(request, session)
        return cart
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_cart.route('/CheckOutCart', methods=['POST', 'GET'])
def CheckOutCart():
    cart_manager.checkoutCart(request)
    return {"res":"check db"}

@manage_cart.route('/removeFromCart', methods=['POST', 'GET'])
def removeFromCart():

    return

@manage_cart.route('/emptyCart', methods=['POST','GET'])
def emptyCart():

    cart_manager.emptyCart(1)
    return {'res':'cart emptied'}