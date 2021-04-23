from flask import Blueprint
from flask import redirect, url_for, session, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.RatingManager import RatingManager
from ..database.db_access import order_access
from ..database.db_access import rating_access

manage_rating = Blueprint("manage_rating", __name__)

rating_manager = RatingManager(rating_access)

@manage_rating.route('/rate_grocery', methods=['POST','GET'])
@jwt_required()
def rate_grocery():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        rating = rating_manager.rateGrocery(user, request)
        return rating
    else:
        return redirect(url_for('index'))

@manage_rating.route('/data_frame', methods=['POST','GET'])
@jwt_required()
def data_frame():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        rating = rating_manager.getDataFrame()
        return str(rating)
    else:
        return redirect(url_for('index'))