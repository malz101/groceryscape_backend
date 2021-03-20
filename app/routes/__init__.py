from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import session

"""import blueprints (routes) for different sections of the system"""
from .CustomerRoute import manage_customer_account
from .EmployeeRoute import manage_employee_account
from .GroceryRoute import manage_groceries
from .CartRoute import manage_cart
from ..database.db_access import customer_access

from ..system_management.CustomerAccountManager import AccountManager
account_manager = AccountManager(customer_access)


"""register blueprints"""
app.register_blueprint(manage_customer_account, url_prefix="/manage_customer_account")
app.register_blueprint(manage_employee_account, url_prefix="/manage_employee_account")
app.register_blueprint(manage_groceries, url_prefix="/manage_groceries")
app.register_blueprint(manage_cart, url_prefix="/manage_cart")


"""serves the index page for customers"""
@app.route('/')
@app.route('/index')
def index():
    # if customer is logged in return home page with customer data. Otherwise, return just the home page
    if 'cust_id' in session:
        customer = account_manager.getCustomer(session['cust_id'])
        if customer:
            return {"id": customer.id, 'firstName': customer.first_name, 'lastName': customer.last_name, \
                    'telephone': customer.telephone, 'email': customer.email, 'gender': customer.gender, \
                    'town': customer.town, 'parish': customer.parish}
        else:
            return {'error': 'no customer data found!'}
    else:
        return render_template("customerViews/index.html")
