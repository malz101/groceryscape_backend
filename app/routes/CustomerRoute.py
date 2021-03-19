from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from ..system_management.CustomerAccountManager import AccountManager
from ..database.db_access import customer_access

"""All requests that are related to the management of a customer's account should come to this route"""
manage_customer_account = Blueprint("manage_customer_account", __name__)

"""create an object that manages all operations on a customer's account"""
customer_manager = AccountManager(customer_access)

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