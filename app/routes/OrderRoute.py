from flask import Blueprint
from flask import redirect, url_for, session, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..system_management.OrderManager import OrderManager
from ..database.db_access import order_access
from ..database.db_access import order_groceries_access
from ..database.db_access import payment_access
import stripe

manage_order = Blueprint("manage_order", __name__)

order_manager = OrderManager(order_access, order_groceries_access, payment_access)

@manage_order.route('/schedule_order', methods=['POST','GET'])
@jwt_required()
def schedule_order():
    user = get_jwt_identity()
    if user and (not 'role' in user):
        try:
            order = order_manager.scheduleOrder(request, user)
            if order:
                response = {'msg':'success', 'data':{'order':order}}, 200
            else:
                {'msg':'issues with scheduling order', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'','error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/checkout_order', methods=['POST','GET'])
@jwt_required()
def checkout_order():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order = order_manager.checkOutOrder(user, request)
            if order:
                response = {'msg':'success','data':{'order':order}}, 200
            elif order == {}:
                response = {'msg':'Unsuccessful. Order not found', 'error':'create-0001'}, 404
            else:
                {'msg':'Unsuccessful. No order id detected', 'error':'create-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/get_order/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order = order_manager.getOrder(order_id)
            if order:
                response = {'msg': 'success', 'data':{'order':order}},200
            else:
                response = {'msg':'Order not found', 'error':'notfound-0001'}, 404
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response

    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/get_orders', methods=['POST','GET'])
@jwt_required()
def get_orders():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            orders = order_manager.getOrders(request)
            if orders:
                response = {'msg':'success', 'data':{'orders':orders}}, 200
            else:
                response = {'msg':'no orders found', 'data':{}},200
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return reponse
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/get_total', methods=['POST','GET'])
@jwt_required()
def get_total():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            order_total = str(order_manager.getTotalOnOrder())
            response = {'msg':'success', 'data':{'order_total': order_total}}
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/get_schedule', methods=['POST','GET'])
@jwt_required()
def get_schedule():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            orders = order_manager.getSchedule()
            if orders:
                response = {'msg':'success', 'data':{'orders':orders}}, 200
            else:
                response = {'msg':'no orders found', 'data':{'orders':orders}}, 200
        except Exception as e:
            print(e)
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response
    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401


@manage_order.route('/record_payment', methods=['POST','GET'])
@jwt_required()
def record_payment():
    user = get_jwt_identity()
    if user and ('role' in user):
        try:
            payment = order_manager.recordPayment(user,request)
            if payment:
                response = {'msg':'success', 'data':{'payment':payment}}, 200
            else:
                response = {'msg':'payment unsuccessful', 'error':'create-0001'}, 404
        except Exception as e:
            response = {'msg':'', 'error':'ise-0001'}, 500
        finally:
            return response

    else:
        return {'msg':'you are not logged in as an employee', 'error':'auth-0001'}, 401

@manage_order.route('/pay')
@jwt_required()
def pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'YOUR_PRODUCT_PRICE_ID',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


@app.route('/webhook', methods=['POST'])
def webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'YOUR_ENDPOINT_SECRET'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}