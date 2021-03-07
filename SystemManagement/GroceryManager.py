from database.Models import Grocery
from database.GroceryAccess import GroceryAccess
class GroceryManager:

    def addGrocery(self, request):

        name = request.form['grocery_name']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']

        """validate the data"""

        """add grocery item to stock"""
        grocery = GroceryAccess().create_grocery(name, description, quantity, float(price))
        return grocery.id, grocery.name, grocery.description, grocery.price