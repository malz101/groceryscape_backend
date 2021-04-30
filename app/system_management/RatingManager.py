
class RatingManager:
    def __init__(self, rating_access):
        self.rating_access = rating_access

    def rateGrocery(self, user, request):
        try:
            getParam = self.getRequestType(request)
            custId = user['cust_id']
            itemId = getParam('item_id')
            rating = getParam('rating')

            rating = self.rating_access.rateGrocery(int(custId),int(itemId), int(rating))
            if rating:
                return {
                    'msg': 'success', 
                    'data':{
                        'rating':{
                            'customer_id':str(rating.cust_id),
                            'customer_name':(rating.customer_ratings.first_name+" "+rating.customer_ratings.last_name),
                            'grocery_name':rating.grocery_ratings.name,
                            'grocery_id':str(rating.item_id),
                            'rating':str(rating.rating)
                        }
                    }
                }, 200
            else:
                return {'msg':'operation could not be completed because customer or grocery does not exist', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            return {'msg':'failed request', 'error':'ise-0001'}, 500
        
    def getDataFrame(self):
        return self.rating_access.getDataFrame()

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get

