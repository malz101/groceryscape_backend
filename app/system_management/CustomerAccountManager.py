import os
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from .. import encrypter

class AccountManager:

    def __init__(self, customer_access, MLManager):
        self.MLManager = MLManager
        self.customer_access = customer_access

    def createAccount(self, request, mail,url_for, key, email_key):

        """extract details from the request"""
        getParam = self.getRequestType(request)
        
        data={
            'first_name': getParam('first_name'),
            'last_name': getParam('last_name'),
            'telephone': getParam('telephone'),
            'email': getParam('email'),
            'gender': getParam('gender'),
            'password': getParam('password'),
            'street': getParam('street'),
            'town': getParam('town'),
            'parish': getParam('parish')
        }
        print('data',data)
        """sanitize and verify details"""
        """create account with sanitized data"""
        customer = self.customer_access.registerCustomer(data)
        if customer:
            self.__sendConfirmationEmail(data['first_name'],data['email'], mail, url_for,key,email_key)
            return True
        return False

    def __sendConfirmationEmail(self,fname,email,mail,url_for, key, email_key):
        '''sends a confirmation email to user'''
        s = URLSafeTimedSerializer(key)
        salt = email_key
        token = s.dumps(email, salt=salt)
        link = url_for('customer.confirm_email', token=token, _external=True)

        msg = Message(recipients=[email])
        msg.subject = "Confirm Email"
        msg.body="""Dear {},\nPlease click the link below or copy and paste in address bar of browser.\n\n{}""".format(fname,link)
        # print('Mail obj',repr(mail))
        mail.send(msg)

    
    def confirmEmail(self,token,key):
        s = URLSafeTimedSerializer(key)
        salt = os.environ.get('EMAIL_CONFIRM_KEY')
        try:
            email = s.loads(token, salt=salt)
            result = self.customer_access.confirmEmail(email)
            
            if not result:
                return '<h1>Account Does not exist</h1>', 404
            return True
        except SignatureExpired:
            return '<h1>The token is expired!</h1>', 403
        except BadTimeSignature:
            '<h1>Token tampered with</h1>', 401

    def login(self, request):

        getParam = self.getRequestType(request)
        data={
            'email' : getParam('email'),
            'password' : getParam('password')
        }
        print('Data',data)
        
        """sanitize email and password"""

        """get the customer's account"""
        customer = self.customer_access.login(data)
        if customer:
            return {
                "cust_id": str(customer.id),
                'first_name': encrypter.decrypt(customer.first_name),
                'last_name': encrypter.decrypt(customer.last_name),
                'telephone': encrypter.decrypt(customer.telephone),
                'town': encrypter.decrypt(customer.town),
                'street': encrypter.decrypt(customer.street),
                'email_confirmed': customer.email_confirmed,
                'parish': encrypter.decrypt(customer.parish)
            }
        return False

    def getCustomer(self, customerId):

        customer = self.customer_access.getCustomerById(int(customerId))
        if customer:
            return self.__getCustomerDetails(customer)
        return False


    def updateAccount(self, request, user):

        getParam = self.getRequestType(request)
        customerId = user['cust_id']
        attribute = getParam('attribute')
        value = getParam('value')

        '''validate and sanitize data'''
        
        '''perform update'''
        customer = self.customer_access.updateAccount(int(customerId), attribute, value)
        if customer:
            return self.__getCustomerDetails(customer)
        return False


    def getRecommendedGroceries(self, custId):
        groceries = ''
        if self.customer_access.getCustomerById(custId):
            groceries = self.MLManager.getRecommendGroceries(custId)
            if groceries:
                return groceries
            return []
        raise NameError


    def __getCustomerDetails(self, customer):

        return {
            "cust_id": str(customer.id),
            'first_name': encrypter.decrypt(customer.first_name),
            'last_name': encrypter.decrypt(customer.last_name),
            'telephone': encrypter.decrypt(customer.telephone), 
            'email': encrypter.decrypt(customer.email), 
            'gender': encrypter.decrypt(customer.gender),
            'street': encrypter.decrypt(customer.street),
            'town': encrypter.decrypt(customer.town),
            'parish': encrypter.decrypt(customer.parish)
        }

                
    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
