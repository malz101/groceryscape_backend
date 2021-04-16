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
@manage_customer_account.route('/signup', methods=['POST', 'GET'])
def signup():

    """Pass all the responsibility of creating an account to the account manager"""
    customer = customer_manager.createAccount(request)
    if customer:
        session['cust_id'] = customer['cust_id']
        token = create_access_token(identity=customer)
        return {"token": token, "customer":customer}
    else:
        return {'error':'failed request'}

@manage_customer_account.route('/login', methods=["POST", "GET"])
def login():
    customer = customer_manager.login(request)
    if customer:
        session['cust_id'] = customer['cust_id']
        token = create_access_token(identity=customer)
        return {"token": token, "customer":customer}
    else:
        return {'error': 'Invalid login details'}

@manage_customer_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'cust_id' in session:
        session.pop('cust_id', None)
    return redirect(url_for('index'))

@manage_customer_account.route('/update_account', methods=["GET", "POST"])
@jwt_required()
def update_account():
    user = get_jwt_identity()
    if user:
        customer = customer_manager.updateAccount(request,user)
        return customer
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/get_customer', methods=["GET"])
@jwt_required()
def get_customer():
    user = get_jwt_identity()
    if user:
        return user
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/get_recommended_groceries', methods=["GET","POST"])
@jwt_required()
def get_recommended_groceries():
    user = get_jwt_identity()
    if user:
        groceries = customer_manager.getRecommendedGroceries(user)
        return groceries
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/get_pending_orders', methods=["GET","POST"])
@jwt_required()
def get_pending_orders():
    user = get_jwt_identity()
    if user:
        orders = customer_manager.getMyPendingOrders(user)
        return orders
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/get_my_orders', methods=["GET","POST"])
@jwt_required()
def get_my_orders():
    user = get_jwt_identity()
    if user:
        orders = customer_manager.getMyOrders(user)
        return orders
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/cancel_order', methods=["GET","POST"])
@jwt_required()
def cancel_order():
    user = get_jwt_identity()
    if user:
        msg = customer_manager.cancelOrder(request)
        return msg
    else:
        return redirect(url_for('index'))
