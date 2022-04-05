from marshmallow import Schema, fields, validate, post_load, post_dump

class UserSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    telephone = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    street = fields.String(required=True)
    town = fields.String(required=True)
    parish = fields.String(required=True)
    time_created = fields.DateTime()
    is_active = fields.Boolean()
    
    class Meta:
        load_only = ['password']


class CustomerSchema(UserSchema):
    gender = fields.String(required=True)
    email = fields.Email(required=True)
    email_confirmed = fields.Boolean()

    # order = 
    #relationships
    # orders = fields.List(fields.Nested(lambda: OrderSchema(exclude=('customer',))))
    # cart = fields.List(fields.Nested(lambda: CartItemSchema(exclude=('customer',))))
    # ratings = fields.List(fields.Nested(lambda: CustomerProductRatingSchema(exclude=('customer',))))
    # count_of_product_prev_ordered = fields.List(fields.Nested(lambda: TotalofProductOrderedbyCustomerMVSchema()))
    

class EmployeeSchema(UserSchema): #a new table called priveledges or access rights needs to be created sometime in the future
    role = fields.String(required=True)
    salary = fields.Decimal(10,2)

    # represent the payment collected an employee (many to one relationship)
    # payments_collected = fields.List(fields.Nested(lambda: PaymentSchema(exclude=('employee',))))
    # checkouts = fields.List(fields.Nested(lambda: OrderSchema(exclude=('employee',))))


class ProductSchema(Schema):
    id = fields.Integer()
    brand = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    inventory = fields.Integer(required=True)
    available = fields.Integer()
    size = fields.String(required=True)
    unit_price = fields.Decimal(10,2)
    unit_weight = fields.Decimal(10,2)
    photo = fields.Url()
    sku = fields.String(required=True)
    package_type = fields.String()
    taxable = fields.Boolean(required=True)
    time_created = fields.DateTime()
    category_ids = fields.List() #list of category ids to filter products by

    # relationships (referenced by)
    # order_lines = fields.List(fields.Nested(lambda: OrderLineSchema(exclude=('product',))))
    # carts = fields.List(fields.Nested(lambda: CartItemSchema(exclude=('product',))))
    # customer_ratings = fields.List(fields.Nested(lambda: CustomerProductRatingSchema(exclude=('product',))))
    categories = fields.List(fields.Nested(lambda: ProductCategorySchema(exclude=('product',))))
    #I wanted to define the relationships below however they cause a reference error on db migration
    #as the views aren't added to the 'db creation list' for migrations
    avg_rating = fields.List(fields.Nested(lambda: ProductAvgRatingMVSchema))

    total_product_ordered_last_three_months= fields.List(fields.Nested(lambda: TotalProductOrderedLastThreeMonthsMVSchema))

    class Meta:
        load_only = ['category_ids']
        dump_only = ['categories','avg_rating','total_product_ordered_last_three_months']


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    status = fields.Boolean(required=True)

    #relationships
    # products = fields.List(fields.Nested(lambda: ProductCategorySchema(exclude=('category',))))
    

class ProductCategorySchema(Schema):
    product_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)

    #relationships
    products = fields.List(fields.Nested(lambda: ProductSchema(exclude=('categories',))))
    # category = fields.Nested(lambda: CategorySchema(exclude=('products',)))


class OrderSchema(Schema):
    #columns 
    id = fields.Integer()
    customer_id = fields.Integer()
    time_created = fields.DateTime()
    status = fields.String()
    payment_type = fields.String()
    billing_first_name = fields.String(required=True)
    billing_last_name = fields.String(required=True)
    billing_telephone = fields.String(required=True)
    billing_street = fields.String(required=True)
    billing_town = fields.String(required=True)
    billing_parish = fields.String(required=True)
    shipping_first_name = fields.String(required=True)
    shipping_last_name = fields.String(required=True)
    shipping_telephone = fields.String(required=True)  
    shipping_time_slot_id = fields.Integer(required=True)
    # shipping_time_slot_start = db.Column(db.Time, nullable=False)    
    # shipping_time_slot_end = db.Column(db.Time, nullable=False) 
    # shipping_date = db.Column(db.Date, nullable=False)
    shipping_street = fields.String(required=True)
    shipping_town = fields.String(required=True)
    shipping_parish = fields.String(required=True)
    shipping_fee = fields.Decimal(10,2)
    delivered_time = fields.DateTime()
    checkout_by = fields.Integer()
    notes = fields.String()

    # relationship (references)
    # customer = fields.Nested(lambda: CustomerSchema())
    # employee = fields.Nested(lambda: EmployeeSchema())
    time_slot = fields.Nested(lambda: ShippingTimeSlotSchema(exclude=('orders',)))

    # relationships (referenced by)
    order_lines = fields.List(fields.Nested(lambda: OrderLineSchema(exclude=('order',))))
    # order_lines_summary = fields.Method(serialize='get_order_lines_summary')
    payments = fields.List(fields.Nested(lambda: PaymentSchema(exclude=('order',))))

    billing = fields.Function(lambda obj: {
        'first_name': obj.billing_first_name,
        'last_name': obj.billing_last_name,
        'telephone': obj.billing_telephone,
        'street': obj.billing_street,
        'town': obj.billing_town,
        'parish': obj.billing_parish,
    })
    shipping = fields.Function(lambda obj: {
        'first_name': obj.shipping_first_name,
        'last_name': obj.shipping_first_name,
        'street': obj.shipping_street,
        'town': obj.shipping_town, 
        'parish': obj.shipping.parish, 
        'fee': obj.shipping_fee,
        'time_slot': {
            'id': obj.shipping_time_slot_id,
            'start_time': obj.time_slot.start_time,
            'end_time': obj.time_slot.end_time   
        }     
    })

    @post_dump(many=True)
    def cost_summary(self,data,many,**kwargs):
        ####-----SERIALIZE ORDER ITEMS------######
        def add_cost_summary_to_order_line(order):
            subtotal_price = 0
            total_tax=0
            price_before_shipping_fee = 0
            total_weight = 0
            item_count = 0
            discounts = []
            order_lines =[]

            #order level
            for order_line in order:
                subtotal_price+= order_line['line_subtotal_price']
                total_tax+= order_line['line_tax']
                price_before_shipping_fee += order_line['line_total_price']
                total_weight += order_line['line_weight']
                item_count += order_line['quantity']        

            order.update({
                'subtotal_price':subtotal_price,
                'total_tax': total_tax,
                'price_before_shipping_fee': price_before_shipping_fee,
                'total_price': price_before_shipping_fee + order['shipping']['fee'],
                'total_weight': total_weight, 
                'item_count':item_count,
                'order_lines': order_lines,
                'discounts': discounts
            })

        if many:
            for order in data:
                add_cost_summary_to_order_line(order)
        else:
            add_cost_summary_to_order_line(data)
        return data



    class Meta:
        dump_only = ['billing', 'shipping','order_lines','payments']
        load_only = ['billing_first_name','billing_last_name','billing_telephone',
        'billing_street','billing_town','billing_parish','shipping_first_name',
        'shipping_last_name','shipping_telephone','shipping_time_slot_id',
        'shipping_street','shipping_town','shipping_parish','shipping_fee']


class OrderLineSchema(Schema):
    order_id = fields.Integer()
    product_id = fields.Integer(required=True)
    product_name = fields.String(required=True)
    product_sku = fields.String(required=True)
    unit_price = fields.Decimal(10,2)
    unit_weight = fields.Decimal(10,2)
    tax_rate = fields.Decimal(10,2) #change from total tax
    quantity = fields.Integer(required=True)
    brand = fields.String(required=True)
    package_type = fields.String(required=True)
    photo = fields.String(required=True)
    line_weight = fields.Function(lambda obj: obj.unit_weight*obj.quantity)
    line_subtotal_price = fields.Function(lambda obj: obj.unit_price*obj.quantity)
    # relationships 
    #order = fields.Nested(lambda: OrderSchema(exclude=('order_lines',)))
    #product = fields.Nested(lambda: ProductSchema())

    @post_dump(pass_many=True)
    def add_fields(self,data,many,**kwargs):
        def add_fields_to_order_line(order_line):
            order_line['line_tax'] = order_line['line_subtotal_price'] * order_line['tax_rate']
            order_line['line_total_price'] = order_line['line_tax'] + order_line['line_subtotal_price']
            order_line['line_level_discount_allocations']= [] #check shopify cart api  
        
        if many:
            for order_line in data:
                add_fields_to_order_line(order_line)
  
        else:
            add_fields_to_order_line(data)   
        return data
     


class CartItemSchema(Schema):
    customer_id = fields.Integer()
    product_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    product = fields.Nested(lambda: ProductSchema())

    line_price = fields.Function(lambda obj: obj.product.unit_price)
    line_subtotal_price = fields.Function(lambda obj: obj.quantity*obj.product.unit_price)
    line_weight = fields.Function(lambda obj: obj.product.unit_weight * obj.quantity)    
    # customer = fields.Nested(lambda: CustomerSchema(exclude=('cart',)))


# class LineItemSchema(Schema):
#     product = fields.Nested(lambda: ProductSchema())
#     line_price = fields.Function(lambda obj: obj.product.unit_price)
#     line_subtotal_price = fields.Function(lambda obj: obj.quantity*obj.product.unit_price)
#     line_weight = fields.Function(lambda obj: obj.product.unit_weight * obj.quantity)
    # line_level_discount = fields.Function() #check shopify cart api 


class CustomerProductRatingSchema(Schema):
    customer_id = fields.Integer()
    product_id = fields.Integer(required=True)
    rating = fields.Integer(required=True)

    # relationships
    # product = fields.Nested(lambda: ProductSchema())
    # customer = fields.Nested(lambda: CustomerSchema())



class PaymentSchema(Schema):
    #columns
    id = fields.Integer()
    order_id = fields.Integer(required=True)
    time_created =fields.DateTime()
    amount_tendered = fields.Decimal(10,2)
    change = fields.Decimal(10,2)
    intent_id = fields.String()
    recorded_by = fields.Integer()
    type = fields.String(required=True)

    #relatioships
    # employee = fields.Nested(lambda: EmployeeSchema())
    order = fields.Nested(lambda: OrderSchema(exclude=('payments',)))



class ParishSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    shipping_rate = fields.Decimal(10,2)

    
    time_slots = fields.List(fields.Nested(lambda: ShippingTimeSlotSchema(exclude=('parish',))))
    default_config_time_slot = fields.List(fields.Nested(lambda: DefaultConfigShippingTimeSlotSchema(exclude=('parish',)))) 




class DefaultConfigShippingTimeSlotSchema(Schema):
    parish_id = fields.Integer(required=True)
    day = fields.Integer(required=True)
    time_slot_interval = fields.TimeDelta(required=True)
    max_per_slot = fields.Integer(required=True)

    #relationships
    parish = fields.Nested(lambda: ParishSchema(exclude=('default_config_time_slot',)))



class ShippingTimeSlotSchema(Schema):
    id = fields.Integer()
    parish_id = fields.Integer(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    num_space_available = fields.Integer(required=True)
    is_active = fields.Boolean()


    #relationships
    parish = fields.Nested(lambda: ParishSchema(exclude=('time_slots',)))
    orders = fields.List(fields.Nested(lambda: OrderSchema(exclude=('time_slot',))))

    

class TaxSchema(Schema):
    tax = fields.String(required=True)
    rate = fields.Decimal(5,5)


class ProductRecommendationsSchema(Schema):
    num_to_select = fields.String(required=True)
    product_id = fields.Integer(required=True)

#####################################################
#                       Views                       #
#####################################################

class ProductAvgRatingMVSchema(Schema):
    product_id = fields.Integer()
    avg_rating = fields.Decimal(10,2)           
    num_customers = fields.Integer()
    coefficient = fields.Decimal(10,10) 



class TotalProductOrderedLastThreeMonthsMVSchema(Schema):
    product_id = fields.Integer()
    total = fields.Decimal(10,2)


class PairsofProductsOrderedTogetherMVSchema(Schema):
    product1_id = fields.Integer()
    product2_id = fields.Integer()
    count = fields.Integer()


class TotalofProductOrderedbyCustomerMVSchema(Schema):
    customer_id = fields.Integer()
    product_id = fields.Integer()
    total = fields.Integer()