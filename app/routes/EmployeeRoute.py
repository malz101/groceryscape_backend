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
        return {'msg':'you are not logged in!', 'error':'auth-001'}, 401

@manage_employee_account.route('/login', methods=["POST", "GET"])
def login():
    employee = employee_manager.login(request)
    token = create_access_token(identity=employee)
    if employee:
        # logout if already logged into an account
        return {"token": token, "employee":employee}
    else:
        return {'error': 'employee not found'}
    
"""register an employee"""
@manage_employee_account.route('/register', methods=['GET','POST'])
@jwt_required()
def register():
    user = get_jwt_identity()
    if user and ('role' in user):
        if user['role'] == 'admin':
            employee = employee_manager.createEmployee(request)
            if employee:
                return employee
            else:
                return {'error': 'account was not created'}
        else:
            return {'msg':'only admin can perform this task'}
    else:
        return {'msg': 'you are not logged in as an employee'}

"""get employees"""
@manage_employee_account.route('/get_employees', methods=['GET','POST'])
@jwt_required()
def get_employees():
    user = get_jwt_identity()
    if user and ('role' in user):
        if user['role'] == 'admin':
            employees = employee_manager.getEmployees()
            return employees
        else:
            return {'msg':'only admin can perform this task'}
    else:
        return {'msg': 'you are not logged in as an employee'}

"""get employee"""
@manage_employee_account.route('/get_employee', methods=['GET','POST'])
@jwt_required()
def get_employee():
    user = get_jwt_identity()
    if user and ('role' in user):
        if user['role'] == 'admin':
            employee = employee_manager.getEmployee(request)
            return employee
        else:
            return {'msg':'only admin can perform this task'}
    else:
        return {'msg': 'you are not logged in as an employee'}

@manage_employee_account.route('/update_employee', methods=['POST','GET'])
@jwt_required()
def update_employee():

    user = get_jwt_identity()
    if user and ('role' in user):
        if user['role'] == 'admin':
            employee = employee_manager.updateEmployee(request)
            return employee
        else:
            return {'msg': 'only admin can perform this task'}
    else:
        return {'msg': 'you are not logged in as an employee'}

"""delete an employee"""
@manage_employee_account.route('/delete_employee', methods=['GET','POST'])
@jwt_required()
def delete_employee():
    user = get_jwt_identity()
    if user and ('role' in user):
        if user['role'] == 'admin':
            msg = employee_manager.deleteEmployee(request)
            return msg
        else:
            return {'msg': 'only admin can perform this task'}
    else:
        return {'msg': 'you are not logged in as an employee'}
    
@manage_employee_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'staff_id' in session:
        session.pop('staff_id', None)
    if 'admin_id' in session:
        session.pop('admin_id', None)
    return redirect(url_for('manage_employee_account.index'))