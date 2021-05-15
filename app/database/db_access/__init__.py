from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .CartAccess import CartAccess
from .CustomerAccess import CustomerAccess
from .EmployeeAccess import EmployeeAccess
from .GroceryAccess import GroceryAccess
from .OrderAccess import OrderAccess
from .PaymentAccess import PaymentAccess
from .RatingAccess import RatingAccess
from .DeliveryAccess import DeliveryAccess

cart_access = CartAccess(GroceryAccess(), OrderAccess(), CustomerAccess())
customer_access = CustomerAccess()
employee_access = EmployeeAccess()
grocery_access = GroceryAccess()
order_access = OrderAccess()
payment_access = PaymentAccess()
rating_access = RatingAccess(grocery_access,customer_access)
delivery_access = DeliveryAccess()

