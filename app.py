from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import session

"""import blueprints (routes) for different sections of the system"""
from routes.CustomerRoute import manage_customer_account
from routes.EmployeeRoute import manage_employee_account
from routes.GroceryRoute import manage_groceries
from routes.CartRoute import manage_cart


app = Flask(__name__)
app.secret_key = "somepassword"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/food_delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
        user_data = session['cust_id']
        return render_template("customerViews/home.html", user=user_data)
    else:
        return render_template("customerViews/index.html")

if __name__ == "__main__":
    app.run(debug=True)