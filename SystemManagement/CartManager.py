
class CartManager:

    def __init__(self, cartAccess):
        self.cartAccess = cartAccess

    def addToCart(self, request):

        cartId = request.form['cart-id']
        quantity = request.form['quantity']
        itemId = request.form['item-id']

        """check if item in stock"""

        """add item to cart"""


    def clearCart(self, request):
        pass

    def removeItemFromCart(self, request):
        pass

    def checkoutCart(self, request):
        pass