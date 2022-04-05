import os
import datetime
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    DB_ENCRYPTION_KEY = os.environ.get('DB_ENCRYPTION_KEY')
    DB_ENCRYPTION_SALT = os.environ.get('DB_ENCRYPTION_SALT')
    EMAIL_CONFIRM_KEY = os.environ.get('EMAIL_CONFIRM_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'Som3$ec5etK*y'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                        'mysql+mysqlconnector://root:@localhost/food_delivery'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './uploads'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '25'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY= os.environ.get('STRIPE_SECRET_KEY')
    # STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')
    
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    SESSION_KEY_PREFIX = os.environ.get('SESSION_KEY_PREFIX')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=31) #31 days
    SESSION_USE_SIGNER = os.environ.get('SESSION_USE_SIGNER')
    from redis import Redis
    SESSION_REDIS = Redis(
        host=os.environ.get('REDIS_HOST'),
        port=os.environ.get('REDIS_PORT'), 
        #password='password'
    )
    WTF_CSRF_SECRET_KEY = SECRET_KEY #Random data for generating secure tokens. If this is not set then SECRET_KEY is used.
    WTF_CSRF_TIME_LIMIT = int(os.environ.get('WTF_CSRF_TIME_LIMIT')) #Number of seconds that the token is valid
    WTF_CSRF_METHODS = (os.environ.get('WTF_CSRF_METHODS')).split(',') #HTTP methods to protect from CSRF.
    WTF_CSRF_HEADERS = (os.environ.get('WTF_CSRF_HEADERS')).split(',') #HTTP headers to search for CSRF token when it is not provided in the form
    WTF_CSRF_FIELD_NAME = os.environ.get('WTF_CSRF_FIELD_NAME') #Key where token is stored in session for comparison.
        
class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE')