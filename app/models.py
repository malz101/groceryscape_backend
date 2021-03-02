from . import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    town = db.Column(db.String(45), nullable=False)
    parish = db.Column(db.String(45), nullable=False)

    def getCustomer(self, email, password):
        customer = Customer.query.filter(email == email).first()
        # customer = db.session.query().filter(Customer.email == email).first()
        return customer.firstName

    orders = db.relationship('Order', backref='customer')
    
    def __init__(self,firstName, lastName, email, password, address, town, parish ):
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.password=password
        self.address=address
        self.town=town
        self.parish=parish

    def __repr__(self):
        return '<Customer %r>' % self.username

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return '<Employee %r>' % self.username    

orderDetails = db.Table('order_details',
                db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
                db.Column('item_id', db.Integer, db.ForeignKey('food.id'), primary_key=True))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    deliveryDate = db.Column(db.DateTime)
    
    # primary key
    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    foodItems = db.relationship('Food', secondary=orderDetails)
    
    def __repr__(self):
        return '<Order %r>' % self.username

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)#, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

    def __init__(self,name,description, quantity, price):
        self.name=name
        self.description=description
        self.quantity=quantity
        self.price=price

    def __repr__(self):
        return '<Food %r>' % self.username
