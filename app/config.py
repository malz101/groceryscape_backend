import os
import datetime

class Config(object):
    """Base Config Object"""
    defaults = {}

    defaults['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    defaults['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'Som3$ec5etK*y'
    defaults['JWT_ACCESS_TOKEN_EXPIRES'] = 1
    defaults['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                        'mysql+mysqlconnector://root:@localhost/food_delivery'
    defaults['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    defaults['UPLOAD_FOLDER'] = './uploads'
    defaults['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'localhost'
    defaults['MAIL_PORT'] = os.environ.get('MAIL_PORT') or '25'
    defaults['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    defaults['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    defaults['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    defaults['MAIL_USE_TLS'] = True
    defaults['MAIL_USE_SSL'] = False
    # defaults['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY')
    # defaults['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
    # defaults['STRIPE_ENDPOINT_SECRET'] = os.environ.get('STRIPE_ENDPOINT_SECRET')

    # Reads the config file if it exists
    try:
        conf = open('./app/groceryscape.conf')
        for c in conf.readlines():
            param, val = c.strip().split(' = ', 1)
            defaults[param] = val
    except FileNotFoundError:
        pass

    SECRET_KEY = defaults['SECRET_KEY']
    JWT_SECRET_KEY = defaults['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = defaults['SQLALCHEMY_DATABASE_URI']
    UPLOAD_FOLDER = defaults['UPLOAD_FOLDER']
    MAIL_SERVER = defaults['MAIL_SERVER']
    MAIL_PORT = defaults['MAIL_PORT']
    MAIL_USERNAME = defaults['MAIL_USERNAME']
    MAIL_PASSWORD = defaults['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = defaults['MAIL_DEFAULT_SENDER']
    # STRIPE_PUBLIC_KEY = defaults['STRIPE_PUBLIC_KEY']
    # STRIPE_SECRET_KEY = defaults['STRIPE_SECRET_KEY']
    # STRIPE_ENDPOINT_SECRET = defaults['STRIPE_ENDPOINT_SECRET']

    try:
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=int(defaults['JWT_ACCESS_TOKEN_EXPIRES']))
    except ValueError:
        raise Exception('JWT_ACCESS_TOKEN_EXPIRES must be a number')

    try:
        SQLALCHEMY_TRACK_MODIFICATIONS = bool(defaults['SQLALCHEMY_TRACK_MODIFICATIONS'])
    except ValueError:
        raise Exception('JWT_ACCESS_TOKEN_EXPIRES must be either True/False (case sensitive)')

    try:
        MAIL_USE_TLS = bool(defaults['MAIL_USE_TLS'])
    except ValueError:
        raise Exception('JWT_ACCESS_TOKEN_EXPIRES must be either True/False (case sensitive)')

    try:
        MAIL_USE_SSL = bool(defaults['MAIL_USE_SSL'])
    except ValueError:
        raise Exception('JWT_ACCESS_TOKEN_EXPIRES must be either True/False (case sensitive)')

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    FLASK_ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
