from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from .config import DevelopmentConfig
import logging
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
mail = Mail(app)
uploaddir = app.config['UPLOAD_FOLDER']
jwt = JWTManager(app)
db = SQLAlchemy(app)
# print('MAIL_USERNAME', app.config['MAIL_USERNAME'])
# print('MAIL_PASSWORD', app.config['MAIL_PASSWORD'])
# print('MAIL_PORT', app.config['MAIL_PORT'])
# print('MAIL_SERVER', app.config['MAIL_SERVER'])
# print('MAIL_DEFAULT_SENDER', app.config['MAIL_DEFAULT_SENDER'])
from app import routes