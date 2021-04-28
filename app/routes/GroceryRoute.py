from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.GroceryManager import GroceryManager
from ..database.db_access import grocery_access

"""This blueprint will handle all requests related to the management of groceries"""
manage_groceries = Blueprint("manage_groceries", __name__)

"""object used to manipulate all grocery operations"""
grocery_manager = GroceryManager(grocery_access)

@manage_groceries.route('/create_grocery')
@jwt_required()
def create_grocery():
    user = get_jwt_identity()
    if user and ('role' in user):
        return render_template('adminViews/create_grocery.html')
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/submit_grocery', methods=['POST','GET'])
@jwt_required()
def submit_grocery():
    user = get_jwt_identity()
    if user and ('role' in user):
        newGrocery = grocery_manager.addGrocery(request)
        return newGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/update_grocery', methods=['POST','GET'])
@jwt_required()
def update_grocery():

    user = get_jwt_identity()
    if user and ('role' in user):
        updatedGrocery = grocery_manager.updateGrocery(request)
        return updatedGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/delete_grocery', methods=['POST','GET'])
@jwt_required()
def delete_grocery():

    user = get_jwt_identity()
    if user and ('role' in user):
        groceries = grocery_manager.deleteGrocery(request)
        return groceries
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/get_groceries', methods=['POST','GET'])
def get_groceries():
    try:
        groceries = grocery_manager.getGroceries(request)
        if groceries:
            response = {'msg':'success', 'data':{'groceries':groceries}}, 200
        else:
            response = {'msg':'No groceries Found', 'data':{'groceries':{}}}, 200
    except Exception as e:
        print(e)
        response = {'msg': 'sorry request failed', 'error':'ise-0001'}, 500
    finally:
        return response



@manage_groceries.route('/get_groceries_by_category', methods=['POST','GET'])
def get_groceries_by_category():
    try:
        groceries = grocery_manager.getGroceriesByCategory(request)
        if groceries:
            response = {'msg':'success', 'data':{'groceries':groceries}}, 200
        else:
            response = {'msg':'No groceries of that category found', 'data':{'groceries':{}}}, 200
    except Exception as e:
        print(e)
        response = {'msg': 'sorry request failed', 'error':'ise-0001'}, 500
    finally:
        return response

@manage_groceries.route('/get_grocery', methods=['POST','GET'])
def get_grocery():
    try:
        grocery = grocery_manager.getGrocery(request)
        if grocery:
            reponse = {'msg':'success', 'data': {'grocery':grocery}}, 200
        else:
            response = {'msg':'Grocery not found', 'data': {'grocery':{}}}, 200
    except Exception as e:
        print(e)
        response = {'msg':'', 'error':'ise-0001'}, 500
    finally:
        return response