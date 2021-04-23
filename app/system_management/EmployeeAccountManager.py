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
                return self.__getEmployeeDetails(employee)
            else:
                return False
                
        except:
            return False

    def deleteEmployee(self, request):
        try:
            getParam = self.getRequestType(request)
            emp_id = getParam('emp_id')

            """sanitize email and password"""

            """get the employee's account"""
            employees = self.employee_access.deleteEmployee(int(emp_id))
            response = {}
            if employees:
                for employee in employees:
                    response[employee.id] = self.__getEmployeeDetails(employee)
                return response
            else:
                return {'msg': 'no employee found'}
        except:
            return {'msg':'failed request'}

    def login(self, request):

        try:
            getParam = self.getRequestType(request)
            email = getParam('email')
            password = getParam('password')

            """sanitize email and password"""

            """get the employee's account"""
            employee = self.employee_access.login(email, password)
            if employee:
                return  self.__getEmployeeDetails(employee)
            else:
                return False
        except:
            return False

    def getEmployee(self,request):
        try:
            getParam = self.getRequestType(request)
            empId = getParam('emp_id')

            employee = self.employee_access.getEmployee(int(empId))
            if employee:
                return self.__getEmployeeDetails(employee)
            else:
                return {'msg':'employee might be deleted'}
        except:
            return {'msg': 'failed request'}

    def getEmployees(self):

        try:
            employees = self.employee_access.getEmployees()
            response = {}
            if employees:
                for employee in employees:
                    response[employee.id] = self.__getEmployeeDetails(employee)
                return response
            else:
                return {'msg':'no employee found'}
        except:
            return {'msg':'request failed'}

    def updateEmployee(self, request):

        try:
            getParam = self.getRequestType(request)
            empId = getParam('emp_id')
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            employee = self.employee_access.updateEmployee(int(empId), attribute, value)
            if employee:
                return self.__getEmployeeDetails(employee)
            else:
                return {'msg':'update failed'}
        except:
            return {'msg':'request failed'}

    def __getEmployeeDetails(self, employee):

        return {"emp_id": employee.id, 'first_name': employee.first_name, 'last_name': employee.last_name, \
                         'email': employee.email,'password': employee.password, 'role': employee.role,\
                        'salary': float(employee.salary), 'address':employee.address}
            
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
