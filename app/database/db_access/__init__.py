from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .CartAccess import CartAccess
from .CustomerAccess import CustomerAccess
from .EmployeeAccess import EmployeeAccess
from .GroceryAccess import GroceryAccess
from .OrderAccess import OrderAccess
from .OrderGroceriesAccess import OrderGroceriesAccess
from .PaymentAccess import PaymentAccess
from .RatingAccess import RatingAccess

cart_access = CartAccess(GroceryAccess(), OrderAccess(), CustomerAccess())
customer_access = CustomerAccess()
employee_access = EmployeeAccess()
grocery_access = GroceryAccess()
order_access = OrderAccess()
order_groceries_access = OrderGroceriesAccess(order_access,grocery_access,customer_access)
payment_access = PaymentAccess(order_access,order_groceries_access,employee_access)
rating_access = RatingAccess(grocery_access,customer_access)

