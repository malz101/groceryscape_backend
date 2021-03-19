
class CartManager:

    def __init__(self, cartAccess, groceryAccess):
        self.groceryAccess = groceryAccess
        self.cartAccess = cartAccess

    def addToCart(self, request, session):

        try:
            '''extract request params'''
            getParam = self.getRequestType(request)
            cartId = session['cust_id']
            quantity = getParam('quantity')
            itemId = getParam('item_id')

            '''sanitize data'''

            '''add item to cart and return all cart items for customer'''
            cart = self.cartAccess.addToCart(int(itemId), int(cartId), int(quantity))
            response = {}
            if cart:
                for grocery in cart:
                    response[str(grocery.item_id)] = {'grocery_id':grocery.item_id, 'quantity':str(grocery.quantity),\
                                                      'cost':str(grocery.cost)}
                return response
            else:
                return False
        except:
            return False

    def emptyCart(self, request):

        self.cartAccess.emptyCart(1)

    def removeItemFromCart(self, request):
        pass

    def checkoutCart(self, request):

        self.cartAccess.checkoutCart(1)

    def updateCartItem(self, request):
        pass

    def getAllCartItems(self, request):
        pass

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get