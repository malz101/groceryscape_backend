from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/food_delivery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    gender = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    town = db.Column(db.String(45), nullable=False)
    parish = db.Column(db.String(45), nullable=False)
    # dob = db.Column(db.DateTime)

    orders = db.relationship('Order', backref='customer')

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False, unique=True)
    manager_id = db.Column(db.Integer, nullable=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)
    branch_work =  db.Column(db.Integer, db.ForeignKey('branch.id'))

    # servesCustomer = db.relationship('Order', backref='employee')

orderDetails = db.Table('order_details',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id'), primary_key=True),
    db.Column('quantity', db.Integer),
    db.Column('price', db.Numeric(10,2))
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    deliveryDate = db.Column(db.DateTime)

    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # servedBy = db.column(db.Integer, db.ForeignKey('employee.id'))

    foodItems = db.relationship('Grocery', secondary=orderDetails)

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Payment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    payment_date = db.Column(db.DateTime())
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)


if __name__ == "__main__":
    db.create_all()

