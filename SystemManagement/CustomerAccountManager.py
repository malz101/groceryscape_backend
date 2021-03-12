from database.CustomerAccess import CustomerAccess

class AccountManager:

    def __init__(self, customer_access):

        self.customer_access = customer_access

    def createAccount(self, request):

        """extract details from the request"""

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        telephone = request.form['telephone']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']
        town = request.form['town']
        parish = request.form['parish']
        # dob = request.form['dob']

        """sanitize and verify details"""

        """create account with sanitized data"""
        customer = self.customer_access.registerCustomer(firstName, lastName, telephone, email, gender, password, town, parish)
        if customer:
            return customer
        else:
            return {'error': 'Failed to create customer account'}

    def loginToAccount(self, request):

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            """sanitize email and password"""

            """get the customer's account"""
            customer = self.customer_access.getCustomer(email, password)
            if customer:
                return customer
            else:
                return False

    def logoutOfAccount(self):
        pass

    def updateAccount(self):
        pass