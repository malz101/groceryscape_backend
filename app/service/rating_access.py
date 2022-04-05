from app import db
from app.database.models import CustomerProductRating


def create_rating(customer_id, product_id, rating):
    '''add customer rating for product to database and returns a rating object.'''
    rating = CustomerProductRating(customer_id, product_id, rating)
    db.session.add(rating)
    db.session.commit()
    return rating


def get_customer_rating_for_product(customer_id, product_id):
    '''returns customer rating for a specific product by id'''
    customer_rating = CustomerProductRating.query.where(
        db.and_(
            CustomerProductRating.customer_id==customer_id,
            CustomerProductRating.product_id==product_id
        ).one()
    )
    return customer_rating


def update_customer_rating_for_product(customer_id,product_id,rating):
    '''updates customer rating for product and returns the updated rating'''
    # result = CustomerProductRating.query.options(db.joinloaded(CustomerProductRating.product)).update(dict(rating=rating)).where(
    #     db.and_(
    #         CustomerProductRating.customer_id==customer_id,
    #         CustomerProductRating.product_id==product_id,
    #     )
    # ).one() #maybe i'll want to change this to fetch
    customer_rating_for_product = get_customer_rating_for_product(customer_id,product_id)
    if customer_rating_for_product:
        customer_rating_for_product.rating = rating
    db.session.commit()
    return rating


def get_all_customer_rating_for_products():
    ratings = CustomerProductRating.query.all()
    return ratings