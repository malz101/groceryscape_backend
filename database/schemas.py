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

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

orderDetails = db.Table('order_details',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
)    

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    deliveryDate = db.Column(db.DateTime)
    
    # primary key
    customerId = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    foodItems = db.relationship('Food', secondary=orderDetails)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


if __name__ == "__main__":
    db.create_all()

