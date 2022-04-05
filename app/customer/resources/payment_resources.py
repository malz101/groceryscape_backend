from flask_login import login_required
from flask_restful import Resource
from flask import current_app, session, request, redirect, url_for,  render_template
from ..common.decorators import login_required

class PaymentApi(Resource):
    @login_required
    def get(self):
        #get payment details
        pass

    @login_required
    def post(self):
        #pay
        pass


class PaymentKeyApi(Resource):
    @login_required
    def get(self):
        pass