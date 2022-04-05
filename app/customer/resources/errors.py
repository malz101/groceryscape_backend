from email import message
from werkzeug.exceptions import HTTPException
from itsdangerous import SignatureExpired, BadTimeSignature
from wtforms import ValidationError

class InternalServerError(HTTPException):
    pass

class SchemaValidationError(HTTPException):
    pass

class DeletingCustomerError(HTTPException):
    pass

class ProductNotAvailableError(HTTPException):
    pass

class ProductNotExistsError(HTTPException):
    pass

class NoProductExistsError(HTTPException):
    pass

class NoRatingExistsError(HTTPException):
    pass

class RatingNotExistsError(HTTPException):
    pass

class EmailAlreadyExistsError(HTTPException):
    pass

class EmailDoesNotExistsError(HTTPException):
    pass

class EmailNotConfirmedError(HTTPException):
    pass

class UnauthenticatedError(HTTPException):
    pass

class AuthenticationError(HTTPException):
    pass

class CSRFTokenAlreadyExistsError(HTTPException):
    pass

class CreateAccountWhileAuthenticatedError(HTTPException):
    pass

class CartItemAlreadyExistsError(HTTPException):
    pass

class CartItemNotExistsError(HTTPException):
    pass

class OrderNotExistsError(HTTPException):
    pass

class NoOrderExistsError(HTTPException):
    pass

class CreateOrderError(HTTPException):
    pass

errors = {
    'InternalServerError': {
        'message': 'Server Error',
        'status': 500,
        'description': 'Something went wrong'
    },
     'SchemaValidationError': {
         'message': 'Schema Error',
         'status': 400,
         'description': 'Request is missing required fields'
     },
     'DeletingCustomerError': {
         "message": "Deleting movie added by other is forbidden",
         "status": 403
     },
     'NoProductExistsError': {
         'message': 'Product Error',
         'status': 422,
         'description': 'No product matching the criteria has been found.'
     },
     'ProductNotExistsError': {
         'description': 'Product with given id doesn\'t exists',
         'status': 422,
         'message': 'Product Error'
     },
     'ProductNotAvailableError': {
         'description': 'Product with given id doesn\'t is not currently available',
         'status': 422,
         'message': 'Product Error'
     },
     'ProductNotExistsError': {
         'message': 'Product Error',
         'status': 422,
         'description': 'No products found.'
     },
     'NoRatingExistsError': {
         'message': 'RatingError',
         'status': 422,
         'description': 'Customer has no previous rating for this product.'
     },
     'RatingNotExistsError': {
         'message': 'RatingError',
         'status': 422,
         'description': 'Customer has no previous rating for any product.'
     },
     'CreateAccountWhileAuthenticatedError': {
         'message': 'Resource Creation Error',
         'status': 422,
         'description': 'User is currently logged in. Cannot create an acconnt while user is logged in.'
     },
     'EmailAlreadyExistsError': {
         'description': 'User with given email address already exists',
         'status': 422,
         'message': 'Resource Creation Error'
     },
    'EmailDoesNotExistsError': {
         'description': 'User with given email address does not exists',
         'status': 422,
         'message': 'Customer Error'
     },
     'EmailNotConfirmedError': {
         'message': 'Authentication Error',
         'status': 401,
         'description': 'Email needs to be verified to access this endpoint',
     },
     'AuthenticationError': {
         'description': "Invalid username or password",
         'status': 401,
         'message': 'Authentication Error'
     },
     'UnauthenticatedError': {
         'message': 'User not logged in.',
         'status': 401,
         'description': 'Please log in or create an account.'
     },
     'SignatureExpired':{
         'message': 'TokenError',
         'status': 403,
         'description': 'The token is expired!',
     },
     'BadTimeSignature': {
         'message': 'TokenError',
         'status': 401,
         'description': 'Token bas been tampered with!',
     },
     'CSRFTokenAlreadyExistsError': {
         'description': 'CSRF token is already assigned to this session.',
         'status': 422,
         'message': 'CSRF Token Error'
     },
    'ValidationError': {
        'description': 'CSRF token either invalid, expired, missing or does not match. Request a new token.',
        'status': 400,
        'message': 'CSRF Token Error'
    },
    'CartItemAlreadyExistsError': {
        'message': 'Cart Error',
        'status': 422,
        'description': 'Item is already in cart.'
    },
    'CartItemNotExistsError': {
        'message': 'Cart Error',
        'status': 422,
        'description': 'Product with given id is not in cart.'
    },
    'OrderNotExistsError': {
        'message': 'Order Error',
        'status': 422,
        'description': 'Order with given id does not exists.'
    },
    'NoOrderExistsError': {
        'description': 'No order matching the criteria has been found.',
        'status': 422,
        'message': 'Product Error'
    },
    'CreateOrderError': {
        'message': 'Resource Create Error',
        'status': 422,
        'description': 'Order could not be created.'
    }
}