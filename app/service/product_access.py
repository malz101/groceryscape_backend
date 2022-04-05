import os
import random
import numpy as np
from flask import current_app
from werkzeug.utils import secure_filename
from app import db
from app.database.models import Product, ProductAvgRatingMV, ProductCategory,\
     TotalProductOrderedLastThreeMonthsMV, PairsofProductsOrderedTogetherMV,\
         TotalofProductOrderedbyCustomerMV
from app.service import rating_access, customer_access, cart_access

# def addGrocery( request):

#     try:
#         getParam = self.getRequestType(request)
#         name = getParam('grocery_name')
#         description = getParam('description')
#         quantity = getParam('quantity')
#         price = getParam('price')
#         units = getParam('units')
#         unit_weight = getParam('unit_weight')
#         category = getParam('category')
#         photo = getParam('photo')

#         filename = secure_filename(photo.filename)
#         photo.save(os.path.join(
#             current_app.config['UPLOAD_FOLDER'], filename
#         ))


#         """validate the data"""

#         """add grocery item to stock"""
#         grocery = self.grocery_access.create_grocery(name, description, int(quantity), units, float(price), float(unit_weight),category, filename)
#         if grocery:
#             return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery, None)}}, 200
#         else:
#             return {'msg':'request to create new grocery item failed', 'error':'create-0001'}, 404
#     except Exception as e:
#         print(e)
#         return {'msg':'request failed', 'error':'ise-0001'}, 500


# def updateGrocery(grocery_id,request):

#     try:
#         getParam = self.getRequestType(request)
#         # groceryId = getParam('grocery_id')
#         attribute = getParam('attribute')
#         value = getParam('value')

#         '''validate and sanitize data'''

#         '''perform update'''
#         grocery = self.grocery_access.updateGrocery(grocery_id, attribute, value)
#         if grocery:
#             rating = self.rating_access.getItemRating(grocery.id)
#             return {'msg':'success', 'data':{'grocery':self.__getGroceryDetails(grocery,rating)}}, 200

#         else:
#             return {'msg':'update failed', 'error':'create-0001'}, 404
#     except Exception as e:
#         print(e)
#         return {'msg':'request failed', 'error':'ise-0001'}, 500


# def deleteGrocery( grocery_id):

#     try:
#         # getParam = self.getRequestType(request)
#         # groceryId = getParam('grocery_id')

#         '''validate and sanitize data'''

#         '''remove grocery from db'''
#         products = self.grocery_access.removeGroceryItem(int(grocery_id))
#         response = []
#         if products:
#             for grocery in products:
#                 rating = self.rating_access.getItemRating(grocery.id)
#                 response.append(self.__getGroceryDetails(grocery, rating))
#             return {'msg':'success', 'data':{'products':response}}, 200
#         else:
#             return {'msg':'no products in stock', 'data':{}}, 200
#     except Exception as e:
#         print(e)
#         return {'msg':'request failed', 'error':'ise-0001'}, 500


def get_products(name='', brand='', description='', categories=[]):
    '''return products filtered by specific criteria'''
    name = f'%{name}%' if name else name

    brand = f'%{brand}%' if brand else brand

    # select p.* from product p 
    #     where p.id in (
    #         select distinct product_id from product_category where product_category.category_id in categories) as products_in_categories pic
    #     ) and ... and ...

    description = f'%{description}%' if description else description
    
    subquery = ProductCategory.query.with_entities(ProductCategory.product_id).where(ProductCategory.catergory_id.in_(categories)).distinct().subquery()
    
    products = Product.query.where(
            db.and_(
                Product.name.ilike(name),
                Product.brand.ilike(brand),
                Product.description.ilike(description),
                Product.brand.ilike(brand),
                Product.id.in_(subquery) if categories else Product.id.not_in(subquery)
            )
        ).all()
    return products


def get_products_in_list(product_ids: list):
    '''returns a list of products associated with the products IDs provided'''
    products = Product.query.where(Product.id.in_(product_ids)).all()
    return products



def get_product(product_id):
    '''returns a single product matched by the id provided'''
    product = Product.query.where(Product.id==product_id).one()
    return product

# def get_avg_rating(product_id):
#     '''returns the all time average rating for a product'''
#     avg_rating = db.session.query(ProductAvgRatingMV)


def get_top_rated_products(num_to_select):
    '''return a specified number of top rated products'''
    top_rated_products = Product.query.join(Product.avg_rating).where(ProductAvgRatingMV.num_customers > 1000).order_by(db.desc(ProductAvgRatingMV.avg_rating)).limit(num_to_select).all()
    return random.sample(top_rated_products, num_to_select)
    
    #select * from (select * from product_avg_rating where num_customers > 1000) as most_rated_items) limit 50 order by rating desc
    #ItemTotalRating.query.order_by(ItemTotalRating.coefficient.desc()).limit(50).all()                           # set the number to select here.


def get_popular_products(num_to_select):
    '''return select number of the most sold products'''
    popular_products = Product.query.join(
        TotalProductOrderedLastThreeMonthsMV, Product.id==TotalProductOrderedLastThreeMonthsMV.product_id
        ).order_by(db.desc(TotalProductOrderedLastThreeMonthsMV.total)).limit(num_to_select).all()
    return popular_products


def get_freq_bought_with(product_id, num_to_select):
    """ Accepts a product_id and returns a sorted
        list of products with the frequency of occurence """
    # select p.* from product p 
    # join pairs_of_products_ordered_together popot on p.id=popot.product2_id
    # where popot.product1_id = product_id

    #I have to do the below query twice because the order in which the join is made matters, as the pairs are stored like (p1,p2, total),
    #hence if only one join is done of p1, it would only return the p2s paired with the p1s but
    #that wouldn't be true for the opposite (i.e) no paired products would be returned if the product looking for is only in the p2 coulmn
    products_bought_with = Product.query.join(PairsofProductsOrderedTogetherMV, Product.id==PairsofProductsOrderedTogetherMV.product2_id).where(
        PairsofProductsOrderedTogetherMV.product1_id==product_id 
    ).order_by(db.desc(PairsofProductsOrderedTogetherMV.count)).limit(num_to_select).all()

    # products_bought_with+= Product.query.join(PairsofProductsOrderedTogetherMV, Product.id==PairsofProductsOrderedTogetherMV.product1_id).where(
    #     PairsofProductsOrderedTogetherMV.product2_id==product_id 
    # ).all()
    
    # products_bought_with.sort(key=lambda p: p, reverse=True)
    return products_bought_with


def get_freq_bought_with_in_list(product_ids, num_to_select):
    """ Accepts a list of grocery IDs and returns a sorted
        list of pairs with the frequency of occurence """
    # select p.* from product p 
    # join pairs_of_products_ordered_together popot on p.id=popot.product2_id
    # where popot.product1_id = product_id
    # gids = set()
    # gids.update(product_ids)

    pairs = db.session.query(PairsofProductsOrderedTogetherMV).where(
        PairsofProductsOrderedTogetherMV.product1_id.in_(product_ids)
        ).order_by(
            PairsofProductsOrderedTogetherMV.total
        ).limit(num_to_select).all()
    
    
    pairDict = {}
    for p in pairs:
        # if (p.product1_id in product_ids):
        try:
            pairDict[p.product1_id][p.product2_id] = p.count
        except KeyError:
            pairDict[p.product1_id] = {p.product2_id: p.count}


    pairFreq = []
    for g1, pairCnt in pairDict.items():
        for g2, freq in pairCnt.items():
            pairFreq.append((g1, g2, freq))
    pairFreq.sort(key=lambda p: p[2], reverse=True)

    return list(map(lambda p: p[1], pairFreq[:num_to_select]))


def get_customer_recommendations(customer_id, num_to_select):
    """ Uses a Pearson product-moment correlation coefficient matrix
        to determine the similarity among customers based on preferences
        specified by ratings then by the amount of items purchased over
        the lifetime of the account. """

    def getTotalAmtPurchased(customer_id=None):
        """ Returns the total amount of each item a customer has purchased \
            over the lifetime of the account. If a list of IDs is provided \
            then it returns the total amount purchased for all those customers. \
            If an empty list is passed then it returns the total purchased for \
            all customers in the system """

        quantity_dict = {}
        product_id_set = set()
        quantities = []
        if (type(customer_id) == int):
            quantities = db.session.query(TotalofProductOrderedbyCustomerMV).\
                    where(TotalofProductOrderedbyCustomerMV.customer_id == customer_id).all()
            quantity_dict[customer_id] = {}
            for q in quantities:
                product_id_set.add(q.product_id)
                quantity_dict[customer_id][q.product_id] = q.total
        else:
            if (customer_id == None):
                quantities = TotalofProductOrderedbyCustomerMV.query.all()
            elif (type(customer_id) == list):
                quantities = db.session.query(TotalofProductOrderedbyCustomerMV).\
                        where(TotalofProductOrderedbyCustomerMV.customer_id.in_(customer_id)).all()

            for q in quantities:
                product_id_set.add(q.product_id)
                try:
                    quantity_dict[q.customer_id][q.product_id] = q.total
                except KeyError:
                    quantity_dict[q.customer_id] = {q.product_id: q.total}
        return quantity_dict, list(product_id_set)


    def createRatingsDictAndProductIDList(ratings):
        """ Returns a dict of customer_id keys with a sub-dictionary as value
            each key in the sub-dict represents a product id and the value is
            the customer rating for the product.

            i.e ratings_dict = {customer_id: {product1_id: rating, product2_id:rating,...},..}

            Also returns a list of product ids

            Return format:
            ratings_dict, product_id_lst
             """
        ratings_dict = {}
        product_id_set = set()
        for rating in ratings:
            product_id_set.add(rating.product_id)
            # Organizes the data in a dictionary indexed by customerID
            try:
                ratings_dict[rating.customer_id][rating.product_id] = rating.rating
            except KeyError:
                ratings_dict[rating.customer_id] = {}
                ratings_dict[rating.customer_id][rating.product_id] = rating.rating
        
        return ratings_dict, list(product_id_set)

    def genMatrix(id, rowIndexLst, colIndexLst, custDict, defaultVal):
        """ Converts a 2D dictionary into a 2D list """

        data = []
        cnt = 0
        for c in rowIndexLst:
            if (c == id):
                customer_idx = cnt

            data.append([])
            for iid in colIndexLst:
                try:
                    data[cnt].append(custDict[c][iid])
                except KeyError:
                    data[cnt].append(defaultVal)
            cnt += 1
        return (data, customer_idx)

    def getMostSimilar(element, matrix, indexToIdMap):
        """ Uses Pearson product-moment correlation coefficient matrix
            to determine the most similar elements of a matrix """

        closest = []
        for i in range(len(matrix)):
            correlMatrix = np.corrcoef(element, matrix[i])
            correl = correlMatrix[0][1]
            if ((correl < 1) and (correl > 0.75)):
                closest.append((indexToIdMap[i], correl))
        closest.sort(key=lambda x: x[1], reverse=True)
        closest = list(map(lambda x: x[0], closest))
        return closest



    ratings = rating_access.get_all_customer_rating_for_products()
    ratings_dict, product_id_lst = createRatingsDictAndProductIDList(ratings)

    # Find similar customers based on ratings provided  
    similar_customers = []
    average_perception = 2.5
    if (customer_id in ratings_dict): # ie: if the customer has rated something in the past
        # Ratings range from 1 to 5. Ratings < 2.5 are thought to be
        # negative while ratings above 2.5 are thought to be positive
        # hence using a default value of 2.5 implies an average or
        # indifferent perception of an item
        customer_id_lst = list(ratings_dict.keys())
        # product_id_lst = getColumns(ratings_dict)
        ratings_lst, customer_idx = genMatrix(customer_id, customer_id_lst, product_id_lst, ratings_dict, average_perception)
        similar_customers = getMostSimilar(ratings_lst[customer_idx], ratings_lst, customer_id_lst)

    # If similar customers were found, search for customers with similar
    # order history from that set of customers, otherwise compare all
    # customers to find customers that have a similar pattern of items
    # purchased over the lifetime of the account
    quantity_dict, product_id_lst = getTotalAmtPurchased(similar_customers)
    if (customer_id in quantity_dict): # ie: if the customer has ordered something in the past
        customer_id_lst = list(quantity_dict.keys())
        # product_id_lst = getColumns(quantity_dict)
        quantity_lst, customer_idx = genMatrix(customer_id, customer_id_lst, product_id_lst, quantity_dict, 0)
        similar_customers = getMostSimilar(quantity_lst[customer_idx], quantity_lst, customer_id_lst)

    recommended_items = set()
    cart_items = cart_access.get_cart_items(customer_id)
    if (type(cart_items) == list):
        cart_items = set(list(map(lambda i: i.item_id, cart_items)))
    else:
        cart_items = set()

    # Extracts a list of items bought by similar customers that haven't
    # been bought by the current customer. Items in the customers cart_items
    # are also ignored
    for c in similar_customers[:15]:
        for gid in quantity_dict[c].keys():
            try:
                if quantity_dict[customer_id][gid]:
                    pass
            except KeyError:
                if (not (gid in cart_items)):
                    recommended_items.add(gid)

    # Pad the rest with items frequently bought together.
    if (len(recommended_items) < num_to_select):
        products = set(cart_items)
        if (customer_id in ratings_dict):
            # Finds all items that the customer has rated positively
            for g in ratings_dict[customer_id].keys():
                if (ratings_dict[customer_id][g] > average_perception):
                    products.add(g)
        elif (customer_id in quantity_dict):
            # Adds all items that the customer has ever bought
            products.update(quantity_dict[customer_id].keys())

        pairFreq = get_freq_bought_with_in_list(list(products), num_to_select)
        i = 0
        while ((len(recommended_items) < num_to_select) and (i < len(pairFreq))):
            recommended_items.add(pairFreq[i])
            i += 1

    # Pad the list with the most purchased items
    # if (len(recommended_items) < num_to_select):
    #     popularItems = get_popular_products(num_to_select)
    #     i = 0
    #     while ((len(recommended_items) < num_to_select) and (i < len(popularItems))):
    #         recommended_items.add(popularItems[i])
    #         i += 1

    return get_products_in_list(recommended_items)
