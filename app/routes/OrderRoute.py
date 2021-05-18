from flask import Blueprint
from flask import redirect, url_for, session, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access,payment_access,delivery_access
from app import mail

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access, payment_access, delivery_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
@jwt_required()
def schedule_order():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            response = order_manager.scheduleOrder(request, user)
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401


@manage_order.route('/checkout_order', methods=['POST','GET'])
@jwt_required()
def checkout_order():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order = order_manager.checkOutOrder(user, request)
            if order:
                response = {'msg':'success','data':{'order':order}}, 200
            elif order == {}:
                response = {'msg':'Unsuccessful. Order not found', 'error':'create-0001'}, 404
            else:
                {'msg':'Unsuccessful. No order id detected', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401


@manage_order.route('/get_order/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order = order_manager.getOrder(order_id)
            if order:
                response = {'msg': 'success', 'data':{'order':order}},200
            else:
                response = {'msg':'Order not found', 'error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response

    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/get_orders', methods=['POST','GET'])
@jwt_required()
def get_orders():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            orders = order_manager.getOrders(request)
            if orders:
                response = {'msg':'success', 'data':{'orders':orders}}, 200
            else:
                response = {'msg':'no orders found', 'data':{}},200
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401


@manage_order.route('/get_schedule', methods=['POST','GET'])
@jwt_required()
def get_schedule():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            orders = order_manager.getSchedule()
            if orders:
                response = {'msg':'success', 'data':{'orders':orders}}, 200
            else:
                response = {'msg':'no orders found', 'data':{'orders':orders}}, 200
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401


@manage_order.route('/record_payment', methods=['POST','GET'])
@jwt_required()
def record_payment():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            payment = order_manager.recordCashPayment(user,request,mail)
            if payment:
                response = {'msg':'success', 'data':{'payment':payment}}, 200
            else:
                response = {'msg':'payment unsuccessful', 'error':'create-0001'}, 404
        except Exception as e:
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401



@manage_order.route('/update_order_status', methods=['POST'])
@jwt_required()
def update_order_status():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order = order_manager.updateStatus(request)
            if order:
                response = {'msg':'success', 'data':{'order':order}}, 200
            else:
                response = {'msg':'update unsuccessful', 'error':'create-0001'}, 404
        except ValueError as e:
            print(e)
            response = {'msg': 'order status or order id field is empty', 'error':'create-0001'}, 200        
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response

    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

