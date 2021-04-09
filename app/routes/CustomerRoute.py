from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
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
        session['cust_id'] = customer['id']
        return customer
    else:
        return {'error':'failed request'}

@manage_customer_account.route('/login', methods=["POST", "GET"])
def login():
    customer = customer_manager.login(request)
    if customer:
        session['cust_id'] = customer['id']
        return customer
    else:
        return {'error': 'Invalid login details'}

@manage_customer_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'cust_id' in session:
        session.pop('cust_id', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/update_account', methods=["GET", "POST"])
def update_account():
    if 'cust_id' in session:
        customer = customer_manager.updateAccount(request,session)
        return customer
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/get_customer', methods=["GET"])
def get_customer():
    if 'cust_id' in session:
        customer = customer_manager.getCustomer(session['cust_id'])
        return customer
    else:
        return redirect(url_for('index'))

@manage_customer_account.route('/get_recommended_groceries', methods=["GET","POST"])
def get_recommended_groceries():
    if 'cust_id' in session:
        groceries = customer_manager.getRecommendedGroceries(session)
        return groceries
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/get_pending_orders', methods=["GET","POST"])
def get_pending_orders():
    if 'cust_id' in session:
        orders = customer_manager.getMyPendingOrders(session)
        return orders
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/get_my_orders', methods=["GET","POST"])
def get_my_orders():
    if 'cust_id' in session:
        orders = customer_manager.getMyOrders(session)
        return orders
    else:
        return redirect(url_for('index'))
    
@manage_customer_account.route('/cancel_order', methods=["GET","POST"])
def cancel_order():
    if 'cust_id' in session:
        msg = customer_manager.cancelOrder(request)
        return msg
    else:
        return redirect(url_for('index'))
