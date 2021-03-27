from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
def schedule_order():
    if 'staff_id' in session or 'admin_id':
        order = order_manager.scheduleOrder(request)
        return order
    else:
        return render_template('adminViews/admin_login.html')

@manage_order.route('/checkout_order', methods=['POST','GET'])
def checkout_order():
    if 'staff_id' in session or 'admin_id' in session:
        order = order_manager.checkOutOrder(session, request)
        return order
    else:
        return render_template('adminViews/admin_login.html')

@manage_order.route('/cancel_order', methods=['POST','GET'])
def cancel_order():
    return

@manage_order.route('/get_order', methods=['POST','GET'])
def get_order():
    if 'staff_id' in session or 'admin_id' in session:
        order = order_manager.getOrder(request)
        return order
    else:
        return render_template('adminViews/admin_login.html')

@manage_order.route('/get_orders', methods=['POST','GET'])
def get_orders():
    if 'staff_id' in session or 'admin_id' in session:
        orders = order_manager.getOrders()
        return orders
    else:
        return render_template('adminViews/admin_login.html')