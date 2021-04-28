# import all lib for ML
import pandas
import sklearn
from sklearn.neighbors import BallTree
from sklearn.preprocessing import StandardScaler

class MLManager:

    def __init__(self, ratingAccess, groceryAccess):
        self.ratingAccess = ratingAccess
        self.groceryAccess = groceryAccess

    def getRecommendGroceries(self, custId):
        ratingDf = self.ratingAccess.getRatingDF()
        print(ratingsDF.shape)
        #ratingsDF = table.pivot_table(index='UserId', columns='ProductId', values='Rating', fill_value=0)

        """
        prodList = list(ratingsDF.columns)

        # Computes nearest neighbours for each customer
        ratingsNearestNeigh = BallTree(ratingsDF.values)

        # Lists the nearest neighbours for the customer given that are within the radius
        ratingsRecIndex, ratingsRecDist = ratingsNearestNeigh.query_radius([ratingsDF.values[0]], 10, return_distance=True, sort_results=True)

        print('ratingsRecIndex: ', ratingsRecIndex[0][0:5], '\nratingsRecDist : ', ratingsRecDist[0][0:5], '\n\n')

        # Access database for groceries the user hasn't bought that other users have
        """

        '''produce a list of grocery ids the should be recommended'''
        lst = []
        recommendedGroceries = groceryAccess.getRecommendedGroceries(lst)
        return recommendedGroceries
    
    '''create supporting methods if needs be'''
    def supportingMethods(self):
        pass