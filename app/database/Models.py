from .. import db, encrypter
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Table, Numeric, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

# Base = declarative_base()


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.LargeBinary, nullable=False)
    last_name = db.Column(db.LargeBinary, nullable=False)
    telephone = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.LargeBinary, nullable=False, unique=True)
    gender = db.Column(db.LargeBinary, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    street = db.Column(db.LargeBinary)
    town = db.Column(db.LargeBinary, nullable=False)
    parish = db.Column(db.LargeBinary, nullable=False)
    email_confirmed = db.Column(db.Boolean,nullable=False, default=True)

    #relationships
    orders = db.relationship('Order', back_populates='customer', passive_deletes=True)
    cart_items = db.relationship("Cart", back_populates="customer_carts", passive_deletes=True)
    ratings = db.relationship("Rating", back_populates="customer", passive_deletes=True)

    def __init__(self, first_name, last_name, telephone, email, gender, password,street, town, parish):
        self.first_name = encrypter.encrypt(first_name)
        self.last_name = encrypter.encrypt(last_name)
        self.telephone = encrypter.encrypt(telephone)
        self.gender = encrypter.encrypt(gender)
        self.email = encrypter.encrypt(email)
        self.password = encrypter.encrypt(generate_password_hash(password, method='pbkdf2:sha256:310000'))
        self.street = encrypter.encrypt(street)
        self.town = encrypter.encrypt(town)
        self.parish = encrypter.encrypt(parish)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.LargeBinary, nullable=False)
    last_name = db.Column(db.LargeBinary, nullable=False)
    telephone = db.Column(db.LargeBinary, nullable=True)
    email = db.Column(db.LargeBinary, nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)
    street = db.Column(db.LargeBinary, nullable=False)
    town = db.Column(db.LargeBinary, nullable=False)
    parish = db.Column(db.LargeBinary, nullable=False)
    role = db.Column(db.LargeBinary, nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)

    # represent the payment collected an employee (many to one relationship)
    payments_collected = db.relationship('CashPayment', back_populates='employee', passive_deletes=True)
    checkouts = db.relationship('Order', back_populates='employee', passive_deletes=True)


    def __init__(self, first_name, last_name, telephone, email, password, street, town, parish, role, salary):
        self.first_name = encrypter.encrypt(first_name)
        self.last_name = encrypter.encrypt(last_name)
        self.telephone = encrypter.encrypt(telephone)
        self.email = encrypter.encrypt(email)
        self.password = encrypter.encrypt(generate_password_hash(password, method='pbkdf2:sha256:310000'))
        self.street = encrypter.encrypt(street)
        self.town = encrypter.encrypt(town)
        self.parish = encrypter.encrypt(parish)
        self.role = encrypter.encrypt(role)
        self.salary = salary


class Grocery(db.Model):
    __tablename__ = 'grocery'
    id = db.Column(db.Integer, primary_key=True, index=True)
    brand = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.UnicodeText(), nullable=False)# unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(100), nullable=False)
    cost_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    grams_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    photo = db.Column(db.String(100), default='grocery.jpg')
    sku = db.Column(db.String(50), unique=True, nullable=True)
    package_type = db.Column(db.String(50), nullable=True)

    __table_args__ = (db.UniqueConstraint('name', 'size', name='_grocery_name_size_uc'),)
    # relationships (referenced by)
    orders = db.relationship("OrderGroceries", back_populates="groceries")
    customer_carts = db.relationship("Cart", back_populates="cart_items", passive_deletes=True)
    ratings = db.relationship("Rating", back_populates="grocery", passive_deletes=True)
    taxes = db.relationship("TaxesOnGrocery", back_populates="grocery", passive_deletes=True)

    #relationships (references)
    # category = db.relationship("Category", back_populates="categories")
    # variants = db.relationship('GroceryVariant', back_populates='grocery', passive_deletes=True)


    def __init__(self,brand, name, description,quantity,size, unit_price, weight, category_id,photo,\
                    sku,package_type):
        self.brand = brand
        self.name = name
        self.description = description
        self.quantity = quantity
        self.size = size
        self.cost_per_unit = unit_price
        self.grams_per_unit = weight
        self.category_id = category_id
        self.photo = photo
        self.sku = sku
        self.package_type = package_type


# class Category(db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True, index=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     status = db.Column(db.Boolean,nullable=False, default=True)

#     # relationships (referenced by)
#     groceries = db.relationship('Grocery', back_populates='category')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, index=True)
    orderdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.LargeBinary,nullable=False,default=encrypter.encrypt('pending'))
    payment_type = db.Column(db.LargeBinary,nullable=False)
    billing_first_name = db.Column(db.LargeBinary, nullable=False)
    billing_last_name = db.Column(db.LargeBinary, nullable=False)
    billing_street = db.Column(db.LargeBinary, nullable=False)
    billing_town = db.Column(db.LargeBinary, nullable=False)
    billing_parish = db.Column(db.LargeBinary, nullable=False)
    delivery_first_name = db.Column(db.LargeBinary, nullable=False)
    delivery_last_name = db.Column(db.LargeBinary, nullable=False)
    delivery_timeslot_start = db.Column(db.Time, nullable=False)    
    delivery_timeslot_end = db.Column(db.Time, nullable=False) 
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_street = db.Column(db.LargeBinary, nullable=False)
    delivery_town = db.Column(db.LargeBinary, nullable=False)
    delivery_parish = db.Column(db.LargeBinary, nullable=False)
    delivery_fee = db.Column(db.Numeric(10,2), nullable=False)
    delivered_time = db.Column(db.DateTime, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), nullable=False)
    checkout_by = db.Column(db.Integer, db.ForeignKey('employee.id',ondelete='SET NULL'), nullable=True)# represents a one to many-to-many relationship between employee and orders
    notes = db.Column(db.LargeBinary, nullable=True)

    # relationship (references)
    customer = db.relationship('Customer', back_populates='orders')
    # parish = db.relationship("DeliveryParish", back_populates="orders")
    employee = db.relationship('Employee', back_populates='checkouts')
    # timeslot = db.relationship('DeliveryTimeSlot', back_populates='orders')

    # relationships (referenced by)
    groceries = db.relationship("OrderGroceries", back_populates="orders",passive_deletes=True)
    cash_payment = db.relationship('CashPayment', back_populates='order', passive_deletes=True)
    card_payment = db.relationship('CardPayment', back_populates='order', passive_deletes=True)

    def __init__(self, customer_id,billing_fname, billing_lname, billing_street,billing_town,billing_parish,\
                    delivery_fname,delivery_lname,delivery_date,delivery_timeslot_start,delivery_timeslot_end,\
                    delivery_street,delivery_town,delivery_parish,delivery_fee,payment_type, notes):
        self.customer_id = customer_id
        self.billing_first_name = encrypter.encrypt(billing_fname)
        self.billing_last_name = encrypter.encrypt(billing_lname)
        self.billing_street = encrypter.encrypt(billing_street)
        self.billing_town = encrypter.encrypt(billing_town)
        self.billing_parish = encrypter.encrypt(billing_parish)
        self.delivery_first_name = encrypter.encrypt(delivery_fname)
        self.delivery_last_name = encrypter.encrypt(delivery_lname)
        self.delivery_date = datetime.strptime(delivery_date,'%Y-%m-%d').date()
        self.delivery_timeslot_start = datetime.strptime(delivery_timeslot_start,'%H:%M:%S').time()
        self.delivery_timeslot_end = datetime.strptime(delivery_timeslot_end,'%H:%M:%S').time()
        self.delivery_street = encrypter.encrypt(delivery_street)
        self.delivery_town = encrypter.encrypt(delivery_town)
        self.delivery_parish = encrypter.encrypt(delivery_parish)
        self.delivery_fee = delivery_fee
        self.payment_type = encrypter.encrypt(payment_type)
        if not notes is None:
            self.notes = encrypter.encrypt(notes)


class OrderGroceries(db.Model):
    __tablename__ = 'order_groceries'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='CASCADE'), primary_key=True, index=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id'), primary_key=True,index=True)
    sku = db.Column(db.String(50),nullable=True)
    unit_price = db.Column(db.Numeric(10,2))
    total_tax = db.Column(db.Numeric(10,2))
    quantity = db.Column(db.Integer)

    # relationships 
    orders = db.relationship("Order", back_populates="groceries")
    groceries = db.relationship("Grocery", back_populates="orders")

    def __init__(self, order_id, grocery_id,quantity, sku, unit_price, total_tax):
        self.order_id = order_id
        self.grocery_id = grocery_id
        self.quantity = quantity
        self.sku = sku
        self.unit_price = unit_price
        self.total_tax = total_tax


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), primary_key=True, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id',ondelete='CASCADE'), primary_key=True, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # relationships (references)
    cart_items = db.relationship("Grocery", back_populates="customer_carts")
    customer_carts = db.relationship("Customer", back_populates="cart_items")

    def __init__(self, cart_id, item_id):
        self.cart_id = cart_id
        self.item_id = item_id
        self.quantity = quantity


class Rating(db.Model):
    __tablename__ = 'rating'
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('grocery.id',ondelete='CASCADE'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # relationships
    grocery = db.relationship("Grocery", back_populates="ratings")
    customer = db.relationship("Customer", back_populates="ratings")


class CashPayment(db.Model):
    __tablename__ = 'cash_payment'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='CASCADE'), primary_key=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='SET NULL'))
    payment_time = db.Column(db.DateTime,default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)

    # relatioships
    employee = db.relationship('Employee', back_populates='payments_collected')
    order = db.relationship('Order', back_populates='cash_payment')

    def __init__(self, order_id,recorded_by, amount_tendered, change):
        self.order_id = order_id
        self.recorded_by = recorded_by
        self.amount_tendered = amount_tendered
        self.change = change


class CardPayment(db.Model):
    __tablename__ = 'card_payment'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='CASCADE'), primary_key=True)
    payment_time = db.Column(db.DateTime(),default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    intent_id = db.Column(db.String(100), unique=True, nullable = False)

    order = db.relationship('Order', back_populates='card_payment')

    def __init__(self, order_id, amount, intent_id):
        self.order_id = order_id
        self.amount_tendered = amount
        self.intent_id = encrypter.encrypt(intent_id)


class DeliveryParish(db.Model):
    __tablename__ = 'delivery_parish'
    id = db.Column(db.Integer, primary_key=True)
    parish = db.Column(db.LargeBinary, unique=True)
    delivery_rate = db.Column(db.Numeric(10,2), nullable=False)

    # orders = db.relationship("Order", back_populates="parish")

    def __init__(self,parish,delivery_rate):
        self.parish = encrypter.encrypt(parish)
        self.delivery_rate = delivery_rate


class DeliveryTimeSlot(db.Model):
    __tablename__ = 'delivery_time_slot'
    id = db.Column(db.Integer, primary_key=True, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    # is_active = db.Column(db.Boolean,nullable=False, default=True)

    # orders = db.relationship("Order", back_populates="timeslot")

    def __init__(self,start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    
class Miscellaneous(db.Model):
    __tablename__ = 'miscellaneous'
    name = db.Column(db.String(50),primary_key=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)


class Taxes(db.Model):
    __tablename__ = 'taxes'
    tax = db.Column(db.String(20), nullable=False, primary_key=True)
    rate = db.Column(db.Numeric(10,2), nullable=False)

    # relationships
    grocery_ids_on_tax = db.relationship("TaxesOnGrocery", back_populates="tax_", passive_deletes=True)


class TaxesOnGrocery(db.Model):
    __tablename__ = "taxes_on_goods"
    tax = db.Column(db.String(20), db.ForeignKey('taxes.tax', ondelete='CASCADE'), primary_key=True)
    grocery_id = db.Column(db.Integer, db.ForeignKey('grocery.id',ondelete='CASCADE'), primary_key=True)

    # relationships
    grocery = db.relationship("Grocery", back_populates="taxes")
    tax_ = db.relationship("Taxes", back_populates="grocery_ids_on_tax")

    def __init__(self, tax, grocery_id):
        self.tax = tax
        self.grocery_id = grocery_id


#####################################################
#                       Views                       #
#####################################################

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