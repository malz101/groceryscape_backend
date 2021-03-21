from flask import Blueprint
from flask import redirect, url_for, session, request
from ..system_management.RatingManager import RatingManager
from ..database.db_access import order_access
from ..database.db_access import rating_access

manage_rating = Blueprint("manage_rating", __name__)

rating_manager = RatingManager(rating_access)

@manage_rating.route('/rate_grocery', methods=['POST','GET'])
def rate_grocery():
    if 'cust_id' in session:
        rating = rating_manager.rateGrocery(session, request)
        return rating
    else:
        return redirect(url_for('index'))
