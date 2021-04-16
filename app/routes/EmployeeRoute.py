from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from ..system_management.EmployeeAccountManager import EmployeeAccountManager
from ..database.db_access import employee_access

"""All requests that are related to the management of an employee's account should come to this route"""
manage_employee_account = Blueprint("manage_employee_account", __name__)

"""create an object that manage all operations on an employee account"""
employee_manager = EmployeeAccountManager(employee_access)

"""admin index page"""
@manage_employee_account.route('/')
@manage_employee_account.route('/index')
def index():
    verify_jwt_in_request(optional=True)
    employee = get_jwt_identity()
    if employee:
        return employee
    else:
        return {'msg':'you are not logged in!'} 

@manage_employee_account.route('/login', methods=["POST", "GET"])
def login():
    employee = employee_manager.login(request)
    token = create_access_token(identity=employee)
    if employee:
        # logout if already logged into an account
        if 'staff_id' in session:
            session.pop('staff_id', None)
        if 'admin_id' in session:
            session.pop('admin_id', None)
            
        if employee['role'] == 'admin':
            session['admin_id'] = int(employee['id'])
        else:
            session['staff_id'] = int(employee['id'])
            
        return {"token": token, "employee":employee}
    else:
        return {'error': 'employee not found'}
    
"""register an employee"""
@manage_employee_account.route('/register', methods=['GET','POST'])
@jwt_required()
def register():
    user = get_jwt_identity()
    if user['role'] == 'admin':
        employee = employee_manager.createEmployee(request)
        if employee:
            if employee['role'] == 'admin':
                session['admin_id'] = int(employee['id'])
            else:
                session['staff_id'] = int(employee['id'])
            return employee
        else:
            return {'error': 'failed request'}
    else:
        return {'msg':'only admin can perform this task'}
    
@manage_employee_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'staff_id' in session:
        session.pop('staff_id', None)
    if 'admin_id' in session:
        session.pop('admin_id', None)
    return redirect(url_for('manage_employee_account.index'))