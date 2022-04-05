from functools import wraps
from flask import g, request, session, jsonify
from flask_session import sessions
from ..resources.errors import UnauthenticatedError, EmailNotConfirmedError, CreateAccountWhileAuthenticatedError

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            raise UnauthenticatedError
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            raise CreateAccountWhileAuthenticatedError
        return f(*args, **kwargs)
    return decorated_function


def email_verification_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email_confirmed'):
            raise EmailNotConfirmedError
        return f(*args, **kwargs)
    return decorated_function