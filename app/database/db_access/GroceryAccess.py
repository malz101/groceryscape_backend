from app import db
from ..models import Grocery
from ..models import Taxes
from ..models import TaxesOnGrocery
from sqlalchemy import and_, or_, not_

class GroceryAccess:

    def create_grocery(self, name, description, quantity, units, price, unit_weight,category, photo):

        grocery = Grocery(name, description, quantity, units, price,\
                          unit_weight, category, photo)
        db.session.add(grocery)
        db.session.commit()
        return self.searchForGrocery(grocery.id)
    
#     def decreaseQuantity(self,id, amount):
#         dated = Grocery.query.filter_by(id=id).update(dict(email='my_new_email@example.com')))
# db.session.commit()
#         '''Decrease the stock count of grocery items 
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
            if attribute == 'unit_weight':
                grocery.unit_weight = float(value)
                db.session.commit()
                return self.searchForGrocery(groceryId)
            if attribute == 'category':
                grocery.category = value
                db.session.commit()
                return self.searchForGrocery(groceryId)
        return False
    

    def adjustStockCount(self,grocery_id,value):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        grocery.quantity += value
        db.session.commit()
        return grocery


    def searchForGrocery(self, grocery_id):
        grocery = Grocery.query.filter_by(id=grocery_id).first()
        try:
            if grocery.id:
                return grocery
            else:
                return False
        except:
            return False

    def getGroceries(self, name=None, description=None, category=None):
        if name is None:
            name =''
        name = '%{}%'.format(name)

        if description is None:
            description = ''
        description = '%{}%'.format(description)

        if category is None:
            category = ''
        category = '%{}%'.format(category)

        groceries = Grocery.query.filter(
            and_(
                Grocery.name.ilike(name), 
                Grocery.description.ilike(description), 
                Grocery.category.ilike(category)
            )
        ).all()
        # try:
        if groceries:
            return groceries
        return False
        # except:
        #     return False
    
    def get_groceries_in_list(self,ids):
        groceries = Grocery.query.filter(Grocery.id.in_(ids)).all()
        # print('Groceries in grcoery access',groceries)
        return groceries
    
    def get_grocery(self, id):
        grocery = Grocery.query.filter(Grocery.id==id)
        return grocery
        
    def removeGroceryItem(self, groceryId):

        grocery = self.searchForGrocery(groceryId)
        if grocery:
            db.session.delete(grocery)
            db.session.commit()
        return self.getGroceries()
    
    def getTaxType(self, groceryId, type):
        grocery = self.searchForGrocery(groceryId)
        if grocery:
            tax = TaxesOnGrocery.query.filter(and_(TaxesOnGrocery.tax.ilike(type), TaxesOnGrocery.grocery_id==groceryId)).first()
            try:
                if tax.grocery_id:
                    return tax
            except:
                return False
        else:
            return False
    
    def getTax(self, groceryId, type):
        taxOnItem = self.getTaxType(groceryId, type)
        if taxOnItem:
            return float(taxOnItem.tax_type.rate) * float(taxOnItem.grocery.cost_per_unit)
        else:
            return 0



