from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access)


@manage_order.route('/makeOrder', methods=['POST'])
def makeOrder():
    return

@manage_order.route('/scheduleOrder', methods=['POST'])
def scheduleOrder():
    return


@manage_order.route('/removeFromCart', methods=['POST'])
def removeFromCart():
    return