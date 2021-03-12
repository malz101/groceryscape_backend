from flask import Blueprint
from flask import redirect, url_for, session, request
from SystemManagement.CartManager import CartManager
from database.CartAccess import CartAccess
from database.GroceryAccess import GroceryAccess
from database.OrderAccess import OrderAccess
from database.CustomerAccess import CustomerAccess


manage_cart = Blueprint("manage_cart", __name__)

cart_manager = CartManager(CartAccess(GroceryAccess(), OrderAccess(), CustomerAccess))

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