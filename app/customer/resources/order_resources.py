from flask_restful import Resource
from flask import current_app, jsonify, session, request, redirect, url_for

from app.schemas import OrderSchema
from ..common.decorators import login_required, email_verification_required
from app.service import order_access
from .errors import InternalServerError, OrderNotExistsError, NoOrderExistsError, CreateOrderError
from marshmallow import ValidationError

class OrderListApi(Resource):
    def get(self):
        try:
            order_query_schema = OrderSchema(only=('brand','name','description','category_ids'))
            query_params = order_query_schema.load(request.args, partial=True)
            query_params.update({'customer_id':session['customer_id']})
            orders = order_access.get_orders(**query_params)

            if orders:
                response = jsonify(serialize_many_orders(orders))
                response.status_code = 200
            else:
                raise NoOrderExistsError
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        return response


    @login_required
    @email_verification_required
    def post(self):
        #create order
        try:
            add_order_schema = OrderSchema(exclude=('id','customer_id','created_at','delivered_time','checkout_by'))
            new_order_data = add_order_schema.load(request.json)
            new_order_data.update({'customer_id':session['customer_id']})
            order = order_access.create_order(new_order_data)
            if order:
                # order_schema = ProductSchema()
                # response = jsonify(order_schema.dump(order))
                response = jsonify(serialize_order(order))
                response.status_code = 200
            else:
                raise InternalServerError
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        return response


class OrderApi(Resource):
    @login_required
    @email_verification_required
    def get(self, order_id):
        #get_my_orders and get order
        order = order_access.get_order(session['customer_id'], order_id)
        
        if order:
            response = jsonify(serialize_order(order))
            response.status_code = 200
        else:
            raise OrderNotExistsError
        return response


    @login_required
    @email_verification_required
    def patch(self,order_id):
        #update order, currently only set_delivery location
        pass
    
    @login_required
    @email_verification_required
    def delete(self,order_id):
        #cancel order
        pass



#########-----------HELPER FUNCTIONS------------################
def serialize_order(order):
    '''returns a dictionary with order info'''
    order_schema = OrderSchema()
    return order_schema.dump(order)
    # serialized_order = {
    #     'id': order.id,
    #     'customer_id': order.customer_id,
    #     'created_at': order.created_at, 
    #     'status': order.status,
    #     'payment_type': order.payment_type,
    #     'billing': {
    #         'first_name': order.billing_first_name,
    #         'last_name': order.billing_last_name,
    #         'telephone': order.billing_telephone,
    #         'street': order.billing_street,
    #         'town': order.billing_town,
    #         'parish': order.billing_parish,
    #     },
    #     'shipping': {
    #         'first_name': order.shipping_first_name,
    #         'last_name': order.shipping_first_name,
    #         'street': order.shipping_street,
    #         'town': order.shipping_town, 
    #         'parish': order.shipping.parish, 
    #         'fee': order.shipping_fee,
    #         'time_slot': {
    #             'id': order.shipping_time_slot_id,
    #             'start_time': order.time_slot.start_time,
    #             'end_time': order.time_slot.end_time
    #         }
    #     },
    #     # 'payment': { serialize each payment
    #     #     'order_id': order.payment.order_id,
    #     #     'created_at': order.payment.created_at,
    #     #     'amount_tendered': order.payment.amount_tendered,
    #     #     'type': 
    #     # },
    #     'notes': order.notes,
    #     'delivered_time': order.delivered_time,
    #     'checkout_by': order.checkout_by
    # }

    # ####-----SERIALIZE ORDER ITEMS------######
    # subtotal_price = 0
    # total_tax=0
    # total_price = 0
    # total_weight = 0
    # item_count = 0
    # discounts = []
    # items =[]

    # for order_item in order.items:
    #     #order item level
    #     line_subtotal_price = order_item.unit_price*order_item.quantity
    #     line_tax = line_subtotal_price * order_item.tax_rate
    #     line_total_price = line_subtotal_price + line_tax
    #     line_weight = order_item.unit_weight*order_item.quantity

    #     #order level
    #     subtotal_price+= line_subtotal_price
    #     total_tax+=line_tax
    #     total_price += line_total_price
    #     total_weight += line_weight
    #     item_count += order_item.quantity

    #     items.append({
    #         'order_id': order_item.order_id,
    #         'product': {
    #             'product_id': order_item.product_id,
    #             'name': order_item.product_name,
    #             'sku': order_item.sku,
    #             'unit_price': order_item.unit_price,
    #             'unit_weight': order.unit_weight,
    #             'photo': order_item.product.photo,
    #             'brand': order_item.product_brand,
    #             'package_type': order_item.product_package_type
    #         },
    #         'line_weight': line_weight,
    #         'tax_rate': order_item.tax_rate,
    #         'quantity': order_item.quantity,
    #         'line_subtotal_price': line_subtotal_price,
    #         'line_total_price': line_total_price,
    #         'line_tax': line_tax,
    #         'line_level_discount_allocations': [], #check shopify cart api
    #     })
                
                
    # serialized_order.update({
    #     'subtotal_price':subtotal_price,
    #     'total_tax': total_tax,
    #     'total_price_before_shipping_fee': total_price,
    #     'final_price': total_price + order.shipping_fee,
    #     'total_weight': total_weight, 
    #     'item_count':item_count,
    #     'items': items,
    #     'discounts': discounts})
    
    # return serialized_order


def serialize_many_orders(orders):
    '''returns a list of dictionaries with order info'''
    order_schema = OrderSchema(many=True)
    return order_schema.dump(orders)