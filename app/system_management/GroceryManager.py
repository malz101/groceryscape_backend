class GroceryManager:
    def __init__(self, grocery_access):
        self.grocery_access = grocery_access
        
    def addGrocery(self, request):

        name = request.form['grocery_name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']

        """validate the data"""

        """add grocery item to stock"""
        grocery = self.grocery_access.create_grocery(name, description, quantity, float(price))
        return grocery.id, grocery.name, grocery.description, grocery.price