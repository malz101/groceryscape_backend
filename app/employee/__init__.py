from flask import Blueprint
from flask_restful import Api

employee_bp = Blueprint('employee',__name__, url_prefix="/")
employee_api = Api(employee_bp)