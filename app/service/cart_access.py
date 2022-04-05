from multiprocessing import synchronize
from app.database.models import CartItem, Product
from app import db



def add_cart_item(customer_id, product_id, quantity):
    """add item to cart, returns a cart item object"""
    cart_item = CartItem(customer_id, product_id, quantity)
    db.session.add(cart_item)
    db.session.commit()
    return cart_item


def get_cart(customer_id):
    '''returns a customers cart items with products in cart loaded'''
    cart = CartItem.query.options(db.joinedload(CartItem.product)).where(CartItem.customer_id==customer_id).all()
    return cart


def get_cart_items(customer_id):
    '''returns a customers cart items without in products in cart loaded'''
    cart = CartItem.query.where(CartItem.customer_id==customer_id).all()
    return cart


def get_cart_item(customer_id, prodcut_id):
    '''get a single cart item without corresponding product loaded'''
    cart_item = CartItem.query.where(
        db.and_(
            CartItem.customer_id==customer_id,
            CartItem.product_id==prodcut_id
        )
    ).one()
    return cart_item


def get_cart_item_with_product(customer_id, prodcut_id):
    '''get a single cart item with corresponding product loaded'''
    cart_item = CartItem.query.options(db.joinloaded(CartItem.product).where(
        db.and_(
            CartItem.customer_id==customer_id,
            CartItem.product_id==prodcut_id
        )
    )).one()
    return cart_item


def update_cart_item(customer_id, product_id, quantity):
    '''Updates the quantity of an item in user cart'''
    # result = CartItem.query.options(db.joinloaded(CartItem.product)).update(dict(quantiy=quantity)).where(
    #     db.and_(
    #         CartItem.customer_id==customer_id,
    #         CartItem.product_id==product_id,
    #     )
    # ).one() #maybe i'll want to change this to fetch
    cart_item = get_cart_item(customer_id,product_id)
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()
    return cart_item


def delete_cart_item(customer_id, product_id):
    '''delete a single cart item'''
    result = CartItem.query.delete(synchronize=False).where(
        db.and_(
            CartItem.customer_id==customer_id,
            CartItem.product_id==product_id
        )
    ).one() #maybe i'll want to change this to fetch
    db.session.commit()
    return result
    

def delete_cart(customer_id):
    '''delete all cart items for specified user'''
    result = CartItem.query.delete(synchronize=False).where(
        CartItem.customer_id==customer_id
    ).all()
    db.session.commit()
    return result
