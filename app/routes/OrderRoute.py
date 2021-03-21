from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
def schedule_order():
    return

@manage_order.route('/cancel_order', methods=['POST','GET'])
def cancel_order():
    return

@manage_order.route('/get_order', methods=['POST','GET'])
def get_order():
    return

@manage_order.route('/get_orders', methods=['POST','GET'])
def get_orders():
    return