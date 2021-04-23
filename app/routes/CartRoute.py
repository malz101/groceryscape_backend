from flask import Blueprint
from flask import redirect, url_for, session, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.CartManager import CartManager
from ..database.db_access import cart_access
from ..database.db_access import grocery_access

manage_cart = Blueprint("manage_cart", __name__)

cart_manager = CartManager(cart_access, grocery_access)
emp_login_restrict_msg = {'msg':'you account does not have a cart'}

@manage_cart.route('/addToCart', methods=['POST','GET'])
@jwt_required()
def addToCart():
    user = get_jwt_identity()
    if not 'role' in user: 
        cart = cart_manager.addToCart(request, user)
        return cart
    else:
        return emp_login_restrict_msg

@manage_cart.route('/CheckOutCart', methods=['POST', 'GET'])
@jwt_required()
def CheckOutCart():
    user = get_jwt_identity()
    if not 'role' in user: 
        order = cart_manager.checkoutCart(user)
        return order
    else:
        return emp_login_restrict_msg
    
@manage_cart.route('/removeFromCart', methods=['POST', 'GET'])
@jwt_required()
def removeFromCart():
    
    user = get_jwt_identity()
    if not 'role' in user:
        cartItems = cart_manager.removeItemFromCart(request, user)
        return cartItems
    else:
        return emp_login_restrict_msg
    
@manage_cart.route('/empty_cart', methods=['GET'])
@jwt_required()
def empty_cart():
    user = get_jwt_identity()
    if not 'role' in user:
        cartItems = cart_manager.emptyCart(user)
        return cartItems
    else:
        return emp_login_restrict_msg
    

@manage_cart.route('/get_cart_items', methods=['GET'])
@jwt_required()
def get_cart_items():
    user = get_jwt_identity()
    if not 'role' in user:
        cartItems = cart_manager.getAllCartItems(user)
        return cartItems
    else:
        return emp_login_restrict_msg

@manage_cart.route('/update_cart', methods=['POST','GET'])
@jwt_required()
def update_cart():
    user = get_jwt_identity()
    if not 'role' in user:
        cartItem = cart_manager.updateCartItem(request, user)
        return cartItem
    else:
        return emp_login_restrict_msg
    

