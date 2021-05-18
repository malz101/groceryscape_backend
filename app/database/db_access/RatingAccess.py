from ... import db
from ..Models import Rating, Grocery, Customer, ItemTotalRating
from sqlalchemy import create_engine
import pymysql
import  pandas as pd
import os
import random

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
            return False

    def getRating(self, custId, itemId):
        rating = Rating.query.filter_by(cust_id=custId, item_id=itemId).first()
        try:
            if rating.cust_id:
                return rating
            else:
                return False
        except:
            return False

    def getAllRatings(self):
        ratings = Rating.query.all()

        ratingsDict = {}
        for r in ratings:
            # Organizes the data in a dictionary indexed by customerID
            try:
                ratingsDict[r.cust_id][r.item_id] = r.rating
            except KeyError:
                ratingsDict[r.cust_id] = {}
                ratingsDict[r.cust_id][r.item_id] = r.rating
        return ratingsDict

    def getTopItems(self, ):
        top_items = ItemTotalRating.query.order_by(ItemTotalRating.coefficient.desc()).limit(50).all()
        num_to_select = 20                           # set the number to select here.
        return random.sample(top_items, num_to_select)

    def getItemRating(self,item_id):
        rating_summary = ItemTotalRating.query.filter_by(item_id=item_id).first()
        return rating_summary