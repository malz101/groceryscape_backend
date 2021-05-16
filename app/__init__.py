from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from .config import DevelopmentConfig
import logging
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)
mail = Mail(app)
app.config.from_object(DevelopmentConfig)
uploaddir = app.config['UPLOAD_FOLDER']
jwt = JWTManager(app)
db = SQLAlchemy(app)
from app import routes