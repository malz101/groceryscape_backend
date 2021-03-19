from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .CartAccess import CartAccess
from .CustomerAccess import CustomerAccess
from .EmployeeAccess import EmployeeAccess
from .GroceryAccess import GroceryAccess
from .OrderAccess import OrderAccess
from .OrderGroceriesAccess import OrderGroceriesAccess
from .PaymentAccess import PaymentAccess

cart_access = CartAccess(GroceryAccess(), OrderAccess(), CustomerAccess())
customer_access = CustomerAccess()
employee_access = EmployeeAccess()
grocery_access = GroceryAccess()
order_access = OrderAccess()
order_groceries_access = OrderGroceriesAccess()
payment_access = PaymentAccess()