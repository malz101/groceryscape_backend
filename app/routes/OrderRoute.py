from flask import Blueprint
from flask import redirect, url_for, session, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access
from ..database.db_access import order_groceries_access
from ..database.db_access import payment_access

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access, order_groceries_access, payment_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
@jwt_required()
def schedule_order():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        order = order_manager.scheduleOrder(request, user)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/checkout_order', methods=['POST','GET'])
@jwt_required()
def checkout_order():
    user = get_jwt_identity()
    if user and ('role' in user):
        order = order_manager.checkOutOrder(user, request)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_order', methods=['POST','GET'])
@jwt_required()
def get_order():
    user = get_jwt_identity()
    if user and ('role' in user):
        order = order_manager.getOrder(request)
        return order
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_orders', methods=['POST','GET'])
@jwt_required()
def get_orders():
    user = get_jwt_identity()
    if user and ('role' in user):
        orders = order_manager.getOrders()
        return orders
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_total', methods=['POST','GET'])
@jwt_required()
def get_total():
    user = get_jwt_identity()
    if user and ('role' in user):
        return str(order_manager.getTotalOnOrder())
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/record_payment', methods=['POST','GET'])
@jwt_required()
def record_payment():
    user = get_jwt_identity()
    if user and ('role' in user):
        payment = order_manager.recordPayment(user,request)
        return payment
    else:
        return {'msg':'you are not logged in as an employee'}

@manage_order.route('/get_schedule', methods=['POST','GET'])
@jwt_required()
def get_schedule():
    user = get_jwt_identity()
    if user and ('role' in user):
        orders = order_manager.getSchedule()
        return orders
    else:
        return {'msg':'you are not logged in as an employee'}