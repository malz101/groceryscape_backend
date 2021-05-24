from flask import Blueprint
from flask import redirect, url_for, session, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.CartManager import CartManager
from ..database.db_access import cart_access, grocery_access

manage_cart = Blueprint("manage_cart", __name__)

cart_manager = CartManager(cart_access, grocery_access)
emp_login_restrict_msg = {'msg':'your account does not have a cart', 'error':'notfound-0001'}, 404

@manage_cart.route('/addToCart', methods=['POST','GET'])
@jwt_required()
def addToCart():
    user = get_jwt_identity()
    if not 'role' in user:
        try:
            result = cart_manager.addToCart(request, user)
            if result:
                response = {'msg':'success','data':{}}, 201
            else:
                response = {'msg':'Item not added. Duplicate Item or Grocery Item not in database','error':'create-0001'}, 404
        except ValueError as e:
            print(e)
            response = {'msg':'quantity execeed quantity stock or negative value provided', 'error':'create-0001'}, 200
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return emp_login_restrict_msg

  
@manage_cart.route('/removeFromCart/<grocery_id>', methods=['POST', 'GET'])
@jwt_required()
def removeFromCart(grocery_id):
    
    user = get_jwt_identity()
    if not 'role' in user:
        try:
            result = cart_manager.removeItemFromCart(grocery_id, user)
            if result:
                response = {'msg':'success', 'data':{}}, 200
            else:
                response = {'msg':'no item found', 'error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
    else:
        return emp_login_restrict_msg
    
@manage_cart.route('/empty_cart', methods=['GET'])
@jwt_required()
def empty_cart():
    user = get_jwt_identity()
    if not 'role' in user:
        try:
            cartItems = cart_manager.emptyCart(user)
            if cartItems:
                response = {'msg':'success', 'data':{}},200
            else:
                response = {'msg':'no item found', 'error':'notfound-0001'},200
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
    else:
        return emp_login_restrict_msg
    

@manage_cart.route('/get_cart_items', methods=['GET'])
@jwt_required()
def get_cart_items():
    user = get_jwt_identity()
    if not 'role' in user:
        try:
            cartItems = cart_manager.getAllCartItems(user)
            if cartItems:
                response = {'msg':'success', 'data':cartItems}
            else:
                response = {'msg':'no items found','data':{}},200
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
    else:
        return emp_login_restrict_msg


@manage_cart.route('/update_cart', methods=['POST'])
@jwt_required()
def update_cart():
    user = get_jwt_identity()
    if not 'role' in user:
        try:
            cartItem = cart_manager.updateCart(request, user)
            if cartItem:
                response = {'msg':'cart updated', 'data':{'cart':cartItem}}, 200
            else:
                response = {'msg':'cart not updated', 'error':'create-0001'}, 404
        except ValueError as e:
            print(e)
            response = {'msg':'one of the items specified is now out of stock or negative value provided', 'error':'create-0001'}, 200
        except TypeError as e:
            print(e)
            response = {'msg':'incorrect data format', 'error':'create-0001'}, 400
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return emp_login_restrict_msg
