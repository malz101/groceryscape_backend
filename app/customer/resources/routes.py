from .auth import LoginApi, LogoutApi, ConfirmEmailApi
from .cart_resources import CartApi

def initialize_routes(api):
    api.add_resource(LoginApi, '/login', endpoint='api.login')
    api.add_resource(LogoutApi, '/logout', endpoint='api.logout')
    api.add_resource(ConfirmEmailApi, '/confirm_email/<token>', endpoint='api.confirm_email')
    
    api.add_resource(CartApi, '/cart', endpoint='api.cart')