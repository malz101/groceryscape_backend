from .. import db
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    telephone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    gender = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    town = db.Column(db.String(45), nullable=False)
    parish = db.Column(db.String(45), nullable=False)

    orders = db.relationship('Order', backref='customer')

    #cart associated many to many
    cart_items = db.relationship("Cart", back_populates="customer_carts")

    #ratings associated many to many
    grocery_ratings = db.relationship("Rating", back_populates="customer_ratings")

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)

    # represent the payment collected an employee (many to one relationship)
    payments_collected = db.relationship('Payment', backref='employee')
    checkouts = db.relationship('Order', backref='employee')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    deliveryDate = db.Column(db.DateTime)
    deliveryTown = db.Column(db.String(45), nullable=False)
    deliveryParish = db.Column(db.String(45), nullable=False)

    # represents the many-to-many relationship between  order and groceries
    groceries = db.relationship("OrderGroceries", back_populates="orders")

    # represents a one-to-one relationship between payment and order
    payment = db.relationship('Payment', backref=db.backref('order', uselist=False))

    # represents a one-to-many relationship between customers and orders
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    # represents a one to many-to-many relationship between employee and orders
    checkout_by = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)# unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(100), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10,2), nullable=False)

    #order associated many to many
    orders = db.relationship("OrderGroceries", back_populates="groceries")

    #cart associated many to many
    customer_carts = db.relationship("Cart", back_populates="cart_items")

    #ratings associated many to many
    customer_ratings = db.relationship("Rating", back_populates="grocery_ratings")

class OrderGroceries(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

    orders = db.relationship("Order", back_populates="groceries")
    groceries = db.relationship("Grocery", back_populates="orders")

class Cart(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Numeric(10,2), nullable=True)

    cart_items = db.relationship("Grocery", back_populates="customer_carts")
    customer_carts = db.relationship("Customer", back_populates="cart_items")

class Rating(db.Model):
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    grocery_ratings = db.relationship("Grocery", back_populates="customer_ratings")
    customer_ratings = db.relationship("Customer", back_populates="grocery_ratings")

class Payment(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('employee.id'))
    payment_date = db.Column(db.DateTime())
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)

