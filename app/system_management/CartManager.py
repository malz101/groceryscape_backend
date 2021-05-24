class CartManager:

    def __init__(self, cartAccess, groceryAccess):
        self.groceryAccess = groceryAccess
        self.cartAccess = cartAccess

    def addToCart(self, request, user):

        '''extract request params'''
        getParam = self.getRequestType(request)
        cartId = user['cust_id']
        quantity = getParam('quantity')
        itemId = getParam('item_id')

        '''sanitize data'''

        '''add item to cart for customer'''
        result = self.cartAccess.addToCart(int(itemId), int(cartId), int(quantity))

        return result


    def emptyCart(self, user):
        
        cartId = user['cust_id']
        isEmpty = self.cartAccess.emptyCart(int(cartId))
        if isEmpty:
            return True
        return False

    def removeItemFromCart(self, grocery_id, user):

        # getParam = self.getRequestType(request)
        # itemId = getParam('grocery_id')
        cartId = user['cust_id']
        return self.cartAccess.removeItem(int(cartId),int(grocery_id))
        


    def updateCart(self, request, user):
        '''Updates items in user cart'''

        cartId = user['cust_id']
        new_cart_values_json = request.json
        print(new_cart_values_json)

        if new_cart_values_json:
            cart_items = self.cartAccess.updateCart(int(cartId),new_cart_values_json)
            print('passed cm78')
            if cart_items:
                return self.__getCartDetails(cart_items)
            return False
        raise TypeError


    def getAllCartItems(self, user):

        cartId = user['cust_id']
        cartItems = self.cartAccess.getAllCartItems(cartId)
        
        
        if cartItems:
            return self.__getCartDetails(cartItems)
        return False


    def __getCartDetails(self, cartItems):
        '''returns details about cart'''

        sub_total = 0
        total_gct = 0
        total_sct = 0
        response = []
        for grocery in cartItems:
            cost_before_tax = float(grocery.quantity*grocery.cart_items.cost_per_unit)
            sub_total+=cost_before_tax
            GCT = float(self.groceryAccess.getTax(grocery.item_id,'GCT')*grocery.quantity)
            SCT = float(self.groceryAccess.getTax(grocery.item_id,'SCT')*grocery.quantity)
            total_gct += GCT
            total_sct += SCT

            total = cost_before_tax + GCT + SCT
            total_weight = str(grocery.quantity*grocery.cart_items.grams_per_unit)+" grams"
            response.append ({
                'grocery_id': str(grocery.item_id),
                'photo' : grocery.cart_items.photo,
                'category': grocery.cart_items.category,
                'inventory': str(grocery.cart_items.quantity),
                'quantity': str(grocery.quantity),
                'cost_before_tax': str(cost_before_tax),
                'name':grocery.cart_items.name,
                'total_weight':total_weight,
                'GCT':str(GCT),
                'SCT':str(SCT),
                'total': str(total)
            
            })
        return {'items':response, 'sub_total':sub_total, 'total_gct':total_gct, 'total_sct':total_sct}

    def getRequestType(self, request):
        if request.method == 'GET':
            return request.args.get
        else:
            return request.form.get
