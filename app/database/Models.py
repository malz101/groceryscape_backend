from .. import db

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import Column, Integer, String, Table, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    gender = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    street = db.Column(db.String(45))
    town = db.Column(db.String(45), nullable=False)
    parish = db.Column(db.String(45), nullable=False)
    email_confirmed = db.Column(db.Boolean,nullable=False, default=False)

    orders = db.relationship('Order', back_populates='customer', cascade="all,delete")

    #cart associated many to many
    cart_items = db.relationship("Cart", back_populates="customer_carts", cascade="all,delete")

    #ratings associated many to many
    grocery_ratings = db.relationship("Rating", back_populates="customer_ratings", cascade="all,delete")


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    town = db.Column(db.String(200), nullable=False)
    parish = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)

    # represent the payment collected an employee (many to one relationship)
    payments_collected = db.relationship('CashPayment', back_populates='employee', cascade="all,delete")
    checkouts = db.relationship('Order', back_populates='employee', cascade="all,delete")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, index=True)
    orderdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_type = db.Column(db.String(40),nullable=True)
    status = db.Column(db.Enum('cancelled','delivered','checked out','pending',name='OrderStatus'), default='pending')
    deliverytimeslot = db.Column(db.Integer, db.ForeignKey('delivery_time_slot.id'), nullable=True)
    deliverydate = db.Column(db.Date)
    deliverystreet = db.Column(db.String(100))
    deliverytown = db.Column(db.String(100))
    deliveryparish = db.Column(db.String(100),db.ForeignKey('delivery_parish.parish'), default='None')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    checkout_by = db.Column(db.Integer, db.ForeignKey('employee.id'))# represents a one to many-to-many relationship between employee and orders

    customer = db.relationship('Customer', back_populates='orders')

    # represents the many-to-many relationship between  orders and groceries
    groceries = db.relationship("OrderGroceries", back_populates="orders", cascade="all,delete")

    # represents a one-to-one relationship between cash payment and order
    cash_payment = db.relationship('CashPayment', backref=db.backref('orders', uselist=False), cascade="all,delete")

    # represents a one-to-one relationship between card payment and order
    card_payment = db.relationship('CardPayment', backref=db.backref('orders', uselist=False), cascade="all,delete")

    # represents the one-to-many relationship between  orders and delivery_parish
    parish = db.relationship("DeliveryParish", back_populates="orders_in_parish")

    employee = db.relationship('Employee', back_populates='checkouts')

    timeslot = db.relationship('DeliveryTimeSlot', back_populates='orders')


class Grocery(db.Model):
    __tablename__ = 'grocery'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.UnicodeText(), nullable=False)# unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    units = db.Column(db.String(100), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    grams_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), default='grocery.jpg')
    sku = db.Column(db.String(50), unique=True, nullable=True)

    #order associated many to many
    orders = db.relationship("OrderGroceries", back_populates="groceries", cascade="all,delete")

    #cart associated many to many
    customer_carts = db.relationship("Cart", back_populates="cart_items", cascade = "all,delete")

    #ratings associated many to many
    customer_ratings = db.relationship("Rating", back_populates="grocery_ratings", cascade="all,delete")

    taxes = db.relationship("Taxes_on_goods", back_populates="grocery", cascade="all,delete")


class OrderGroceries(db.Model):
    __tablename__ = 'order_groceries'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    orders = db.relationship("Order", back_populates="groceries")
    groceries = db.relationship("Grocery", back_populates="orders")


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    cart_items = db.relationship("Grocery", back_populates="customer_carts")
    customer_carts = db.relationship("Customer", back_populates="cart_items")


class Rating(db.Model):
    __tablename__ = 'rating'
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    grocery_ratings = db.relationship("Grocery", back_populates="customer_ratings")
    customer_ratings = db.relationship("Customer", back_populates="grocery_ratings")


class CashPayment(db.Model):
    __tablename__ = 'cash_payment'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('employee.id'))
    payment_date = db.Column(db.DateTime,default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)

    employee = db.relationship('Employee', back_populates='payments_collected')


class CardPayment(db.Model):
    __tablename__ = 'card_payment'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    payment_date = db.Column(db.DateTime(),default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    intent_id = db.Column(db.String(100), unique=True, nullable = False)

    def __init__(self, order_id, amount, intent_id):
        self.order_id = order_id
        self.amount_tendered = amount
        self.intent_id = intent_id


class DeliveryParish(db.Model):
    __tablename__ = 'delivery_parish'
    parish = db.Column(db.String(45), primary_key=True)
    delivery_rate = db.Column(db.Numeric(10,2), nullable=False)

    orders_in_parish = db.relationship("Order", back_populates="parish")


class DeliveryTimeSlot(db.Model):
    __tablename__ = 'delivery_time_slot'
    id = db.Column(db.Integer, primary_key=True, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Boolean,nullable=False, default=True)

    orders = db.relationship("Order", back_populates="timeslot")

    def __init__(self,start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    
class MaxDeliveriesPerSlot(db.Model):
    __tablename__ = 'max_deliveries_per_slot'
    max_deliveries_per_time_slot = db.Column(db.Integer,primary_key=True, nullable=False)

class Taxes(db.Model):
    __tablename__ = 'taxes'
    tax = db.Column(db.String(50), nullable=False, primary_key=True)
    rate = db.Column(db.Numeric(10,2), nullable=False)

    groceries = db.relationship("Taxes_on_goods", back_populates="tax_type", cascade="all,delete")


class Taxes_on_goods(db.Model):
    __tablename__ = "taxes_on_goods"
    tax = db.Column(db.String, db.ForeignKey('taxes.tax'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True)

    grocery = db.relationship("Grocery", back_populates="taxes")
    tax_type = db.relationship("Taxes", back_populates="groceries")



#####################################################
#                       Views
####################################################

class ItemTotalRating(db.Model):
    __tablename__ = 'item_total_rating'
    item_id = db.Column(db.Integer, primary_key=True)
    total_rating = db.Column(db.Integer)
    num_customer = db.Column(db.Integer)
    coefficient = db.Column(db.Numeric(15,10))


class TotalQuantityPurchased(db.Model):
    __tablename__ = 'total_quantity_purchased'
    grocery_id = db.Column(db.Integer,db.ForeignKey('grocery.id'),primary_key=True)
    total = db.Column(db.Integer)


class CountPairs(db.Model):
    __tablename__ = 'count_pairs'
    item1 = db.Column(db.Integer, db.ForeignKey('grocery.id'),primary_key=True)
    item2 = db.Column(db.Integer,db.ForeignKey('grocery.id'), primary_key=True)
    count = db.Column(db.Integer)

class TotalAmountPurchased(db.Model):
    __tablename__ = 'total_amount_purchased'
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    grocery_id = db.Column(db.Integer,db.ForeignKey('grocery.id'), primary_key=True)
    total = db.Column(db.Integer)