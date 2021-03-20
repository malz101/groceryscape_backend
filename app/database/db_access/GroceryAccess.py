from ... import db
from ..Models import Grocery

class GroceryAccess:

    def create_grocery(self, name, description, quantity, units, price):

        grocery = Grocery(name=name, description=description, quantity=quantity, units=units, cost_per_unit=price)
        db.session.add(grocery)
        db.session.commit()
        return self.searchForGrocery(grocery.id)

    def updateGrocery(self, groceryId, attribute, value):

        grocery = self.searchForGrocery(groceryId)
        if grocery:
            if attribute == 'name':
                grocery.name = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'description':
                grocery.description = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'quantity':
                grocery.quantity = int(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'units':
                grocery.units = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'cost_per_unit':
                grocery.cost_per_unit = float(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
        return False

    def searchForGrocery(self, grocery_id):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        try:
            if grocery.id:
                return grocery
            else:
                return False
        except:
            return False

    def getGroceries(self):
        groceries = Grocery.query.filter_by().all()
        try:
            if groceries[0].name:
                return groceries
        except:
            return False

    def removeGroceryItem(self, groceryId):

        grocery = self.searchForGrocery(groceryId)
        if grocery:
            db.session.delete(grocery)
            db.session.commit()
        return self.getGroceries()

