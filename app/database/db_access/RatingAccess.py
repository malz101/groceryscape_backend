from ... import db
from ..Models import Rating, Grocery, Customer
from sqlalchemy import create_engine
import pymysql
import  pandas as pd
import os

class RatingAccess:

    def __init__(self, groceryAccess, customerAccess):
        self.groceryAccess = groceryAccess
        self.customerAccess = customerAccess

    def rateGrocery(self, custId, itemId, myRating):

        grocery = self.groceryAccess.searchForGrocery(itemId)
        customer = self.customerAccess.getCustomerById(custId)

        if grocery and customer:
            currentRating = self.getRating(custId, itemId)
            if currentRating:
                if myRating < 0:
                    myRating = 0
                currentRating.rating = myRating
                db.session.commit()
                return self.getRating(custId, itemId)
            else:
                rating = Rating(cust_id=custId, item_id=itemId, rating=myRating)
                rating.grocery_ratings = grocery
                customer.grocery_ratings.append(rating)
                db.session.add(rating)
                db.session.commit()
                return self.getRating(custId, itemId)
        else:
            False


    def getRating(self, custId, itemId):

        rating = Rating.query.filter_by(cust_id=custId, item_id=itemId).first()
        try:
            if rating.cust_id:
                return rating
            else:
                return False
        except:
            return False
        
    def getRatingDF(self):
        db_connection = create_engine(os.environ.get('PYMYSQL_DATABASE_URI') or 'mysql+pymysql://root:''@localhost:3306/food_delivery')
        df = pd.read_sql('SELECT * FROM rating', con=db_connection)
        print(df)
        return df
