import redis
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from .config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from .encrypt import Encrypt
import logging
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
# CORS(app)
mail = Mail(app)
cors = CORS(app, resources={r"/*": {"origins": ["https://groceryscape.web.app","https://groceryscape-admin.web.app"]}})
# csrf = CSRFProtect(app)
uploaddir = app.config['UPLOAD_FOLDER']
encrypter = Encrypt(app.config['DB_ENCRYPTION_KEY'],app.config['DB_ENCRYPTION_SALT'])
db = SQLAlchemy(app)
# print('MAIL_USERNAME', app.config['MAIL_USERNAME'])
# print('MAIL_PASSWORD', app.config['MAIL_PASSWORD'])
# print('MAIL_PORT', app.config['MAIL_PORT'])
# print('MAIL_SERVER', app.config['MAIL_SERVER'])
# print('MAIL_DEFAULT_SENDER', app.config['MAIL_DEFAULT_SENDER'])
jwt = JWTManager(app)
# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )

# # Callback function to check if a JWT exists in the redis blocklist
# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header, jwt_payload):
#     jti = jwt_payload["jti"]
#     token_in_redis = jwt_redis_blocklist.get(jti)
#     return token_in_redis is not None


from app import routes