from app import db, encryp
from app.database.models import Cart, CartItem
from app.service import product_access

from datetime import datetime, timezone

def create_cart(customer_id: int):
    """create a cart"""
    cart = Cart(customer_id)
    db.session.add(cart)
    db.session.commit()
    return cart


def get_cart(cart_id: int):
    '''returns a cart with cart items and products in cart loaded'''
    # cart = CartItem.query.options(db.joinedload(CartItem.product)).where(CartItem.customer_id==customer_id).all()
    cart = Cart.query.options(
        db.joinedload(Cart.cart_items).
        joinedload(CartItem.product)
    ).where(Cart.cart_id==cart_id).one()
    return cart


def get_carts(customer_id=None, statuses=(),min_created_at=str(datetime(1970, 1, 1,tzinfo=timezone.utc)),\
    max_created_at=None, min_modified_at=str(datetime(1970, 1, 1,tzinfo=timezone.utc)),max_modified_at=None):
    '''returns customer's carts using the customer's ID, and other selection criteria'''

    max_created_at = max_created_at if max_created_at else str(datetime.utcnow()) #have to do this inside the function, otherwise the default max_created_at timestamp would be time at which the function as compilied
    max_modified_at = max_modified_at if max_modified_at else str(datetime.utcnow())    
    
    carts = Cart.query.options(db.joinedload(Cart.cart_items).lazyload(Cart.product)).where(
        db.and_(
            Cart.customer_id==customer_id,
            Cart._status.in_(map(lambda status: encryp.encrypt(status),statuses)) if statuses else Cart._status.not_in(statuses),
            Cart.created_at >= min_created_at,
            Cart.created_at <= max_created_at,
            Cart.modified_at >= min_modified_at,
            Cart.modified_at <= max_modified_at
        )
    ).all()
    return carts


def get_cart_item(cart_id: int, prodcut_id: int):
    '''get a single cart item without corresponding product loaded'''
    cart_item = CartItem.query.options(db.lazyload(CartItem.product)).where(
        db.and_(
            CartItem.cart_id==cart_id,
            CartItem.product_id==prodcut_id
        )
    ).one()
    return cart_item


def add_items_to_cart(cart_id: int, new_cart_items_data:list|tuple)->list|tuple:
    """add items to cart, returns a list of newly added cart items"""
    cart = get_cart(cart_id)
    # new_cart_items = [CartItem(cart_id, **new_cart_item) for new_cart_item in new_cart_items if new_cart_item['quantity']>0] #if new_cart_item['quantity']>0]
    # cart.items.extend(new_cart_items)

    new_cart_items = []
    for new_cart_item_data in new_cart_items_data:
        if new_cart_item_data['quantity']>0: #if quantity is zero don't add it to cart
            product = product_access.get_product(new_cart_item_data['product_id'])
            if product: #if product exists
                if product.available < 1:
                    # raise ValueError(f'The product \'{product.name}\' is already sold out.')
                    return (1,product)
                elif new_cart_item_data['quantity'] > product.available:
                    return (2,product,new_cart_item_data)
                    # raise ValueError(f'Cannot add {new_cart_item_data["quantity"]} {product.name} to cart. '
                    #                     f'Only {product.available} {product.name} in stock.')
                else:
                    new_cart_item_data.append(CartItem(cart_id, **new_cart_item_data)) 
            else:
                return (-1,new_cart_item_data['product_id']) #means product does not exists
    cart.items.extend(new_cart_items)
    cart.modified_at = datetime.utcnow()
    
    # below is an alternate way to perform the same function without getting from from db first
    # db.session.add_all(new_cart_items)
    # Cart.query.where(Cart.id == cart_id).update(dict(modified_at=datetime.utcnow()))
    db.session.commit()
    return new_cart_items


def update_cart(cart_id: int, new_cart_data: dict):
    '''update the cart's line item quantities, note, or status. '''

    cart = get_cart(cart_id)
    if cart:
        for attribute, value in new_cart_data.items():
            match attribute:
                case 'status':
                    cart.status = value
                case 'notes':
                    cart.notes = value
                case 'updates': #updates is a dict, i.e. {product_id: quantity}
                    for cart_item in cart.items:
                        # cart_item.quantity = value.pop(cart_item.product_id,cart_item.quantity)
                        if cart_item.product_id in value:
                            product = product_access.get_product(cart_item.product_id)
                            new_quantity = value.pop(cart_item.product_id)
                            if new_quantity==0: #new_quantity==0
                                cart.items.remove(cart_item)
                            elif product.available < 1:
                                # raise ValueError(f'The product \'{product.name}\' is already sold out.')
                                return (1,product)
                            elif new_quantity > product.available:
                                return (2,product)
                                # raise ValueError(f'Cannot add {new_quantity} {product.name} to cart. '
                                #                     f'Only {product.available} {product.name} in stock.')
                            else:
                                cart_item.quantity = new_quantity
                    
                    #add item to cart if not already in cart
                    # new_cart_items = [CartItem(cart_id,product_id,quantity) for product_id,quantity in value.items() if quantity > 0]
                    new_cart_items =[]
                    for product_id, quantity in value.items():
                        if quantity>0: #if quantity is zero don't add it to cart
                            product = product_access.get_product(product_id)
                            if product: # if product exists
                                if product.available < 1:
                                    return (1,product)
                                    # raise ValueError(f'The product {product.name} is already sold out.')
                                elif quantity > product.available:
                                    return (2,product)
                                    # raise ValueError(f'Cannot add {quantity} {product.name} to cart. '
                                    #                     f'Only {product.available} {product.name} in stock.')
                                else:
                                    new_cart_items.append(CartItem(cart_id, product_id, quantity))
                            else:
                                return (-1,product_id) #means product does not exists
                    cart.items.extend(new_cart_items)
        cart.modified_at = datetime.utcnow()
        db.session.commit()
    return cart    


def update_cart_item(cart_id: int, product_id:int , quantity:int):
    '''Updates the quantity of an item in a cart'''
    # result = CartItem.query.options(db.joinloaded(CartItem.product)).update(dict(quantiy=quantity)).where(
    #     db.and_(
    #         Carart_id==customer_id,
    #         CartItem.product_id==product_id,
    #     )
    # ).one() #maybe i'll want to change this to fetch
    cart_item = get_cart_item(cart_id,product_id)
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
    return cart_item


def clear_cart(cart_id:int):
    '''delete all cart items from a cart'''
    cart = get_cart(cart_id)
    cart.items.clear()
    # result = CartItem.query.delete(synchronize='evaluate').where(
    #     CartItem.cart_id==cart_id
    # ).all() #maybe i'll want to change this to fetch
    cart.modified_at = datetime.utcnow() 
    db.session.commit()
    return cart


def delete_cart_item(cart_id:int, product_id:int):
    '''delete a single cart item'''
    result = CartItem.query.where(
        db.and_(
            CartItem.cart_id==cart_id,
            CartItem.product_id==product_id
        )
    ).delete(synchronize='evaluate').one() #maybe i'll want to change this to fetch
    db.session.commit()
    return result
    

def delete_cart(cart_id:int):
    '''delete cart by cart ID'''
    result = Cart.query.where(
        Cart.id==cart_id
    ).delete(synchronize='evaluate').one()
    db.session.commit()
    return result