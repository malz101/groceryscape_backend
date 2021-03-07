from database.EmployeeAccess import EmployeeAccess
class EmployeeAccountManager:

    def createEmployee(self, request):

        """extract details from the request"""

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        role = request.form['role']
        salary = request.form['salary']
        branch_work = request.form['branch_work']

        """sanitize and validate details"""

        """create account with sanitized data"""
        employee = EmployeeAccess().registerEmployee(firstName, lastName, email, password, address, role, float(salary), branch_work)
        return employee.id

    def login(self, request):

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            """sanitize email and password"""

            """get the customer's account"""
            employee = EmployeeAccess().getEmployee(email, password)

            if employee:
                return employee.id, employee.role
            else:
                return False, False
