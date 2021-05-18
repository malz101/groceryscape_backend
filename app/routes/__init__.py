import os
from app import app
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

"""import blueprints (routes) for different sections of the system"""
from .CustomerRoute import manage_customer_account
from .EmployeeRoute import manage_employee_account
from .GroceryRoute import manage_groceries
from .CartRoute import manage_cart
from .RatingRoute import manage_rating
from .OrderRoute import manage_order
from app.system_management.MLManager import MLManager

from app.database.db_access import customer_access,rating_access,grocery_access,order_access,\
                                    delivery_access, cart_access


from ..system_management.CustomerAccountManager import AccountManager
account_manager = AccountManager(customer_access, MLManager(customer_access, order_access, rating_access, cart_access))


"""register blueprints"""
app.register_blueprint(manage_customer_account, url_prefix="/manage_customer_account")
app.register_blueprint(manage_employee_account, url_prefix="/manage_employee_account")
app.register_blueprint(manage_groceries, url_prefix="/manage_groceries")
app.register_blueprint(manage_cart, url_prefix="/manage_cart")
app.register_blueprint(manage_rating, url_prefix="/manage_rating")
app.register_blueprint(manage_order, url_prefix="/manage_order")



"""serves the index page for users"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # return app.send_static_file('index.html')
    return render_template('index.html')



@app.route('/get_parish/<parish>', methods=['GET'])
@jwt_required()
def get_parish(parish):
    try:
        parish = delivery_access.getDeliveryParish(parish)
        if parish:
            # print('Parish',parish.parish)
            response = {'msg':'success', 'data':{'parish':{'name':str(parish.parish), 'delivery_fee':float(parish.delivery_rate)}}}, 200
        else:
            response = {'msg':'unsuccessful', 'error':'notfound-0001'}, 404
    except Exception as e:
        print(e)
        reponse = {'msg':'', 'error':'ise-0001'}, 500
    finally:
        return response


@app.route('/get_delivery_timeslots', methods=['GET'])
@jwt_required()
def get_delivery_timeslots():
    try:
        timeslots = delivery_access.getDeliveryTimeSlots()
        if timeslots:
            result=[]
            for timeslot in timeslots:
                result.append({
                    'id':str(timeslot.id),
                    'start_time':str(timeslot.start_time),
                    'end_time':str(timeslot.end_time)
                })
            response = {'msg':'success', 'data':{'timeslots':result}}, 200
        else:
            response = {'msg':'unsuccessful', 'error':'notfound-0001'}, 404
    except Exception as e:
        print(e)
        response = {'msg':'', 'error':'ise-0001'}, 500
    finally:
        return response


@app.route('/get_parishes', methods=['GET'])
@jwt_required()
def get_parishes():
    try:
        parishes = delivery_access.getDeliveryParishes()
        if parishes:
            result=[]
            for parish in parishes:
                result.append({'name':str(parish.parish), 'delivery_fee':float(parish.delivery_rate)})
            response = {'msg':'success', 'data':{'parishes':result}}, 200
        else:
            response = {'msg':'unsuccessful', 'error':'notfound-0001'}, 404
    except Exception as e:
        print(e)
        reponse = {'msg':'', 'error':'ise-0001'}, 500
    finally:
        return response


@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir,app.config['UPLOAD_FOLDER']), filename)


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
# @app.route("/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     return {"access_token": access_token}, 200

