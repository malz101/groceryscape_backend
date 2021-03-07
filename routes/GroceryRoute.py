from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from SystemManagement.GroceryManager import GroceryManager

"""This blueprint will handle all requests related to the management of groceries"""
manage_groceries = Blueprint("manage_groceries", __name__)

"""object used to manipulate all grocery operations"""
grocery_manager = GroceryManager()

@manage_groceries.route('/create_grocery')
def create_grocery():
    if 'admin_id' in session or 'staff_id' in session:
        return render_template('adminViews/create_grocery.html')
    else:
        return redirect(url_for('manage_employee_account.index'))

@manage_groceries.route('/submit_grocery', methods=['POST'])
def submit_grocery():

    if 'staff_id' in session or 'admin_id' in session:
        new_grocery = grocery_manager.addGrocery(request)
        return render_template('adminViews/admin_new_grocery.html', grocery_details=new_grocery)
    else:
        return redirect(url_for('manage_employee_account.index'))

