from flask_restful import Resource
from flask import current_app, jsonify, session, request, redirect, url_for,  render_template
from app.service import cart_access, product_access
from ..common.decorators import login_required
from .errors import CartItemAlreadyExistsError, CartItemNotExistsError, ProductNotExistsError, ProductNotAvailableError
from app.schemas import CartItemSchema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

class CartApi(Resource):
    def get(self):
        """return cart items for customer.
        Logged in customer cart data is stored in database.
        Non-Logged in cutomer cart data is stored in session"""
        subtotal_price = 0
        #total_price = 0 #leave this for checkout route
        total_weight = 0
        item_count = 0
        items = []
        cart_level_discount_applications = []
        cart_item_schema = CartItemSchema()

        if session.get('logged_in'):
            cart = cart_access.get_cart(session['customer_id'])
            
            #traverse cart to get summary for logged in user
            for cart_item in cart:
                # line_item_dict = serialize_line_item_auth(cart_item)
                line_item_dict = cart_item_schema.dump(cart_item)

                subtotal_price += line_item_dict['line_subtotal_price']
                item_count += line_item_dict['quantity']
                total_weight += line_item_dict['item_total_weight']
                items.append(line_item_dict)
        else:#not logged in
            session.setdefault('cart',dict({})) #initlialize cart if not already created
            cart = session.get('cart')
            #cart for non-logged in user is stores in session as {product_id: quantity}
            products_in_cart = product_access.get_products_in_list(list(cart.keys())) if cart else []
            
            #traverse cart to get summary for non-logged in user
            for product in products_in_cart:
                quantity = cart[product.id]#get quantity of product in cart
                
                line_item_dict = serialize_line_item_not_auth(quantity, product)
    
                item_count += line_item_dict['quantity']
                subtotal_price += line_item_dict['line_subtotal_price']
                total_weight += line_item_dict['item_total_weight']
                items.append(line_item_dict)


        response = jsonify({
            'subtotal_price': subtotal_price,
            'total_weight': total_weight, 
            'item_count':item_count,
            'items': items,
            'cart_level_discount_applications': cart_level_discount_applications #check spotify cart api
        })
        response.status_code = 200
        
        return response

                

    def post(self):
        """addtocart"""
        #Just to not cause confusion in the future, my first approach was to take a list of new cart items and then add them to cart
        #however I changed to just take a single item and put responsibilty of frontend to make multiple request to add multiple items
        #to cart, for reasons as follows:
        #It's more difficult to craft error messages for multiple items.
        #Also by nature, 1 cart entry is one resource and that is what the post request is for, to add a resource

        #new item to add to cart are received as [product_id: quantity,...]
        try:

            add_to_cart_schema = CartItemSchema(exclude=('product','line_price','line_subtotal_price','line_weight'))
            new_cart_item = add_to_cart_schema.load(request.json)
            new_cart_item_id = new_cart_item['product_id']
            new_cart_item_quantity = new_cart_item['quantity']

            
            product = product_access.get_product(new_cart_item_id)
            # new_cart_item_ids_list = list(new_cart_items.keys()) #create a list of all grocey ids to all to cart
            # products_found = product_access.get_products_in_list(new_cart_item_ids_list) #get a list of all products found from id list
            # products_not_found = set(new_cart_item_ids_list) - set([product.id for product in groceries_found]) #get a list of ids of items that don't exist in the database or out of stock
            
            # if groceries_not_found:
                # message = [f'The product with id# {invalid_product_id} doesn\'t exist.' for invalid_product_id in groceries_not_found]
                # response, status = jsonify({'messages': message})
            
                #creates a list of dicts that represent new cart items to be added to database using mutiple insers
                #new_cart_items_dict = [{'customer_id': session['customer_id'], 'item_id': product.id, 'quantity': min(new_cart_items[product.id], product.available)} for product in groceries_found if product.id not in groceries_not_available]
                #cart_access.add_items_to_cart(new_cart_items_dict)   
            if product:
                cart_item_schema = CartItemSchema() 
                if product.available < 1:
                    raise ProductNotAvailableError
                    # response = {'message': 'Cart Error','description': f'The product {product.name} is already sold out.'}
                    # response.status_code = 422
                elif new_cart_item_quantity <= product.available:
                    if session.get('logged_in'): 
                        cart_item = cart_access.add_to_cart(session['customer_id'], new_cart_item_id, new_cart_item_quantity)
                        # response = jsonify(serialize_line_item_auth(cart_item))
                        response = jsonify(cart_item_schema.load(cart_item))
                        response.status_code = 201
                    else:#not logged in
                        session.setdefault('cart',dict({}))#initialize an empty cart if cart doesn't exist
                        if session.get['cart'].get(new_cart_item_id):
                            raise CartItemAlreadyExistsError
                            # response = jsonify({'message': 'Cart Error','description':f'{product.name} already exists in cart.'}),422
                            # response.status_code = 422
                        else:#item not already in cart
                            session['cart'][new_cart_item_id] = new_cart_item_quantity
                            response = jsonify(serialize_line_item_not_auth(new_cart_item_quantity,product))
                            response.status_code = 201
                else: #new_cart_item_quantity > product.available
                    response = jsonify({'message': 'Cart Error',\
                        'description': f'You cannot add {new_cart_item_quantity} {product.name} to cart. '+\
                                        f'Only {product.available} {product.name} in stock.'})
                    response.status_code = 422
            else:
                raise ProductNotExistsError
                # response = jsonify({'message': 'Product Error', 'description': f'Product with id# {new_cart_item_id} does not exist'})
                # response.status_code = 404
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status
        except IntegrityError as err:
            raise CartItemAlreadyExistsError  
        return response


    def patch(self):
        "update_cart"
        try:
            update_cart_item_schema = CartItemSchema(exclude=('product','line_price','line_subtotal_price','line_weight'))
            update_cart_data = update_cart_item_schema.load(request.json)

            add_to_previous_quantity = update_cart_data['add_to_previous_quantity']
            
            cart_item_to_update = update_cart_data['cart_item']
            cart_item_to_update_id = cart_item_to_update['product_id']
            cart_item_to_update_quantity = cart_item_to_update['quantity']
        
            product = product_access.get_product(cart_item_to_update_id)
            if session.get('logged_in'):
                cart_item = cart_access.get_cart_item(session['customer_id'], cart_item_to_update_id)
            else:
                session.setdefault('cart',dict({}))#initlialize cart if not already created
                cart_item = {'product_id':cart_item_to_update_id , 'quantity':session.get('cart').get(cart_item_to_update_id)}\
                    if session.get('cart').get(cart_item_to_update_id,None) else dict({})

            if cart_item: #if item exist in cart
                cart_item_schema = CartItemSchema()
                if session.get('logged_in'):
                    cart_item_to_update_quantity = cart_item_to_update_quantity+cart_item.quantity if add_to_previous_quantity else cart_item_to_update_quantity
                else:
                    cart_item_to_update_quantity = cart_item_to_update_quantity+cart_item['quantity'] if add_to_previous_quantity else cart_item_to_update_quantity
                
                
                if cart_item_to_update_quantity == 0:#remove item from cart
                    if session.get('logged_in'):
                        result = cart_access.delete_cart_item(session['customer_id'], cart_item_to_update_id)
                    else:#not logged in
                        result = session.get('cart').pop(cart_item_to_update_id, None)
                    
                    if result:
                        response = jsonify({'message': 'Item removed from cart!'}) 
                        response.status_code = 201
                    else:
                        raise CartItemNotExistsError
                        # response = jsonify({'message': 'Cart Error','description': 'Item not found in cart.'})
                        # response.status_code = 404
                elif product.available < 1:
                    raise ProductNotAvailableError
                    # response = {'message': 'Cart Error','description': f'The product {product.name} is already sold out.'}
                    # response.status_code = 422            
                elif cart_item_to_update_quantity <= product.available:
                    if session.get('logged_in'):
                        cart_item = cart_access.update_cart_item(session['customer_id'],cart_item_to_update_id, cart_item_to_update_quantity)
                        if cart_item:
                            # response = jsonify(serialize_line_item_auth(cart_item))
                            response = jsonify(cart_item_schema.load(cart_item))
                            response.status_code = 201
                        else:
                            pass # raise CartItemNotExistsError
                    else:
                        session['cart'][cart_item_to_update_id] = cart_item_to_update_quantity
                        response = jsonify(serialize_line_item_not_auth(cart_item_to_update_quantity, product))
                        response.status_code = 201
                else:#cart_item_to_update_quantity > product.available
                    response = jsonify({'message': 'Cart Error',\
                        'description': f'You cannot add {cart_item_to_update_quantity} {product.name} to cart. '+\
                                        f'Only {product.available} {product.name} in stock.'})
                    response.status_code = 422
            else:
                raise CartItemNotExistsError
                # response = jsonify({'message': 'Cart Error', 'description': f'Product with id# {cart_item_to_update_id} does not exist in cart'})
                # response.status_code = 404
            
        except ValidationError as err:
            status = 400
            response = jsonify({'message': 'Schema Validation Error', 'description':err.messages, 'status':status})
            response.status_code = status            
        return response


    def delete(self):
        """empty cart, remove from cart"""
        
        if session.get('logged_in'):
            cart_access.delete_cart(session['customer_id'])
        else:#not logged in
            session.setdefault('cart',dict({}))#initlialize cart if not already created
            session['cart'].clear()
    
        response = jsonify({'message': 'Item removed from cart!'})
        response.status_code = 200

        return response


class SynchronizeCartsApi(Resource):
    """Synchronizes session cart with cart stored in database"""
    @login_required
    def post(self):
        session.setdefault('cart', dict({}))#initlialize cart if not already created
        session_cart = session['cart']
        #cart for non-logged in user is stored in session as {product_id: quantity}
        products_in_session_cart = product_access.get_products_in_list(list(session_cart.keys())) if session_cart else []
        db_cart = cart_access.get_cart_items(session['customer_id'])
        
        #update persistant cart with items from session cart
        for product in products_in_session_cart:
            quantity = session_cart[product.id]#quantity of item in session cart
            for cart_item_index in range(len(db_cart)):
                #if item in session cart is already in db cart, add the quantities of both and update db cart
                if product.id == db_cart[cart_item_index].product_id:
                    quantity += db_cart[cart_item_index].quantity #add quantity of item in session cart to quantity in db
                    quantity = min(quantity, product.available)#make sure quantity isn't more than what's available
                    cart_access.update_cart_item(session['customer_id'], product.id,quantity)
                    db_cart.pop(cart_item_index)
                    break
            else:#if item not already in cart (i.e if the inner loop wasn't broken)
                cart_access.add_cart_item(session['customer_id'],product.id, quantity)
                




###########----------Helper Functions--------##########

def serialize_line_item_auth(cart_item):
    # cart_item.quantity = min(cart_item.quantity, cart_item.product.available) #updates quantity in cart if more than what's in inventory, this does not persist to database
    
    
    line_subtotal_price = cart_item.quantity*cart_item.product.unit_price
    
    line_weight = cart_item.product.unit_weight * cart_item.quantity
    
    
    return {
        'product_id': cart_item.product_id,
        'quantity': cart_item.quantity,
        'image': cart_item.product.photo,
        'name': cart_item.product.name,
        'line_price': cart_item.product.unit_price,
        'line_subtotal_price': line_subtotal_price,
        'taxable': cart_item.product.taxable,
        'unit_weight': cart_item.product.unit_weight,
        'line_weight': line_weight,
        'line_level_discount_allocations':[], #check shopify cart api 
    }


def serialize_line_item_not_auth(quantity, product):
    # quantity = min(quantity, product.available)#updates quantity in cart if more than what's in inventory, this does not persist to database

    line_subtotal_price = quantity * product.unit_price

    line_weight = product.unit_weight * quantity

    return{
        'product_id': product.id,
        'quantity': quantity,
        'image': product.photo,
        'name': product.name,
        'line_price': product.unit_price,
        'line_subtotal_price': line_subtotal_price,
        'taxable': product.taxable,
        'unit_weight': product.unit_weight,
        'line_weight': line_weight,
        'line_level_discount_allocations':[], #check shopify cart api 
    }