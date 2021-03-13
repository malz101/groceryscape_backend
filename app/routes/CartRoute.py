from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.CartManager import CartManager
from ..database.db_access import cart_access

manage_cart = Blueprint("manage_cart", __name__)

cart_manager = CartManager(cart_access)

@manage_cart.route('/addToCart', methods=['POST'])
def addToCart():

    cart_manager.addToCart(request)
    return

@manage_cart.route('/CheckOutCart', methods=['POST'])
def CheckOutCart():

    return

@manage_cart.route('/removeFromCart', methods=['POST'])
def removeFromCart():

    return