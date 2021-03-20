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
    if 'cust_id' in session:
        order = cart_manager.checkoutCart(session)
        return order
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_cart.route('/removeFromCart', methods=['POST', 'GET'])
def removeFromCart():

    if 'cust_id' in session:
        cartItems = cart_manager.removeItemFromCart(request, session)
        return cartItems
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_cart.route('/emptyCart', methods=['POST','GET'])
def emptyCart():

    # cart_manager.emptyCart(1)
    return {'res':'cart emptied'}

@manage_cart.route('/get_cart_items', methods=['POST','GET'])
def get_cart_items():

    if 'cust_id' in session:
        cartItems = cart_manager.getAllCartItems(session)
        return cartItems
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_cart.route('/update_cart', methods=['POST','GET'])
def update_cart():

    if 'cust_id' in session:
        cartItem = cart_manager.updateCartItem(request,session)
        return cartItem
    else:
        return redirect(url_for('manage_employee_account.index'))

