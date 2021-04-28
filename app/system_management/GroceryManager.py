class GroceryManager:
    def __init__(self, grocery_access):
        self.grocery_access = grocery_access
        
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

            """validate the data"""

            """add grocery item to stock"""
            grocery = self.grocery_access.create_grocery(name, description, int(quantity), units, float(price), float(grams_per_unit),category)
            if grocery:
                return self.__getGroceryDetails(grocery)
            else:
                return {'msg':'request to create new grocery item failed'}
        except:
            return {'msg':'request to create new grocery item failed'}

    def updateGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')
            attribute = getParam('attribute')
            value = getParam('value')

            '''validate and sanitize data'''

            '''perform update'''
            grocery = self.grocery_access.updateGrocery(groceryId, attribute, value)
            if grocery:
                return self.__getGroceryDetails(grocery)
            else:
                return {'msg':'update failed'}
        except:
            return {'msg':'request failed'}

    def deleteGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')

            '''validate and sanitize data'''

            '''remove grocery from db'''
            groceries = self.grocery_access.removeGroceryItem(int(groceryId))
            response = {}
            if groceries:
                for grocery in groceries:
                    response[str(grocery.id)] = self.__getGroceryDetails(grocery)
                return response
            else:
                return {'msg':'no groceries in stock'}
        except:
            return {'msg':'request failed'}

    def getGroceries(self, request):

        try:
            groceries = self.grocery_access.getGroceries()
            response = {}
            if groceries:
                for grocery in groceries:
                    response[str(grocery.id)] = self.__getGroceryDetails(grocery)
                return response
            else:
                return {'msg':'no grocery found'}
        except:
            return {'msg':'request failed'}

    def getGroceriesByCategory(self, request):

        try:
            getParam = self.getRequestType(request)
            category = getParam('category')

            groceries = self.grocery_access.getGroceriesByCategory(category)
            response = {}
            if groceries:
                for grocery in groceries:
                    response[str(grocery.id)] = self.__getGroceryDetails(grocery)
                return response
            else:
                return {'msg':'no grocery found'}
        except:
            return {'msg':'request failed'}

    def getGrocery(self, request):

        try:
            getParam = self.getRequestType(request)
            groceryId = getParam('grocery_id')

            grocery = self.grocery_access.searchForGrocery(int(groceryId))
            if grocery:
                return self.__getGroceryDetails(grocery)
            else:
                return {'msg':'no grocery found'}
        except:
            return {'msg':'request failed'}

    def __getGroceryDetails(self, grocery):

        return {'id': str(grocery.id), 'name': grocery.name, 'description': grocery.description, \
                        'quantity': str(grocery.quantity), 'units': grocery.units, \
                        'cost_per_unit': str(grocery.cost_per_unit), 'grams_per_unit':str(grocery.grams_per_unit),\
                'category':grocery.category}


    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
