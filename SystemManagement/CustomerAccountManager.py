from database.CustomerAccess import CustomerManager

class AccountManager:

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
        cm = CustomerManager()
        customer = cm.registerCustomer(firstName, lastName, telephone, email, gender, password, town, parish)
        return customer.id

    def loginToAccount(self, request):

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            """sanitize email and password"""

            """get the customer's account"""
            customer = CustomerManager().getCustomer(email, password)


            if customer:
                return customer.id, customer.firstName
            else:
                return False

    def logoutOfAccount(self):
        pass

    def updateAccount(self):
        pass