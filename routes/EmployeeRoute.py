from flask import Blueprint
from flask import redirect, url_for, session, request, render_template
from SystemManagement.EmployeeAccountManager import EmployeeAccountManager

"""All requests that are related to the management of an employee's account should come to this route"""
manage_employee_account = Blueprint("manage_employee_account", __name__)

"""create an object that manage all operations on an employee account"""
employee_manager = EmployeeAccountManager()

"""admin index page"""
@manage_employee_account.route('/')
@manage_employee_account.route('/index')
def index():
    if 'staff_id' in session:
        return render_template('adminViews/admin_home.html', user=session['emp_id'])
    if 'admin_id' in session:
        return render_template('adminViews/admin_home.html', user=session['admin_id'])
    else:
        return render_template('adminViews/admin_login.html')

@manage_employee_account.route('/login', methods=["POST"])
def login():
    emp_id, role = employee_manager.login(request)
    if emp_id and role == 'staff':
        session['staff_id'] = emp_id
        return render_template("adminViews/admin_home.html", user=emp_id)
    elif emp_id and role == 'admin':
        session['admin_id'] = emp_id
        return render_template("adminViews/admin_home.html", user=emp_id)
    else:
        return redirect(url_for('manage_employee_account.index'))

"""register an employee"""
@manage_employee_account.route('/register', methods=['POST'])
def register():
    """Pass all the responsibility of creating an account to the account manager"""
    if 'admin_id' in session:
        emp_id = employee_manager.createEmployee(request)
        if emp_id:
            return redirect(url_for('manage_employee_account.index'))
        else:
            return redirect(url_for('manage_employee_account.index'), error='ERROR')
    else:
        return redirect(url_for('manage_employee_account.index'))

"""request to create a new employee account"""
@manage_employee_account.route('/create_employee')
def create_employee():
    if 'admin_id' in session:
        return render_template('adminViews/admin_add_employee.html')
    else:
        return redirect(url_for('manage_employee_account.index'))


@manage_employee_account.route('/logout', methods=["GET", "POST"])
def logout():
    if 'staff_id' in session:
        session.pop('staff_id', None)
    if 'admin_id' in session:
        session.pop('admin_id', None)
        return redirect(url_for('manage_employee_account.index'))
    else:
        return redirect(url_for('manage_employee_account.index'))