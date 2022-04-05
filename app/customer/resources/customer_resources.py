from flask_restful import Resource
from flask import current_app, jsonify, session, request, redirect, url_for,  render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app.customer.common.decorators import login_required, logout_required
from app.service import customer_access
from app.schemas import CustomerSchema
from app import mail
# from app.customer import customer_api
from .errors import DeletingCustomerError, EmailAlreadyExistsError, InternalServerError
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
# from werkzeug.datastructures import ImmutableMultiDict
# from werkzeug.wsgi import LimitedStream
# import io


class CustomerApi(Resource):
    @login_required
    def get(self):
        """
        CustomerApi GET method. Retrieves all players found in the Football
        Stats database, unless the id path parameter is provided. If this id
        is provided then the player with the associated player_id is retrieved.

        :param id: Player ID to retrieve, this path parameter is optional
        :ret
        passs
        """
        customer = customer_access.get_customer(session['customer_id'])
        customer_schema = CustomerSchema()
        response = jsonify(customer_schema.dump(customer))
        response.status_code = 200
        return response
    
    @logout_required
    def post(self):
        """
        CustomerApi POST method. Adds a new Customer to the database.

        :return: Customer.customer_id, 201 HTTP status code.
        """
        try:
            create_customer_schema = CustomerSchema(exclude=('id', 'is_active', 'time_created', 'email_confirmed'))
            new_customer_data = create_customer_schema.load(request.json) #use marshmellow to verify schema
            customer = customer_access.create_customer(new_customer_data)
            if customer:
                sendConfirmationEmail(customer.first_name,customer.email)
                customer_schema = CustomerSchema()
                response = jsonify(customer_schema.dump(customer))
                response.status_code = 201
                
                '''login user after they create account. I tried the method below but it didn't work as
                the 307 status code means the client browser sends back the initial request before redirect. This produces an
                invalid schema error as the login endpoint is not expecting any other fields except email and password.
                Hence the onus is now on the frontend to manually send the request to the login the user.'''
                # print('data:', request.get_data(cache=False)) #flush the cache of the current request.stream, if not the previous resquest.stream with be used on redirect request
                # print('dict:',request.get_data())
                # new_request_data = {'email': new_customer_data['email'], 'password': new_customer_data['password']}
                # new_request_data_json = json.dumps(new_request_data, indent=2).encode('utf-8') #convert dictionary to json object
                # new_request_data_stream = io.BytesIO(new_request_data_json) #create buffered io object to read json data
                # request.stream = LimitedStream(new_request_data_stream,len(new_request_data_json)) # convert to werkzeug.wsgi.LimitedStream object (a wrapper for (IO[bytes]), this is flask stores the request stream
                # response = redirect(url_for('customer.login'), code=307) #blueprint name + endpoint, 303 mandating the change of request type to GET, and 307 preserving the request type as originally sent.


            else:
                raise InternalServerError
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        except IntegrityError:
            raise EmailAlreadyExistsError
        return response


    @login_required
    def patch(self):
        try:
            update_customer_schema = CustomerSchema(exclude=('id', 'is_active', 'time_created', 'email_confirmed'), partial=True)

            customer_new_data = update_customer_schema.load(request.json, partial=True)

            customer = customer_access.update_customer(session['customer_id'], customer_new_data)

            if customer:
                customer_schema = CustomerSchema()
                response = jsonify(customer_schema.dump(customer))
                response.status_code = 201
            else:
                raise InternalServerError
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status            
        return response


    # @login_required
    # def delete(self):
    #     customer = customer_access.delete_customer(customer_id=session['customer_id'])

    #     if customer:
    #         response = jsonify(serialize_customer(customer)), 201
    #         response.status_code = 200
    #     else:
    #         raise DeletingCustomerError
        
    #     return response



###########----------Helper Functions--------##########

def sendConfirmationEmail(fname,email):
    '''sends a confirmation email to user'''
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    salt = current_app.config['EMAIL_CONFIRM_KEY']
    token = s.dumps(email, salt=salt)
    link = url_for('customer.confirm-email', token=token, _external=True) #blueprint name + endpoint
    msg = Message(recipients=[email])
    msg.subject = 'Confirm Email Address'
    msg.body=(
        f"Dear {fname},\n"
        f"Please click the link below or copy and paste in address bar of browser.\n\n"
        f"{link}"
    )
    # print('Mail obj',repr(mail))
    mail.send(msg)