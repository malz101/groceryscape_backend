import os
import datetime

class Config(object):
    """Base Config Object"""

    # initialized with defaults
    configs = {'DEBUG': False, \
            'SECRET_KEY': 'Som3$ec5etK*y', \
            'JWT_SECRET_KEY': 'Som3$ec5etK*y', \
            'JWT_ACCESS_TOKEN_EXPIRES': 1, \
            'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://root:@localhost/food_delivery', \
            'SQLALCHEMY_TRACK_MODIFICATIONS': False, \
            'UPLOAD_FOLDER': './uploads'}

    try:
        fptr = open('./app/groceryscape.conf')
        lines = fptr.readlines()
        for l in lines:
            # Filters out comments and blank lines
            if ((l != '') and (l[0] != '#')):
                try:
                    var, val = l.strip().split(' = ', 1)
                    configs[var] = val
                except KeyError:
                    raise Exception('Invalid configuration: ' + l)
                except ValueError:
                    raise Exception('Invalid configuration: ' + l)
    except (FileNotFoundError):
        pass

    try:
        DEBUG = bool(configs['DEBUG'])
        SECRET_KEY = os.environ.get('SECRET_KEY') or configs['SECRET_KEY']
        JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or configs['JWT_SECRET_KEY']
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=int(configs['JWT_ACCESS_TOKEN_EXPIRES']))
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or configs['SQLALCHEMY_DATABASE_URI']
        SQLALCHEMY_TRACK_MODIFICATIONS = bool(configs['SQLALCHEMY_TRACK_MODIFICATIONS'])
        UPLOAD_FOLDER = configs['UPLOAD_FOLDER']
    except ValueError:
        raise Exception('One of the configurations has an invalid value')

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
