# import all lib for ML
import pandas

class MLManager:
    
    def __init__(self, ratingAccess, groceryAccess):
        self.ratingAccess = ratingAccess
        self.groceryAccess = groceryAccess
    
    def getRecommendGroceries(self, custId):
        
        # this the dataframe of the 
        ratingDf = self.ratingAccess.getRatingDF()
        return str(ratingDf)
        '''using rating dataframe to dynamically create model and recommend'''
        
        '''produce a list of grocery ids the should be recommended'''
        lst = []
        recommendedGroceries = groceryAccess.getRecommendedGroceries(lst)
        return recommendedGroceries
    
    '''create supporting methods if needs be'''
    def supportingMethods(self):
        pass