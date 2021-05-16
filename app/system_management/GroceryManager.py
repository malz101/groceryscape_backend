from app import uploaddir
import os
from werkzeug.utils import secure_filename
class GroceryManager:
    def __init__(self, grocery_access, rating_access):
        self.grocery_access = grocery_access
        self.rating_access = rating_access


    def addGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            name = getParam('grocery_name')
            description = getParam('description')
            quantity = getParam('quantity')
            price = getParam('price')
            units = getParam('units')
            grams_per_unit = getParam('grams_per_unit')
            category = getParam('category')
            photo = getParam('photo')

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                uploaddir, filename
            ))


            """validate the data"""

            """add grocery item to stock"""
            grocery = self.grocery_access.create_grocery(name, description, int(quantity), units, float(price), float(grams_per_unit),category, filename)
            if grocery:
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery, None)}}, 200
            else:
                return {'msg':'request to create new grocery item failed', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def updateGrocery(self,grocery_id,request):

        try:
            getParam = self.getRequestType(request)
            # groceryId = getParam('grocery_id')
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            grocery = self.grocery_access.updateGrocery(grocery_id, attribute, value)
            if grocery:
                rating = self.rating_access.getItemRating(grocery.id)
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery,rating)}}, 200

            else:
                return {'msg':'update failed', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def deleteGrocery(self, grocery_id):

        try:
            # getParam = self.getRequestType(request)
            # groceryId = getParam('grocery_id')

            '''validate and sanitize data'''

            '''remove grocery from db'''
            groceries = self.grocery_access.removeGroceryItem(int(grocery_id))
            response = []
            if groceries:
                for grocery in groceries:
                    rating = self.rating_access.getItemRating(grocery.id)
                    response.append(self.__getGroceryDetails(grocery, rating))
                return {'msg':'success', 'data':{'groceries':response}}, 200
            else:
                return {'msg':'no groceries in stock', 'data':{}}, 200
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def getGroceries(self, request):

        try:
            getParam = self.getRequestType(request)
            category = getParam('category')
            description = getParam('description')
            name = getParam('name')

            groceries = self.grocery_access.getGroceries(name, description, category)
            response = []
            if groceries:
                for grocery in groceries:
                    rating = self.rating_access.getItemRating(grocery.id)
                    response.append(self.__getGroceryDetails(grocery,rating))
                return {'msg':'success', 'data':{'groceries':response}},200
            else:
                return {'msg':'no grocery found', 'data':{}}, 200
        except Exception as e:
            print (e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500
    

    def getGroceriesInList(self,ids):
        groceries = self.grocery_access.getGroceriesInList(ids)
        result =[]
        if groceries:
            for grocery in groceries:
                rating = self.rating_access.getItemRating(grocery.id)
                result.append(self.__getGroceryDetails(grocery, rating))
        return result


    def getGrocery(self, request):
        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')

            grocery = self.grocery_access.searchForGrocery(int(groceryId))
            if grocery:
                rating = self.rating_access.getItemRating(grocery.id)
                return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery,rating)}}, 200
            else:
                return {'msg':'no grocery found', 'data':{}}, 200
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500
        

    def getFeaturedItems(self):
        try:
            ratings = self.rating_access.getTopItems()
            
            ids = [rating.item_id for rating in ratings]

            items = self.grocery_access.getGroceriesInList(ids)

            if items:
                result = []
                for item in items:
                    rating = self.rating_access.getItemRating(item.id)
                    result.append(self.__getGroceryDetails(item,rating))
                return {'msg':'success','data':{'groceries':result}}
            return False
        except Exception as e:
            print(e)
            return {'msg':'request failed', 'error':'ise-0001'}, 500

    def __getGroceryDetails(self, grocery,rating):

        result = {
            'id': str(grocery.id),
            'name': grocery.name, 
            'description': grocery.description,            
            'quantity': str(grocery.quantity), 
            'units': grocery.units,
            'cost_per_unit': str(grocery.cost_per_unit), 
            'grams_per_unit':str(grocery.grams_per_unit),
            'category':grocery.category, 
            'photo':grocery.photo, 
            'sku':grocery.sku
        }
        if rating:
            result['rating'] = rating.total_rating/(rating.num_customer*5)*5
            result['num_customers_rated'] = rating.num_customer
        else:
            result['rating'] = None
            result['num_customers_rated'] = 0
        return result


    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
