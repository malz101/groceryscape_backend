import random
from faker import Faker
import pandas as pd
import re
import os
from datetime import datetime
from app.database.Models import Cart,Customer,Employee,Grocery,Order,OrderGroceries,\
    CashPayment,Rating, DeliveryParish, DeliveryTimeSlot
from app import db, encrypter
from sqlalchemy.exc import IntegrityError

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

        self.orderStatus = ['pending','served','checked out','cancelled']

    def populateCustomers(self):
        '''populate customer table with test data'''
        Faker.seed(0)
        for _ in range(self.NUMBER_OF_CUSTOMERS):

            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            telephone = self.fake.phone_number()
            email = self.fake.safe_email()
            password = self.fake.password()
            street = self.fake.street_address()
            town = self.fake.city()
            parish = self.__selectParish()
            gender = self.__selectGender()
            

            customer = Customer(first_name, last_name, telephone, email, gender, password,street, town, parish)
            db.session.add(customer)
            db.session.commit()
            line = str(customer.id)+", "+first_name+", "+last_name+", "+telephone+", "+email+", "+gender+\
                ", "+password+", "+street+", "+town+", "+parish+"\n"
            f = open("./misc/db_data/customers.txt", "a")
            f.write(line)
            f.close()

            print("Added {} {}".format(first_name,last_name))

    def populateEmployee(self):
        '''populate employee table with test data'''
        Faker.seed(0)
        for _ in range(self.NUMBER_OF_EMPLOYEES):
            first_name = self.fake.first_name()
            last_name = self.fake.last_name()
            email = self.fake.safe_email()
            telephone = self.fake.phone_number()
            password = self.fake.password()
            street = self.fake.street_address()
            town = self.fake.city()
            parish = self.__selectParish()

            role = self.__getRole()
            salary = round(random.uniform(100000, 200000), 2)

            employee = Employee(first_name, last_name, telephone, email, password, street, town, parish, role, salary)
            db.session.add(employee)
            db.session.commit()
            line = str(employee.id)+", "+first_name+", "+last_name+", "+email+", "+password+", "+street+\
                ", "+town+", "+parish+","+role+", "+str(float(salary))+", "+telephone+"\n"

            f = open("./misc/db_data/employees.txt", "a")
            f.write(line)
            f.close()
            print("Added {} {}".format(first_name, last_name))

    def populateGroceries(self):
        '''populate groery table test data'''
        Faker.seed(0)
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
        '''populate orders table with test data'''
        customers = Customer.query.all()
        timeslots = DeliveryTimeSlot.query.all()
        parishes = DeliveryParish.query.all()
        Faker.seed(0)
        for _ in range(self.NUMBER_OF_ORDERS):
            customer = random.choice(customers)
            timeslot = random.choice(timeslots)
            parish = DeliveryParish.query.filter_by(parish=customer.parish).first()
            billing_fname = delivery_fname = encrypter.decrypt(customer.first_name)
            billing_lname = delivery_lname = encrypter.decrypt(customer.last_name)
            billing_street = delivery_street = encrypter.decrypt(customer.street)
            billing_town = delivery_town = encrypter.decrypt(customer.town)
            billing_parish = delivery_parish = encrypter.decrypt(parish.parish)
            delivery_date = '2021-5-'+str(random.randint(26,28))
            delivery_timeslot_start = str(timeslot.start_time)
            delivery_timeslot_end = str(timeslot.end_time)
            delivery_fee = parish.delivery_rate
            payment_type = 'cash'
            customer_id = customer.id
            notes = self.fake.sentence()

            
            order = Order(customer_id,billing_fname, billing_lname, billing_street,billing_town,billing_parish,\
                    delivery_fname,delivery_lname,delivery_date,delivery_timeslot_start,delivery_timeslot_end,\
                    delivery_street,delivery_town,delivery_parish,delivery_fee,payment_type, notes)

            db.session.add(order)
            db.session.commit()

            line = str(order.id)+", "+str(customer_id)+", "+billing_fname+", "+ billing_lname+", "+ billing_street+\
                ", "+billing_town+", "+billing_parish+", "+delivery_fname+", "+delivery_lname+", "+\
                str(delivery_date)+", "+str(delivery_timeslot_start)+", "+str(delivery_timeslot_end)+", "+\
                delivery_street+", "+delivery_town+", "+delivery_parish+", "+str(float(delivery_fee))+", "+\
                payment_type+", "+ notes+"\n"
            
            f = open("./misc/db_data/orders.txt", "a")
            f.write(line)
            f.close()
            print("Order {} for customer {} added".format(str(order.id),customer_id))


    def populateOrderGroceries(self):
        '''populate order groceries table with test data'''
        orders = Order.query.all()
        groceries = Grocery.query.all()
        for order in orders:
            for groc in random.choices(groceries,k=random.randint(1,10)):
                
                order_id = order.id
                grocery_id = groc.id
                quantity = random.randint(1,5)

                total_tax=0
                for tax_on_grocery in groc.taxes:
                    total_tax += groc.cost_per_unit*tax_on_grocery.tax_.rate*quantity
                try:
                    orderGrocery = OrderGroceries(order_id,grocery_id,quantity,groc.sku,groc.cost_per_unit,total_tax)
                    db.session.add(orderGrocery)
                    db.session.commit()
                    line = str(order.id)+", "+str(groc.id)+", "+str(quantity)+", "+groc.sku+", "+\
                        str(float(orderGrocery.unit_price))+", "+str(float(orderGrocery.total_tax))+"\n"

                    f = open("./misc/db_data/order_groceries.txt", "a")
                    f.write(line)
                    f.close()
                    print("grocery {} in quantity {} added for order {}".format(str(groc.id),str(quantity),str(order.id)))
                
                except IntegrityError:
                    db.session.rollback()

    def populateDeliveryParish(self):

        for parish in self.parishes:
            new_parish = DeliveryParish(parish,round(random.uniform(500, 3500), 2))
            db.session.add(new_parish)
            db.session.commit()

            line = str(new_parish.id)+", "+parish+", "+ str(float(new_parish.delivery_rate))+"\n"
            f = open("./misc/db_data/parishes.txt", "a")
            f.write(line)
            f.close()
            print("{} added with rate {}".format(str(encrypter.decrypt(new_parish.parish)),str(float(new_parish.delivery_rate))))        

        new_parish = DeliveryParish('None',0.00)
        db.session.add(new_parish)
        db.session.commit()
        line = str(new_parish.id)+", "+str(encrypter.decrypt(new_parish.parish))+", "+ str(float(new_parish.delivery_rate))+"\n"
        f = open("./misc/db_data/parishes.txt", "a")
        f.write(line)
        f.close()
        print("{} added with rate {}".format('None',str(float(new_parish.delivery_rate))))          


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



# if __name__ =='__main__':

    # pd = PopulateDatabase()
    # pd.populateCustomers()
    # pd.populateEmployee()
    # pd.populateGroceries()
    # pd.populateDeliveryParish()
    # pd.populateOrder()
    # pd.populateOrderGroceries()
    # pd.populateRating()