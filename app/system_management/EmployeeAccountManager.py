class EmployeeAccountManager:
    def __init__(self, employee_access):
        self.employee_access = employee_access
        
    def createEmployee(self, request):


        try:
            getParam = self.getRequestType(request)
            firstName = getParam('first_name')
            lastName = getParam('last_name')
            email = getParam('email')
            password = getParam('password')
            address = getParam('address')
            role = getParam('role')
            salary = getParam('salary')

            """sanitize and validate details"""

            """create account with sanitized data"""
            employee = self.employee_access.registerEmployee(firstName, lastName, email, password, address, role, float(salary))
            if employee:
                return {"id": str(employee.id), 'first_name': employee.first_name, 'last_name': employee.last_name, \
                         'email': employee.email,'password': employee.password, 'role': employee.role,\
                        'salary': str(employee.salary), 'address':employee.address}
            else:
                return False
                
        except:
            return False
        
    def login(self, request):

        try:
            getParam = self.getRequestType(request)
            email = getParam('email')
            password = getParam('password')

            """sanitize email and password"""

            """get the employee's account"""
            employee = self.employee_access.login(email, password)
            if employee:
                return  {"id": str(employee.id), 'first_name': employee.first_name, 'last_name': employee.last_name, \
                         'email': employee.email,'password': employee.password, 'role': employee.role,\
                        'salary': str(employee.salary), 'address':employee.address}
            else:
                return False
        except:
            return False

    def getEmployee(self,empId):
        try:
            employee = self.employee_access.getEmployee(empId)
            if employee:
                return {"id": str(employee.id), 'first_name': employee.first_name, 'last_name': employee.last_name, \
                         'email': employee.email,'password': employee.password, 'role': employee.role,\
                        'salary': str(employee.salary), 'address':employee.address}
            else:
                return {'msg':'employee might be deleted or updated'}
        except:
            return {'msg': 'failed request'}
            
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
