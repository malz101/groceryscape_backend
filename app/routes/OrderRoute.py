from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access
from ..database.db_access import order_groceries_access
from ..database.db_access import payment_access

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access, order_groceries_access, payment_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
def schedule_order():
    if 'staff_id' in session or 'admin_id':
        order = order_manager.scheduleOrder(request)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/checkout_order', methods=['POST','GET'])
def checkout_order():
    if 'staff_id' in session or 'admin_id' in session:
        order = order_manager.checkOutOrder(session, request)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_order', methods=['POST','GET'])
def get_order():
    if 'staff_id' in session or 'admin_id' in session:
        order = order_manager.getOrder(request)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_orders', methods=['POST','GET'])
def get_orders():
    if 'staff_id' in session or 'admin_id' in session:
        orders = order_manager.getOrders()
        return orders
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_total', methods=['POST','GET'])
def get_total():
    if 'staff_id' in session or 'admin_id' in session:
        return str(order_manager.getTotalOnOrder())
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/record_payment', methods=['POST','GET'])
def record_payment():
    if 'staff_id' in session or 'admin_id' in session:
        payment = order_manager.recordPayment(session,request)
        return payment
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_schedule', methods=['POST','GET'])
def get_schedule():
    if 'staff_id' in session or 'admin_id' in session:
        orders = order_manager.getSchedule()
        return orders
    else:
        return {'msg':'you are not logged in as an employee'}