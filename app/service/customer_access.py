from app import db,encryp
from app.database.models import Customer

import os
from flask_sqlalchemy import get_debug_queries

def create_customer(new_customer_data:dict):
    """creates a customer record"""
    customer = Customer(**new_customer_data)
    db.session.add(customer)
    db.session.commit()
    return customer

    
def confirm_email(email):
    '''updates email_confirmed field of customer with email to true'''
    result = Customer.query.where(Customer._email == encryp.encrypt(email)).update(dict(email_confirmed=True))
    #result = str(Customer.query.where(Customer._email == encryp.encrypt(email)).update(dict(email_confirmed=True)))
    # info = get_debug_queries()[0]
    # print(info.statement,info.parameters,info.duration,sep='\n')
    return result


def get_customer(customer_id=None, email=None):
    '''get a customer by email or id'''
    
    if customer_id:
        customer = Customer.query.where(Customer.id==customer_id).one()
    elif email:
        customer = Customer.query.where(Customer._email == encryp.encrypt(email)).one()
    else:
        customer = None

    return customer


def email_exist(email: str) -> bool:
    pass


def update_customer(customer_id, new_customer_data):
    customer = get_customer(customer_id)
    if customer:
        for attribute, value in new_customer_data.items():
            match attribute:
                case 'first_name':
                    customer.first_name = value
                case 'last_name':
                    customer.last_name = value
                case 'telephone':
                    customer.telephone = value
                case 'email':
                    customer.email = value
                    #customer.email_confirmed = false #might want dem to reconfirm email
                case 'password':
                    customer.password = value
                case 'gender':
                    customer.gender = value
                case 'street':
                    customer.street = value
                case 'town':
                    customer.town = value
                case 'parish':
                    customer.parish = value
                case 'is_active':
                    customer.is_active = value
        db.session.commit()
    return customer


# def delete_customer_data(customer_id=None, email=None):
#     '''Deactivates customers account'''
#     if customer_id:
#         customer = get_customer(customer_id=customer_id)
#     elif email:
#         customer = get_customer(email=email)
#     else:
#         customer =  None

#     if customer:
#         customer.is_active = False
#     return customer
