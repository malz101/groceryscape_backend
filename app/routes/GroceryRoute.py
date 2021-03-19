from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from ..system_management.GroceryManager import GroceryManager
from ..database.db_access import grocery_access

"""This blueprint will handle all requests related to the management of groceries"""
manage_groceries = Blueprint("manage_groceries", __name__)

"""object used to manipulate all grocery operations"""
grocery_manager = GroceryManager(grocery_access)

@manage_groceries.route('/create_grocery')
def create_grocery():
    if 'admin_id' in session or 'staff_id' in session:
        return render_template('adminViews/create_grocery.html')
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/submit_grocery', methods=['POST','GET'])
def submit_grocery():

    if 'staff_id' in session or 'admin_id' in session:
        newGrocery = grocery_manager.addGrocery(request)
        return newGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/update_grocery', methods=['POST','GET'])
def update_grocery():

    if 'staff_id' in session or 'admin_id' in session:
        updatedGrocery = grocery_manager.updateGrocery(request)
        return updatedGrocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/delete_grocery', methods=['POST','GET'])
def delete_grocery():

    if 'staff_id' in session or 'admin_id' in session:
        groceries = grocery_manager.deleteGrocery(request)
        return groceries
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/get_grocery', methods=['POST','GET'])
def get_grocery():

    if 'staff_id' in session or 'admin_id' in session:
        grocery = grocery_manager.getGrocery(request)
        return grocery
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/get_groceries', methods=['POST','GET'])
def get_groceries():

    if 'staff_id' in session or 'admin_id' in session:
        groceries = grocery_manager.getGroceries(request)
        return groceries
    else:
        return redirect(url_for('manage_employee_account.index'))