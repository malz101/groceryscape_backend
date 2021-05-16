import os
import datetime

class Config(object):
    """Base Config Object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'Som3$ec5etK*y'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:''@localhost/food_delivery'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './uploads'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '25'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    # STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    # STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')


class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    FLASK_ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
