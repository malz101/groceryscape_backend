from .. import db
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    checkouts = db.relationship('Order', backref='employee')

orders_groceries = db.Table('order_details',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id'), primary_key=True),
    db.Column('quantity', db.Integer),
    db.Column('price', db.Numeric(10,2))
)

CartItems = db.Table('cart_items',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('grocery_id', db.Integer, db.ForeignKey('grocery.id'), primary_key=True),
    db.Column('quantity', db.Integer),
    db.Column('cost', db.Numeric(10,2))
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    deliveryDate = db.Column(db.DateTime)
    deliveryTown = db.Column(db.String(45), nullable=False)
    deliveryParish = db.Column(db.String(45), nullable=False)

    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    checkoutBy = db.Column(db.Integer, db.ForeignKey('employee.id'))

    foodItems = db.relationship('Grocery', secondary=orders_groceries)

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)# unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(100), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10,2), nullable=False)


class Payment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    payment_date = db.Column(db.DateTime())
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)
    recordedBy = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Cart(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'))
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Numeric(10,2), nullable=True)

    cartItems = db.relationship('Grocery', secondary=CartItems)

class Rating(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

