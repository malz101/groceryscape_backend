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
    if user:
        return render_template('adminViews/create_grocery.html')
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/submit_grocery', methods=['POST','GET'])
@jwt_required()
def submit_grocery():
    user = get_jwt_identity()
    if user:
        newGrocery = grocery_manager.addGrocery(request)
        return newGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/update_grocery', methods=['POST','GET'])
@jwt_required()
def update_grocery():

    user = get_jwt_identity()
    if user:
        updatedGrocery = grocery_manager.updateGrocery(request)
        return updatedGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/delete_grocery', methods=['POST','GET'])
@jwt_required()
def delete_grocery():

    user = get_jwt_identity()
    if user:
        groceries = grocery_manager.deleteGrocery(request)
        return groceries
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/get_groceries', methods=['POST','GET'])
def get_groceries():
    groceries = grocery_manager.getGroceries(request)
    return groceries