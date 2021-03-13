from ... import db
from ..Models import Grocery

class GroceryAccess:

    def create_grocery(self, name, description, quantity, price):

        grocery = Grocery(name=name, description=description, quantity=quantity, price=price)
        db.session.add(grocery)
        db.session.commit()

        return grocery

    def updateGrocery(self, grocery_item, updatedAttribites):
        pass


    def searchForGrocery(self, grocery_id):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        try:
            if grocery.id:
                return {'id':grocery.id, 'name':grocery.name, 'description':grocery.description,\
                        'quantity':grocery.quantity, 'units':grocery.units, 'cost_per_unit':grocery.cost_per_unit}
            else:
                return False
        except:
            return False

    def getAllGroceries(self):
        pass