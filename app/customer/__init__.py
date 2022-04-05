# from .resources.routes import initialize_routes

def create_blueprint():
    from flask import Blueprint
    from flask_restful import Api
    from .resources.errors import errors
    
    customer_bp = Blueprint('customer',__name__)
    customer_api = Api(customer_bp,errors=errors)
    initialize_routes(customer_api)
    
    return customer_bp



def initialize_routes(api):
    from .resources.customer_resources import CustomerApi
    from .resources.auth import CSRFTokenApi,LoginApi, LogoutApi, ConfirmEmailApi
    from .resources.cart_resources import CartApi
    from .resources.product_resources import ProductApi, ProductListApi, RateListApi, RateApi, ProductRecommendationsApi
    # from .resources.order_resources import OrderApi, OrderListApi
    
    api.add_resource(CSRFTokenApi, '/csrf-token', endpoint='csrf-token')
    api.add_resource(CustomerApi, '/customers', endpoint='customers')
    api.add_resource(LoginApi, '/login', endpoint='login')
    api.add_resource(LogoutApi, '/logout', endpoint='logout')
    api.add_resource(ConfirmEmailApi, '/confirm-email/<string:token>', endpoint='confirm-email')
    
    api.add_resource(CartApi, '/carts', endpoint='carts')

    api.add_resource(ProductListApi, '/products', endpoint='products')
    api.add_resource(ProductApi, '/products/<int:product_id>', endpoint='product')
    api.add_resource(ProductRecommendationsApi, '/products/recommendation/<string:type>', endpoint='recommendation')
    api.add_resource(RateListApi, '/products/rates', endpoint='rates')
    api.add_resource(RateApi, '/products/rates/<int:product_id>', endpoint='rate')

    # api.add_resource(OrderListApi, '/orders', endpoint='orders')
    # api.add_resource(OrderApi, '/orders<int:order_id>', endpoint='order')