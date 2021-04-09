import random
from faker import Faker
import pandas as pd
import re
import os
import datetime
from app.database.Models import Cart
from app.database.Models import Customer
from app.database.Models import Employee
from app.database.Models import Grocery
from app.database.Models import Order
from app.database.Models import OrderGroceries
from app.database.Models import Payment
from app.database.Models import Rating
from app import db

class PopulateDatabase:

    def __init__(self):
        self.fake = Faker()
        self.NUMBER_OF_CUSTOMERS = 50
        self.NUMBER_OF_EMPLOYEES = 10
        self.NUMBER_OF_GROCERIES = 500
        self.NUMBER_OF_ORDERS = 200

        self.parishes = ['Kingston','St. Mary','St. Thomas','St. Ann','Clarendon','St. James','Trelawny','Portland',\
                       'St. Andrew','Manchester','St. Elizabeth','Westmoreland','Hanover','St. Catherine']
        self.genders = ['Male','Female']
        self.roles = ['admin','staff']
        self.units = ['gill','teaspoon','tablespoon','ounce','cup', 'pint','quart', 'gallon', 'ml','litre',\
                      'lb','mg','g', 'dl']

        self.orderStatus = ['PENDING','SERVED','CHECKED OUT','CANCELED']

    def populateCustomers(self):

        for _ in range(self.NUMBER_OF_CUSTOMERS):

            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            telephone = self.fake.phone_number()
            email = self.fake.safe_email()
            password = self.fake.password()
            town = self.fake.city()

            gender = self.__selectGender()
            parish = self.__selectParish()

            customer = Customer(first_name=first_name,last_name=last_name,telephone=telephone,email=email,gender=gender,\
                     password=password,town=town,parish=parish)
            db.session.add(customer)
            db.session.commit()

            print("Added {} {}".format(first_name,last_name))

    def populateEmployee(self):

        for _ in range(self.NUMBER_OF_EMPLOYEES):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            email = self.fake.safe_email()
            password = self.fake.password()
            address = self.fake.address()

            role = self.__getRole()
            salary = round(random.uniform(100000, 200000), 2)

            employee = Employee(first_name=first_name, last_name=last_name, email=email, password=password, address=address,\
                                role=role, salary=salary)
            db.session.add(employee)
            db.session.commit()

            print("Added {} {}".format(first_name, last_name))

    def populateGroceries(self):

        for _ in range(self.NUMBER_OF_GROCERIES):
            name = self.fake.name()
            description = self.fake.sentence()
            quantity = random.randint(1,20)
            units = self.__getUnit()
            cost_per_unit = round(random.uniform(10, 100), 2)

            grocery = Grocery(name=name, description=description, quantity=quantity, units=units, \
                              cost_per_unit=cost_per_unit)
            db.session.add(grocery)
            db.session.commit()

            print("Added {} to stock".format(name))

    def populateOrder(self):

        for _ in range(self.NUMBER_OF_ORDERS):
            deliveryDate = datetime.datetime(2021,4,1)
            deliveryTown = self.fake.city()
            deliveryParish = self.__selectParish()
            customer_id = random.randint(5,self.NUMBER_OF_CUSTOMERS)

            order = Order(deliveryDate=deliveryDate, deliveryTown=deliveryTown, deliveryParish=deliveryParish, \
                          customer_id=customer_id)
            db.session.add(order)
            db.session.commit()

            print("Order for customer {}".format(customer_id))

    def populateOrderGroceries(self):

        for order in range(3, self.NUMBER_OF_ORDERS + 3):

            for groc in self.__getRanGroceries(self.NUMBER_OF_GROCERIES):

                order_id = order
                grocery_id = groc
                quantity = random.randint(1,10)
                price = round(random.uniform(10, 100), 2)

                orderGrocery = OrderGroceries(order_id=order_id,grocery_id=grocery_id,quantity=quantity,price=price)
                db.session.add(orderGrocery)
                db.session.commit()
                print(" order {}".format(order))


    def populateRating(self):

        for customer in range(3,self.NUMBER_OF_CUSTOMERS+1):
            for grocery in range(5,self.NUMBER_OF_GROCERIES+3):
                cust_id = customer
                item_id = grocery
                rating = random.randint(1,10)
                ratings = Rating(cust_id=cust_id, item_id=item_id, rating=rating)
                db.session.add(ratings)
                db.session.commit()
                print("customer {} rated grocery {}: {} points".format(cust_id,item_id,rating))


    def populatePayment(self):
        pass

    def __selectParish(self):
        return self.parishes[random.randint(0, len(self.parishes)-1)]

    def __selectGender(self):
        return self.genders[random.randint(0, len(self.genders)-1)]

    def __getRole(self):
        return self.roles[random.randint(0, len(self.roles)-1)]

    def __getUnit(self):
        return self.roles[random.randint(0, len(self.roles) - 1)]

    def __getOrderStatus(self):
        return self.orderStatus[random.randint(0, len(self.orderStatus) - 1)]

    def __getRanGroceries(self, num_of_groceries):
        return random.sample(range(5, num_of_groceries), 7)



if __name__ =='__main__':

    pd = PopulateDatabase()
    # pd.populateCustomers()
    # pd.populateEmployee()
    # pd.populateGroceries()
    # pd.populateOrder()
    # pd.populateOrderGroceries()
    pd.populateRating()