from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
# from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from .sessions import CustomSession
from flask_migrate import Migrate
from .encrypter import Encrypter

db = SQLAlchemy()       #database object
mail = Mail()           #mail client object
# jwt = JWTManager()      #java web token manager object
cors = CORS()           #Cross-origin sharing object
csrf = CSRFProtect()    #csrf protection object
sess = CustomSession()        #session object for server-side sessions
encryp = Encrypter()     #encrypt object, object that does encryption
migrate = Migrate()