from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from SystemManagement.CustomerAccountManager import AccountManager

"""All requests that are related to the management of a customer's account should come to this route"""
manage_customer_account = Blueprint("manage_customer_account", __name__)

"""create an object that manages all operations on a customer's account"""
customer_manager = AccountManager()

"""handles customers' account requests"""
@manage_customer_account.route('/signup', methods=['POST'])
def signu():

    """Pass all the responsibility of creating an account to the account manager"""
    cust_id = customer_manager.createAccount(request)

    session['cust_id'] = cust_id
    return redirect(url_for('index'))

@manage_customer_account.route('/login', methods=["POST"])
def login():

    cust_id = customer_manager.loginToAccount(request)
    if(cust_id):
        session['cust_id'] = cust_id
        return redirect(url_for('index'))
    else:
        return render_template("customerViews/index.html", error='ERROR')

@manage_customer_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'cust_id' in session:
        session.pop('cust_id', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))