from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.CustomerAccountManager import AccountManager
from ..database.db_access import customer_access
from ..system_management.MLManager import MLManager
from ..database.db_access import rating_access
from ..database.db_access import grocery_access
from ..database.db_access import order_access


"""All requests that are related to the management of a customer's account should come to this route"""
manage_customer_account = Blueprint("manage_customer_account", __name__)

"""create an object that manages all operations on a customer's account"""
customer_manager = AccountManager(customer_access, MLManager(rating_access,grocery_access),order_access)


"""handles customers' account requests"""
@manage_customer_account.route('/signup', methods=['POST'])
def signup():
    """Pass all the responsibility of creating an account to the account manager"""
    try:
        customer = customer_manager.createAccount(request)
        if customer:
            response = {'msg': 'account created', 'data':{}}, 201
        else:
            response = {'msg': 'email address already exits', 'error':'create-0001'}, 404
    except Exception as e:
        print(e)
        reponse = {'msg': '', 'error':'ise-0001'}, 500
    finally:
        return reponse

@manage_customer_account.route('/login', methods=["POST"])
def login():
    try:
        customer = customer_manager.login(request)
        if customer:
            token = create_access_token(identity=customer)
            response = {'msg':'', 'data': {"token": token, "customer":customer}}, 200
        else:
            response = {
                'msg':'Incorrect email or password', 
                'error': 'auth-0001',
                'detail': 'Authentication failed due to incorrect username or password.'
            }, 401

    except Exception as e:
        print(e)
        response = {'msg':'', 'error': 'ise-0001'}, 500
    finally:
        return response


@manage_customer_account.route('/logout', methods=["GET"])
@jwt_required()
def logout():
    user = get_jwt_identity()
    # print(user)
    try:
        if user:
            # return {'msg' : 'logout success', 'data':{}}, 200
            return redirect(url_for('index'))
        return {'msg': 'user cannot be identified', 'error': 'jwt-0001'}, 401

    except Exception as e:
        print(e)
        return {'msg': '', 'error':'internal server error'}, 500

@manage_customer_account.route('/update_account', methods=["POST"])
@jwt_required()
def update_account():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            customer = customer_manager.updateAccount(request,user)
            # print('Custoemr',customer)
            if customer:
                response = {'msg':'account was updated', 'data':{'customer':customer}}, 201
            else:
                response = {'msg':'account does not exist', 'error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg': '', 'error':'internal server error'}, 500
        finally:
            return response
    return redirect(url_for('index'))

@manage_customer_account.route('/get_customer', methods=["GET"])
@jwt_required()
def get_customer():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            customer = customer_manager.get_customer(user['cust_id'])
            if customer:
                response = {'msg': 'success','data': {'customer':customer}}, 200
            else:
                response = {'msg':'user with id '+user_id+' does not exist','error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
            
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/get_recommended_groceries', methods=["GET","POST"])
@jwt_required()
def get_recommended_groceries():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            groceries = customer_manager.getRecommendedGroceries(user)
            reponse = {'msg': '', 'data':{'groceries':groceries}}, 200
        except NameError:
            response = {'msg': 'customer not found', 'data': {}}, 200
        except Exception as e:
            print(e)
            response = {'msg': '', 'error': 'ise-0001'}, 500
        finally:
            return reponse

    else:
        return redirect(url_for('index'))
    
    
@manage_customer_account.route('/get_my_orders', methods=["GET"])
@jwt_required()
def get_my_orders():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            orders = customer_manager.getMyOrders(user,request)
            if orders:
                response = {'msg': '', 'data':{'orders':orders}}, 200
            else:
                response = {'msg': 'no orders found', 'data':{}}, 200

        except Exception as e:
            print(e)
            response = {'msg': '', 'error':'ise-0001'}, 500
        finally:
            return response
    
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/cancel_order/<order_id>', methods=["GET","POST"])
@jwt_required()
def cancel_order(order_id):
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            msg = customer_manager.cancelOrder(user, order_id)
            if msg:
                response = {'msg':'order successfully cancelled', 'data':{'msg':msg}}, 200
            else:
                reponse = {'msg': 'order cancellation unsuccessful', 'error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return redirect(url_for('index'))


@manage_customer_account.route('/set_delivery_location/<order_id>', methods=["POST"])
@jwt_required()
def set_delivery_location(order_id):
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            order = customer_manager.setDeliveryLocation(user, request, order_id)
            print(order)
            if order:
                response = {'msg':'delivery location update successful', 'data':{'order':order}}, 200
            else:
                response = {'msg':'delivery loction update unsuccessful', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            response = response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return redirect(url_for('index'))