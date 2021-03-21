
class RatingManager:
    def __init__(self, rating_access):
        self.rating_access = rating_access

    def rateGrocery(self, session, request):
        try:
            getParam = self.getRequestType(request)
            custId = session['cust_id']
            itemId = getParam('item_id')
            rating = getParam('rating')

            rating = self.rating_access.rateGrocery(int(custId),int(itemId), int(rating))
            if rating:
                return {'customer_id':str(rating.cust_id),'customer_name':(rating.customer_ratings.first_name+" "+\
                        rating.customer_ratings.last_name), 'grocery_name':rating.grocery_ratings.name,\
                        'grocery_id':str(rating.item_id),'rating':str(rating.rating)}
            else:
                return {'msg':'operation could not be completed'}
        except:
            return {'msg':'failed request'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get

