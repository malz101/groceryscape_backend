from typing import ItemsView
from flask_restful import Resource
from flask import current_app, jsonify, session, request, redirect, url_for,  render_template
from app.customer.common.decorators import login_required
# import app.service.product_access as product_access
from app.service import product_access, rating_access
from app.schemas import ProductSchema, CustomerProductRatingSchema, ProductRecommendationsSchema
from .errors import InternalServerError, ProductNotExistsError, NoProductExistsError, NoRatingExistsError, RatingNotExistsError
from marshmallow import ValidationError

class ProductListApi(Resource):
    def get(self):
        product_query_schema = ProductSchema(only=('brand','name','description','category_ids'))
        query_params = product_query_schema.load(request.args, partial=True)
        products = product_access.get_products(**query_params)
        if products:
            response = jsonify(serialize_many_products(products))
            response.status_code = 200
        else:
            raise NoProductExistsError
        return response


class ProductApi(Resource):
    def get(self, product_id):
        #get_groceries and get product
        product = product_access.get_product(product_id)
        if product:
            # product_schema = ProductSchema()
            # response = jsonify(product_schema.dump(product))
            response = jsonify(serialize_product(product))
            response.status_code = 200
        else:
            raise ProductNotExistsError
        
        return response
    

class RateListApi(Resource):
    def get(self):
        # data = request.json
        customer_product_ratings = rating_access.get_customer_rating_for_products(session['customer_id'])
        if customer_product_ratings:
            # rating_schema = CustomerProductRatingSchema()
            # response = jsonify(rating_schema.load(customer_product_ratings))
            response = jsonify(serialize_many_customer_rating(customer_product_ratings))
            response.status_code = 200
        else:
            raise NoRatingExistsError
        return response
    
    @login_required
    def post(self):
        #rate_product
        try:
            add_rating_schema = CustomerProductRatingSchema(exclude=('customer_id',))
            data = add_rating_schema.load(request.json)
            customer_product_rating = rating_access.create_rating(session['customer_id'], data['product_id'], data['rating'])

            if customer_product_rating:
                # rating_schema = CustomerProductRatingSchema()
                # response = jsonify(rating_schema.dump(customer_product_rating))
                response = jsonify(serialize_customer_rating(customer_product_rating))
                response.status_code = 201
            else:
                raise InternalServerError
                #remember to raise Rating already exists error
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        return response


class RateApi(Resource):
    def get(self,product_id):
        # data = request.json
        customer_product_rating = rating_access.get_customer_rating_for_product(session['customer_id'], product_id)
        if customer_product_rating:
            # rating_schema = CustomerProductRatingSchema()
            # response = jsonify(rating_schema.load(customer_product_rating))
            response = jsonify(serialize_customer_rating(customer_product_rating))
            response.status_code = 200
        else:
            raise RatingNotExistsError
        return response
    

    def patch(self, product_id):
        try:
            update_rating_schema = CustomerProductRatingSchema(only=('rating',))
            data = update_rating_schema.load(request.json)
            customer_product_rating = rating_access.update_customer_rating_for_product(session['customer_id'], product_id, data['rating'])
            if customer_product_rating:
                # rating_schema = CustomerProductRatingSchema()
                # response = jsonify(rating_schema.dump(customer_product_rating))
                response = jsonify(serialize_customer_rating(customer_product_rating))
                response.status_code = 201
            else:
                raise NoRatingExistsError
                #remember to raise Rating already exists error
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        return response


# class ProductTopRatedApi(Resource):
#     def get(self):
#         #get featured items
#         data = request.json
#         top_rated_products = product_access.get_top_rated_products(data['num_to_select'])
#         if top_rated_products:
#             response = jsonify(serialize_many_products(top_rated_products))
            # response.status_code = 200
#         else:
#             raise NoProductExistsError
#         return response


# class ProductPopularApi(Resource):
#     def get(self):
#         #get popular items
#         data = request.json
#         popular_products = product_access.get_popular_products(data['num_to_select'])
#         if popular_products:
#             response= jsonify(serialize_many_products(popular_products))
            # response.status_code = 200  
#         else:
#             raise NoProductExistsError
#         return response


# class ProductBougthWithApi(Resource):
#     def get(self):
#         #get_freq_bought_with
#         data = request.json
#         products_bought_with = product_access.get_freq_bought_with(data['product_id'], data['num_to_select'])
#         if products_bought_with:
#             response = jsonify(serialize_many_products(products_bought_with))
            # response.status_code = 200
#         return response


class ProductRecommendationsApi(Resource):
    def get(self, type):
        #the three previous functions could be seen as different
        #type of recommendations, there an option could exist where
        #a get param is used to switch between the type of recommendation
        # data  = request.json

        match type:
            case 'top_rated':
                get_top_rated_schema = ProductRecommendationsSchema(exclude=('product_id',))
                data = get_top_rated_schema.load(request.json)
                products = product_access.get_top_rated_products(data['num_to_select'])
            case 'most_popular':
                get_most_popular_schema = ProductRecommendationsSchema(exclude=('product_id',))
                data = get_most_popular_schema.load(request.json)
                products = product_access.get_popular_products(data['num_to_select'])
            case 'freq_bought with':
                get_freq_bought_with_schema = ProductRecommendationsSchema()
                data = get_freq_bought_with_schema.load(request.json)
                products = product_access.get_freq_bought_with(data['product_id'], data['num_to_select'])
            case 'personal':
                @login_required
                def helper():
                    products = product_access.get_customer_recommendations(session['customer_id'])
                    return products
                products = helper()
            case _:
                #todo: actually this should be an invalid recommendation type error
                NoProductExistsError 
        
        if products:
            response = jsonify(serialize_many_products(products))
            response.status_code = 200
        else:
            NoProductExistsError
        return response



###########----------Helper Functions--------##########
def serialize_product(product):
    product_schema = ProductSchema()
    return product_schema.dump(product)
    # result = {
    #     'id': product.id,
    #     'name': product.name,
    #     'brand': product.brand, 
    #     'description': product.description,            
    #     'invetory': product.inventory,
    #     'available': product.available,
    #     'size': product.size, 
    #     'cost_per_unit': product.cost_per_unit, 
    #     'unit_weight': product.unit_weight, 
    #     'photo': product.photo, 
    #     'sku': product.sku,
    #     'package_type': product.package_type,
    #     'taxable': product.taxable,
    #     'categories': product.categories,
    #     'rating': {}
    # }
    
    # # avg_rating = product_access.get_avg_rating(product.id)
    # if product.avg_rating:
    #     result['rating']['avg_rating'] = product.avg_rating.avg_rating
    #     result['rating']['num_customers'] = product.avg_rating.num_customers
    # else:
    #     result['rating']['avg_rating'] = None
    #     result['rating']['num_customers'] = 0
    # return result


def serialize_many_products(products):
    '''serialize many products'''
    product_schema = ProductSchema(many=True)
    return product_schema.dump(products)
    # serialized_products = []
    # for product in products:
    #     # serialized_products.append(serialize_product(product))
    #     serialized_products.append(product_schema.dump(product))
    # return serialized_products

def serialize_customer_rating(customer_product_rating):
    rating_schema = CustomerProductRatingSchema()
    return rating_schema.dump(customer_product_rating)
    # return {
    #     'product_id': customer_product_rating.product_id,
    #     'rating': customer_product_rating.rating
    # }

def serialize_many_customer_rating(customer_product_ratings):
    rating_schema = CustomerProductRatingSchema(many=True)
    return rating_schema.dump(customer_product_ratings)