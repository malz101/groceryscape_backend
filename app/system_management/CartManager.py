
class CartManager:

    def __init__(self, cartAccess, groceryAccess):
        self.groceryAccess = groceryAccess
        self.cartAccess = cartAccess

    def addToCart(self, request, user):

        try:
            '''extract request params'''
            getParam = self.getRequestType(request)
            cartId = user['cust_id']
            quantity = getParam('quantity')
            itemId = getParam('item_id')

            '''sanitize data'''

            '''add item to cart and return all cart items for customer'''
            cart = self.cartAccess.addToCart(int(itemId), int(cartId), int(quantity))
            response = {}
            if cart:
                for grocery in cart:
                    response[str(grocery.item_id)] = {'grocery_id':grocery.item_id,'name':grocery.cart_items.name,\
                                                      'quantity':str(grocery.quantity)}

                return response
            else:
                return {'msg':'failed operation'}
        except:
            return {'msg':'failed operation'}

    def emptyCart(self, session):

        try:
            cartId = session['cust_id']
            isEmpty = self.cartAccess.emptyCart(int(cartId))
            if isEmpty:
                return {'msg':'cart emptied'}
            else:
                return {'msg':'operation failed'}
        except:
            return {'msg':'operation failed'}

    def removeItemFromCart(self, request, session):

        try:
            getParam = self.getRequestType(request)
            itemId = getParam('grocery_id')
            cartId = session['cust_id']

            cartItems = self.cartAccess.removeItem(cartId, itemId)
            response = {}
            if cartItems:
                for grocery in cartItems:
                    response[str(grocery.item_id)] = {'grocery_id': str(grocery.item_id), 'quantity': str(grocery.quantity), \
                                                      'cost': str(grocery.cost), 'name':grocery.cart_items.name}
                return response
            else:
                return {'msg': 'failed'}

        except:
            return {'msg':'failed operation'}

    def checkoutCart(self, session):

        try:
            cartId = session['cust_id']
            order = self.cartAccess.checkoutCart(int(cartId))
            if order:
                return {'order_id':str(order.id), 'order_date':order.orderDate, 'status':str(order.status), \
                        'customer_id':str(order.customer_id), 'customer':(order.customer.first_name + " "+ order.customer.last_name)}
            else:
                return {'msg':'order was not created'}
        except:
            return {'msg':'failed request'}

    def updateCartItem(self, request, session):

        try:
            getParam = self.getRequestType(request)
            itemId = getParam('item_id')
            quantity = getParam('quantity')
            cartId = session['cust_id']

            cartItem = self.cartAccess.updateCartItem(int(cartId),int(itemId),int(quantity))
            if cartItem:
                return {'grocery_id': str(cartItem.item_id), 'quantity': str(cartItem.quantity), \
                        'cost': str(cartItem.cost), 'name':cartItem.cart_items.name}
            else:
                return {'msg':'not updated'}
        except:
            return {'msg':'failed request'}

    def getAllCartItems(self, session):

        try:
            cartId = session['cust_id']
            cartItems = self.cartAccess.getAllCartItems(cartId)
            response = {}
            if cartItems:
                for grocery in cartItems:
                    response[str(grocery.item_id)] = {'grocery_id': str(grocery.item_id), 'quantity': str(grocery.quantity), \
                                                      'cost': str(grocery.cost), 'name':grocery.cart_items.name}
                return response
            else:
                return {'msg': 'not item found'}
        except:
            return {'msg': 'failed'}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get