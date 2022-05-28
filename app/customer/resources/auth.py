from app import csrf
from app.service import customer_access, cart_access
from app.schemas import CustomerSchema
from ..common.decorators import login_required
from .errors import InternalServerError,AuthenticationError, EmailDoesNotExistsError, CSRFTokenAlreadyExistsError


from flask_restful import Resource
from flask import current_app, session, redirect, request, jsonify
from flask_wtf.csrf import generate_csrf, validate_csrf
from wtforms import ValidationError
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer
from marshmallow import ValidationError


class LoginApi(Resource):
    def get(self):
        if session.get('logged_in'):
            response = jsonify({'login': True})
            response.status_code = 200
        else:
            response = jsonify({'login': False})
            response.status_code = 200
        return response

    def post(self):
        try:
            login_schema = CustomerSchema(only=('email', 'password'))
            data = login_schema.load(request.json)
            customer = customer_access.get_customer(email=data['email'])
            if customer and check_password_hash(customer.password, data['password']):
                # #regenerate session to prevent session fixation attack
                # current_app.session_interface.regenerate_session(session) #moved to app wide app.util.decorators
                #create new session values
                session['logged_in'] = True
                session['customer_id'] = customer.id
                session['email_confirmed'] = customer.email_confirmed
                # cart_lst = cart_access.get_carts(customer_id=customer.id,statuses=('shopping')) #should return a list wirh a single cart
                # cart = cart_lst[0] if cart_lst else cart_access.create_cart(customer.id) #customers should only have one shopping cart
                # session['cart_id'] = cart.id
                response = jsonify({'message' : 'login success'})
                response.status_code = 200
                #generate new csrf token for logged in session
                generate_csrf_token(response)
            else:
                raise AuthenticationError
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status            
        return response
        


class LogoutApi(Resource):
    @login_required
    def get(self):
        pass
    
    @login_required
    def post(self):
        if not session.clear():
            response = jsonify({'message' : 'logout success'})
            response.status_code = 200
            return response
        raise InternalServerError


class ConfirmEmailApi(Resource):
    @csrf.exempt
    def get(self,token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        salt = current_app.config['EMAIL_CONFIRM_KEY']

        email = s.loads(token, salt=salt)
        if customer_access.confirm_email(email):
            return redirect('http://localhost:8080/login')
        raise EmailDoesNotExistsError


class CSRFTokenApi(Resource):
    @csrf.exempt
    def get(self):
        if not session.get(current_app.config.get('WTF_CSRF_FIELD_NAME')):
            response = jsonify({'message': 'CSRF Header set'})
            response.status_code = 200
            generate_csrf_token(response)
        else: #csrf token in session

            for header_name in current_app.config.get('WTF_CSRF_HEADERS', []):
                if request.headers.get(header_name):
                    token_to_validate = request.headers[header_name]
                    try:
                        validate_csrf(token_to_validate)
                        raise CSRFTokenAlreadyExistsError #if no errors and csrf token in session, cannot reset csrf token
                    except ValidationError as e:
                        cause = str(e)
                        print(cause)
                        if cause == "The CSRF tokens do not match.":
                            response = jsonify({'message': 'TokenError', 'description': cause+" Terminating session, please re-login!"})
                            response.status_code = 400
                            session.clear()
                            break
            else: #if break not executed
                response = jsonify({'message': 'CSRF Header set'})
                response.status_code = 200
                generate_csrf_token(response) 
            
        return response


def generate_csrf_token(response):
    """Generates a new csrf token and binds it to the session.
    Token is also bound to response header so that client can 
    store it.
    """
    token = generate_csrf() #creates csf token and set session variable with the csrf token with key 'csrf_token'
    # session['csrf_token'] = token
    response.headers.set("X-CSRFToken",token) 
    # return token