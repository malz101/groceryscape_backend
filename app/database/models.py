from app import db, encryp
from datetime import datetime, date, timedelta
from .view_factory import MaterializedView, create_mat_view, refresh_all_mat_views
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import aliased

class Customer(db.Model):
    __tablename__ = 'customer'

    #columns
    id = db.Column(db.Integer, primary_key=True, index=True)
    _first_name = db.Column('first_name',db.LargeBinary, nullable=False)
    _last_name = db.Column('last_name',db.LargeBinary, nullable=False)
    _gender = db.Column('gender',db.LargeBinary, nullable=False)
    _telephone = db.Column('telephone',db.LargeBinary, nullable=False)
    _email = db.Column('email',db.LargeBinary, nullable=False, unique=True, index=True)
    _password = db.Column('password',db.LargeBinary, nullable=False)
    _street = db.Column('street',db.LargeBinary)
    _town = db.Column('town',db.LargeBinary, nullable=False)
    _parish = db.Column('parish',db.LargeBinary, nullable=False)
    email_confirmed = db.Column(db.Boolean,nullable=False, default=True)#remember to change back to false
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean,nullable=False, default=True)#remember to change back to false

    #relationships
    orders = db.relationship('Order', back_populates='customer', passive_deletes=True, lazy='noload')
    carts = db.relationship('Cart', back_populates='customer', passive_deletes=True, lazy='noload')
    ratings = db.relationship('CustomerProductRating', back_populates='customer', passive_deletes=True, lazy='noload')
    # count_of_product_prev_ordered = db.relationship('TotalofProductOrderedbyCustomerMV', backref='customer',
    #                     uselist=True, # makes it a one-to-many relationship, this is the default setting
    #                     primaryjoin='Customer.id==TotalofProductOrderedbyCustomerMV.customer_id',
    #                     foreign_keys='TotalofProductOrderedbyCustomerMV.customer_id', lazy='select')
    count_of_product_prev_ordered = None

    def __init__(self, first_name, last_name, telephone, email, gender, password,street, town, parish):
        self.first_name = first_name
        self.last_name = last_name
        self.telephone = telephone
        self.gender = gender
        self.email = email
        self.password = password
        self.street = street
        self.town = town
        self.parish = parish
    

    @property
    def first_name(self):
        """Return the first name of customer"""
        return encryp.decrypt(self._first_name)
    @first_name.setter
    def first_name(self, first_name):
        """Set value of first name"""
        self._first_name = encryp.encrypt(first_name)
    

    @property
    def last_name(self):
        """Returns the last name of the customer"""
        return encryp.decrypt(self._last_name)
    @last_name.setter
    def last_name(self,last_name):
        """Sets value of last name"""
        self._last_name = encryp.encrypt(last_name)

    @property
    def telephone(self):
        return encryp.decrypt(self._telephone)
    @telephone.setter
    def telephone(self,telephone):
        self._telephone = encryp.encrypt(telephone)

    @property
    def gender(self):
        return encryp.decrypt(self._gender)
    @gender.setter
    def gender(self,gender):
        self._gender = encryp.encrypt(gender)

    @property
    def email(self):
        return encryp.decrypt(self._email)
    @email.setter
    def email(self,email):
        self._email = encryp.encrypt(email)
    
    @property
    def password(self):
        return encryp.decrypt(self._password)
    @password.setter
    def password(self,password):
        self._password = encryp.encrypt(generate_password_hash(password, method='pbkdf2:sha256:310000'))
    
    @property
    def street(self):
        return encryp.decrypt(self._street)
    @street.setter
    def street(self,street):
        self._street = encryp.encrypt(street)

    @property
    def town(self):
        return encryp.decrypt(self._town)
    @town.setter
    def town(self,town):
        self._town = encryp.encrypt(town)
    
    @property
    def parish(self):
        return encryp.decrypt(self._parish)
    @parish.setter
    def parish(self,parish):
        self._parish = encryp.encrypt(parish)


class Employee(db.Model): #a new table called priveledges or access rights needs to be created sometime in the future
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, index=True)
    _first_name = db.Column('first_name',db.LargeBinary, nullable=False)
    _last_name = db.Column('last_name',db.LargeBinary, nullable=False)
    _telephone = db.Column('telephone',db.LargeBinary, nullable=True)
    _email = db.Column('email',db.LargeBinary, nullable=False, unique=True)
    _password = db.Column('password',db.LargeBinary, nullable=False)
    _street = db.Column('street',db.LargeBinary, nullable=False)
    _town = db.Column('town',db.LargeBinary, nullable=False)
    _parish = db.Column('parish',db.LargeBinary, nullable=False)
    _role = db.Column('role',db.LargeBinary, nullable=False)
    salary = db.Column(db.Numeric(10,2), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean,nullable=False, default=True)#remember to change back to false

    # represent the payment collected an employee (many to one relationship)
    payments_collected = db.relationship('Payment', back_populates='employee', passive_deletes=True, lazy='noload')
    checkouts = db.relationship('Order', back_populates='employee', passive_deletes=True, lazy='noload')


    def __init__(self, first_name, last_name, telephone, email, password, street, town, parish, role, salary):
        self.first_name = encryp.encrypt(first_name)
        self.last_name = encryp.encrypt(last_name)
        self.telephone = encryp.encrypt(telephone)
        self.email = encryp.encrypt(email)
        self.password = encryp.encrypt(generate_password_hash(password, method='pbkdf2:sha256:310000'))
        self.street = encryp.encrypt(street)
        self.town = encryp.encrypt(town)
        self.parish = encryp.encrypt(parish)
        self.role = encryp.encrypt(role)
        self.salary = salary

    @property
    def first_name(self):
        return encryp.decrypt(self._first_name)
    @first_name.setter
    def first_name(self,first_name):
        self._first_name = encryp.encrypt(first_name)

    @property
    def last_name(self):
        return encryp.decrypt(self._last_name)
    @last_name.setter
    def last_name(self,last_name):
        self._last_name = encryp.encrypt(last_name)
    
    @property
    def telephone(self):
        return encryp.decrypt(self._telephone)
    @telephone.setter
    def telephone(self,telephone):
        self._telephone = encryp.encrypt(telephone)
    
    @property
    def email(self):
        return encryp.decrypt(self._email)
    @email.setter
    def email(self,email):
        self._email = encryp.encrypt(email)
    
    @property
    def password(self):
        return encryp.decrypt(self._password)
    @password.setter
    def password(self,password):
        self._password = encryp.encrypt(generate_password_hash(password, method='pbkdf2:sha256:310000'))

    @property
    def street(self):
        return encryp.decrypt(self._street)
    @street.setter
    def street(self,street):        
        self._street = encryp.encrypt(street)

    @property
    def town(self):
        return encryp.decrypt(self._town)
    @town.setter
    def town(self,town):
        self._town = encryp.encrypt(town)

    @property
    def parish(self):
        return encryp.decrypt(self._parish)    
    @parish.setter
    def parish(self,parish):    
        self._parish = encryp.encrypt(parish)

    @property
    def role(self):
        return encryp.decrypt(self._role) 
    @role.setter
    def role(self,role):
        self._role = encryp.encrypt(role)



class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, index=True)
    brand = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.UnicodeText(), nullable=False)# unique=True)
    inventory = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    unit_weight = db.Column(db.Numeric(10,2), nullable=False)
    photo = db.Column(db.String(100), default='product.jpg')
    sku = db.Column(db.String(50), unique=True, nullable=True)
    package_type = db.Column(db.String(50), nullable=True)
    taxable = db.Column(db.Boolean,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('name', 'size', name='_product_name_size_uc'),)
    
    # relationships (referenced by)
    order_lines = db.relationship("OrderLine", back_populates="product", passive_deletes=True, lazy='noload')
    cart_items = db.relationship("CartItem", back_populates="product", passive_deletes=True, lazy='noload')
    customer_ratings = db.relationship("CustomerProductRating", back_populates="product", passive_deletes=True, lazy='noload')
    categories = db.relationship('ProductCategory', back_populates='product', passive_deletes=True, lazy='noload')

    #I wanted to define the relationships below however they cause a reference error on db migration
    #as the views aren't added to the 'db creation list' for migrations
    # avg_rating = db.relationship('ProductAvgRatingMV', backref='product',
    #                     uselist=False, # makes it a one-to-one relationship
    #                     primaryjoin='Product.id==ProductAvgRatingMV.product_id',
    #                     foreign_keys='ProductAvgRatingMV.product_id', lazy='joined')
    # total_product_ordered_last_three_months= db.relationship('TotalProductOrderedLastThreeMonthsMV', backref='product',
    #                     uselist=False, # makes it a one-to-one relationship
    #                     primaryjoin='Product.id==TotalProductOrderedLastThreeMonthsMV.product_id',
    #                     foreign_keys='TotalProductOrderedLastThreeMonthsMV.product_id') #, lazy='joined') #maybe I want to change this later
                                
    # variants = db.relationship('ProductVariant', back_populates='product', passive_deletes=True)
    avg_rating = None
    total_product_ordered_last_three_months = None

    def __init__(self,brand, name, description,inventory,size, unit_price, weight, category_id,photo,\
                    sku,package_type, taxable):
        self.brand = brand
        self.name = name
        self.description = description
        self.inventory = inventory
        self.available = inventory
        self.size = size
        self.unit_price = unit_price
        self.unit_weight = weight
        self.category_id = category_id
        self.photo = photo
        self.sku = sku
        self.package_type = package_type
        self.taxable = taxable


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.Boolean,nullable=False, default=True)

    #relationships
    products = db.relationship('ProductCategory', back_populates='category', passive_deletes=True, lazy='noload')

    def __init__(self, name,status):
        self.name = name
        self.status = status


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete='CASCADE'), primary_key=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id',ondelete='CASCADE') , primary_key=True, index=True)

    #relationships
    product = db.relationship('Product', back_populates='categories', lazy='noload')
    category = db.relationship('Category', back_populates='products', lazy='noload')


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), primary_key=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _status = db.Column(db.LargeBinary,nullable=False, default=encryp.encrypt('shopping')) #shopping, checkout, paid and abandoned.
    _notes = db.Column('notes',db.LargeBinary, nullable=True)

    #relationships
    customer = db.relationship('Customer',back_populates='carts',lazy='noload')
    items = db.relationship('CartItem', back_populates='cart',passive_deletes=True, lazy='noload')

    def __init__(self,customer_id):
        self.customer_id = customer_id
        self.notes = None
    
    @property
    def status(self):
        return encryp.decrypt(self._status)
    @status.setter
    def status(self,status):
        self._status = encryp.encrypt(status)

    @property
    def notes(self):
        return encryp.decrypt(self._notes)
    @notes.setter
    def notes(self,notes):
        self._notes = encryp.encrypt(notes)


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id',ondelete='CASCADE'), primary_key=True, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete='CASCADE'), primary_key=True, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # relationships (references)
    product = db.relationship('Product', back_populates='carts', lazy='noload') #change relationship name to product or product_product
    cart = db.relationship('Cart', back_populates='items', lazy='noload')

    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id         #change name from product_id to product_id
        self.quantity = quantity
        


class Order(db.Model):
    __tablename__ = 'orders'
    #columns 
    id = db.Column(db.Integer, primary_key=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _status = db.Column(db.LargeBinary,nullable=False,default=encryp.encrypt('pending'))
    _payment_type = db.Column('payment_type',db.LargeBinary,nullable=False)
    _billing_first_name = db.Column('billing_first_name',db.LargeBinary, nullable=False)
    _billing_last_name = db.Column('billing_last_name',db.LargeBinary, nullable=False)
    _billing_telephone = db.Column('billing_telephone',db.LargeBinary, nullable=False)
    _billing_street = db.Column('billing_street',db.LargeBinary, nullable=False)
    _billing_town = db.Column('billing_town',db.LargeBinary, nullable=False)
    _billing_parish = db.Column('billing_parish',db.LargeBinary, nullable=False)
    _shipping_first_name = db.Column('shipping_first_name',db.LargeBinary, nullable=False)
    _shipping_last_name = db.Column('shipping_last_name',db.LargeBinary, nullable=False)
    _shipping_telephone = db.Column('shipping_telephone',db.LargeBinary, nullable=False)    
    shipping_time_slot_id = db.Column(db.Integer, db.ForeignKey('shipping_time_slot.id',ondelete='SET NULL'), nullable=False) 
    # shipping_time_slot_start = db.Column(db.Time, nullable=False)    
    # shipping_time_slot_end = db.Column(db.Time, nullable=False) 
    # shipping_date = db.Column(db.Date, nullable=False)
    _shipping_street = db.Column('shipping_street',db.LargeBinary, nullable=False)
    _shipping_town = db.Column('shipping_town',db.LargeBinary, nullable=False)
    _shipping_parish = db.Column('shipping_parish',db.LargeBinary, nullable=False)
    shipping_fee = db.Column(db.Numeric(10,2), nullable=False)
    delivered_time = db.Column(db.DateTime, nullable=True)
    checkout_by = db.Column(db.Integer, db.ForeignKey('employee.id',ondelete='SET NULL'), nullable=True)# represents a one to many-to-many relationship between employee and orders
    _notes = db.Column('notes',db.LargeBinary, nullable=True)

    # relationship (references)
    customer = db.relationship('Customer', back_populates='orders',lazy='noload')
    employee = db.relationship('Employee', back_populates='checkouts', lazy='noload')
    time_slot = db.relationship('ShippingTimeSlot', back_populates='orders', lazy='noload')

    # relationships (referenced by)
    order_lines = db.relationship("OrderLine", back_populates="order",passive_deletes=True, lazy='noload')
    payments = db.relationship('Payment', back_populates='order', passive_deletes=True, lazy='noload')

    def __init__(self, customer_id,billing_fname, billing_lname,billing_telephone, billing_street,billing_town,billing_parish,\
                    shipping_fname,shipping_lname,shipping_telephone,shipping_date,shipping_time_slot_start,shipping_time_slot_end,\
                    shipping_street,shipping_town,shipping_parish,shipping_fee,notes=None):
        self.customer_id = customer_id
        self.billing_first_name = billing_fname
        self.billing_last_name = billing_lname
        self.billing_telephone = billing_telephone
        self.billing_street = billing_street
        self.billing_town = billing_town
        self.billing_parish = billing_parish
        self.shipping_first_name = shipping_fname
        self.shipping_last_name = shipping_lname
        self.shipping_telephone = shipping_telephone
        self.shipping_date = datetime.strptime(shipping_date,'%Y-%m-%d').date()
        self.shipping_time_slot_start = datetime.strptime(shipping_time_slot_start,'%H:%M:%S').time()
        self.shipping_time_slot_end = datetime.strptime(shipping_time_slot_end,'%H:%M:%S').time()
        self.shipping_street = shipping_street
        self.shipping_town = shipping_town
        self.shipping_parish = shipping_parish
        self.shipping_fee = shipping_fee
        # self.payment_type = payment_type #I feel I should remove this since the payment table would already store it
        self.notes = notes

    @property
    def status(self):
        return encryp.decrypt(self._status)
    @status.setter
    def status(self,status):
        self._status = encryp.encrypt(status)

    @property
    def billing_first_name(self):
        return encryp.decrypt(self._billing_first_name)
    @billing_first_name.setter
    def billing_first_name(self,billing_fname):
        self._billing_first_name = encryp.encrypt(billing_fname)
    
    @property
    def billing_last_name(self):
        return encryp.decrypt(self._billing_last_name)
    @billing_last_name.setter
    def billing_last_name(self,billing_lname):
        self._billing_last_name = encryp.encrypt(billing_lname)

    @property
    def billing_telephone(self):
        return encryp.decrypt(self._billing_telephone)
    @billing_telephone.setter
    def billing_telephone(self,billing_telephone):
        self._billing_telephone = encryp.encrypt(billing_telephone)
    
    @property
    def billing_street(self):
        return encryp.decrypt(self._billing_street)
    @billing_street.setter
    def billing_street(self,billing_street):
        self._billing_street = encryp.encrypt(billing_street)

    @property
    def billing_town(self):
        return encryp.decrypt(self._billing_town)
    @billing_town.setter
    def billing_town(self, billing_town):
        self._billing_town = encryp.encrypt(billing_town)
    
    @property
    def billing_parish(self):
        return encryp.decrypt(self._billing_parish)
    @billing_parish.setter
    def billing_parish(self,billing_parish):
        self._billing_parish = encryp.encrypt(billing_parish)

    @property
    def shipping_first_name(self):
        return encryp.decrypt(self._shipping_first_name)
    @shipping_first_name.setter
    def shipping_first_name(self,shipping_fname):
        self._shipping_first_name = encryp.encrypt(shipping_fname)
    
    @property
    def shipping_last_name(self):
        return encryp.decrypt(self._shipping_last_name)
    @shipping_last_name.setter
    def shipping_last_name(self,shipping_lname):
        self._shipping_last_name = encryp.encrypt(shipping_lname)

    @property
    def shipping_telephone(self):
        return encryp.decrypt(self._shipping_telephone)
    @shipping_telephone.setter
    def shipping_telephone(self,shipping_telephone):
        self._shipping_telephone = encryp.encrypt(shipping_telephone)
    
    @property
    def shipping_street(self):
        return encryp.decrypt(self._shipping_street)
    @shipping_street.setter
    def shipping_street(self,shipping_street):
        self._shipping_street = encryp.encrypt(shipping_street)

    @property
    def shipping_town(self):
        return encryp.decrypt(self._shipping_town)
    @shipping_town.setter
    def shipping_town(self, shipping_town):
        self._shipping_town = encryp.encrypt(shipping_town)
    
    @property
    def shipping_parish(self):
        return encryp.decrypt(self._shipping_parish)
    @shipping_parish.setter
    def shipping_parish(self,shipping_parish):
        self._shipping_parish = encryp.encrypt(shipping_parish)

    @property
    def payment_type(self):
        return encryp.decrypt(self._payment_type)
    @payment_type.setter
    def payment_type(self,payment_type):
        self._payment_type = encryp.encrypt(payment_type)

    @property
    def notes(self):
        return encryp.decrypt(self._notes)
    @notes.setter
    def notes(self,notes):
        self._notes = encryp.encrypt(notes)


class OrderLine(db.Model):
    __tablename__ = 'order_line'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='CASCADE'), primary_key=True, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True,index=True)
    name = db.Column(db.String(100), nullable=True)
    sku = db.Column(db.String(50),nullable=True)
    unit_price = db.Column(db.Numeric(10,2), nullable=False)
    unit_weight = db.Column(db.Numeric(10,2), nullable=False)
    tax_rate = db.Column(db.Numeric(10,2)) #change from total tax
    quantity = db.Column(db.Integer)
    brand = db.Column(db.String(100), nullable=True)
    package_type = db.Column(db.String(50), nullable=True)
    photo = db.Column(db.String(100), default='product.jpg')

    # relationships 
    order = db.relationship("Order", back_populates="order_lines", lazy='noload')
    product = db.relationship("Product", back_populates="order_lines", lazy='noload')

    def __init__(self, order_id, product_id,product_name, product_brand,\
        product_package_type,quantity, product_sku, unit_price, tax_rate,\
            product_unit_weight,photo):
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_brand = product_brand
        self.product_package_type = product_package_type
        self.quantity = quantity
        self.product_sku = product_sku
        self.unit_price = unit_price
        self.tax_rate = tax_rate
        self.product_unit_weight = product_unit_weight
        self.photo = photo


class CustomerProductRating(db.Model):
    __tablename__ = 'customer_product_rating'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id',ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete='CASCADE'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    # relationships
    product = db.relationship('Product', back_populates='customer_ratings', lazy='noload')
    customer = db.relationship('Customer', back_populates='ratings', lazy='noload')

    def __init__(self, customer_id, product_id, rating):
        self.customer_id = customer_id
        self.product_id = product_id
        self,rating = rating

class Payment(db.Model):
    __tablename__ = 'payment'
    #columns
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id',ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    amount_tendered = db.Column(db.Numeric(10,2), nullable=False)
    change = db.Column(db.Numeric(10,2), nullable=True)
    _intent_id = db.Column('intent_id',db.LargeBinary, unique=True, nullable = True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='SET NULL'),nullable=True)
    type = db.Column(db.String(50), nullable=False)

    #relatioships
    employee = db.relationship('Employee', back_populates='payments_collected', lazy='noload')
    order = db.relationship('Order', back_populates='payments', lazy='noload')

    def __init__(self, order_id,amount_tendered, change, intent_id, recorded_by, type):
        self.order_id = order_id
        self.amount_tendered = amount_tendered
        self.change = change
        self.intent_id = intent_id
        self.recorded_by = recorded_by
        self.type = type

    @property
    def intent_id(self):
        return encryp.decrypt(self._intent_id)
    @intent_id.setter
    def intent_id(self,intent_id):
        self._intent_id = encryp.encrypt(intent_id)



class Parish(db.Model):
    __tablename__ = 'parish'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name',db.LargeBinary, unique=True)
    shipping_rate = db.Column(db.Numeric(10,2), nullable=False)

    
    time_slots = db.relationship("ShippingTimeSlot", back_populates="parish", passive_deletes=True, lazy='noload')
    default_config_time_slot = db.relationship('DefaultConfigShippingTimeSlot', back_populates='parish', passive_deletes=True, lazy='noload')

    def __init__(self,name,shipping_rate):
        self.parish = name
        self.shipping_rate = shipping_rate
    
    @property
    def name(self):
        return encryp.decrypt(self._name)
    @name.setter
    def name(self,name):
        self._parish = encryp.encrypt(name)



class DefaultConfigShippingTimeSlot(db.Model):
    __tablename__ = 'default_config_shipping_time_slot'
    parish_id = db.Column(db.Integer, db.ForeignKey('parish.id', ondelete='CASCADE'), primary_key=True)
    day = db.Column(db.Integer, primary_key=True,nullable=False) #0-6
    time_slot_interval = db.Column(db.Interval, nullable=False)
    max_per_slot = db.Column(db.Integer, nullable = False)

    #relationships
    parish = db.relationship('Parish', back_populates='default_config_time_slot', lazy='noload')

    def __init__(self, parish_id, day, max_per_slot, time_slot_interval):
        self.parish_id = parish_id
        self.day = day
        self.max_per_slot = max_per_slot
        self.time_slot_interval = time_slot_interval


class ShippingTimeSlot(db.Model):
    # run cron job that populates time_slot every night
    __tablename__ = 'shipping_time_slot'
    id = db.Column(db.Integer, primary_key=True, index=True)
    parish_id = db.Column(db.Integer, db.ForeignKey('parish.id', ondelete='CASCADE'), nullable=False)
    # _parish = db.Column('parish',db.LargeBinary, unique=True)
    # day = db.Column(db.Integer, nullable=False) #0-6
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    num_space_available = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean,nullable=False, default=True)

    __table_args__ = (db.UniqueConstraint('parish_id', 'start_time', 'end_time', name='shipping_time_slot_parish_id_start_time_end_time_uc'),)

    #relationships
    parish = db.relationship('Parish', back_populates="time_slots", lazy='noload')
    orders = db.relationship('Order', back_populates='time_slot', passive_deletes=True, lazy='noload')

    def __init__(self,parish_id,start_time, end_time, max_per_slot, num_space_available):
        self.parish_id = parish_id
        self.start_time = start_time
        self.end_time = end_time
        self.max_per_slot = max_per_slot
        self.num_space_available = num_space_available

    

class Tax(db.Model):
    __tablename__ = 'tax'
    tax = db.Column(db.String(20), nullable=False, primary_key=True)
    rate = db.Column(db.Numeric(5,5), nullable=False)

    def __init__(self, tax, rate):
        self.tax = tax
        self.rate = rate


#####################################################
#                       Views                       #
#####################################################

class ProductAvgRatingMV(MaterializedView):
    __table__ = create_mat_view(
        'product_avg_rating',
        db.select(
            CustomerProductRating.product_id.label('product_id'),
            db.func.avg(CustomerProductRating.rating).label('avg_rating'),
            db.func.count(CustomerProductRating.customer_id).label('num_customers'), #equivalent to count(*)
            (db.func.sum(CustomerProductRating.rating) * db.func.count(CustomerProductRating.customer_id) * 1/10000).label('coefficient')
        ).group_by(CustomerProductRating.product_id)
    )
db.Index('product_avg_rating_product_id_idx', ProductAvgRatingMV.product_id, unique=True)



class TotalProductOrderedLastThreeMonthsMV(MaterializedView):
    __table__ = create_mat_view(
        'total_product_ordered_last_three_months',
        db.select(
            OrderLine.product_id.label('product_id'),
            db.func.sum(OrderLine.quantity).label('total')
        ).join(
            Order, OrderLine.order_id==Order.id #explicit condition,from OrderGroceries join Order on OrderLine.order_id==Order.id
        ).where(
            str(datetime.utcnow()) - Order.created_at < str(timedelta(days=90))
        ).group_by(OrderLine.product_id)
    )
db.Index('ix_total_product_ordered_last_three_months_product_id',TotalProductOrderedLastThreeMonthsMV.product_id, unique=True)


class PairsofProductsOrderedTogetherMV(MaterializedView):
    #SELECT g1.grocery_id AS item1, g2.grocery_id AS item2, count(*) AS count FROM order_line g1 JOIN order_line g2 ON g1.order_id = g2.order_id WHERE g1.grocery_id < g2.grocery_id GROUP BY g1.grocery_id, g2.grocery_id having count(*) > 1"""
    order_line_alias = aliased(OrderLine) #private variable to use as OrderLine alias in query
                                            #this is needed so that the join cam be performed on the same table
    __table__ = create_mat_view(
        'pairs_of_products_ordered_together',
        db.select(
            OrderLine.product_id.label('product1_id'),
            order_line_alias.product_id.label('product2_id'),
            db.func.count().label('count') - 1
        ).join(
            order_line_alias, OrderLine.order_id==order_line_alias.order_id
        # ).where(
        #     OrderLine.product_id < order_line_alias.product_id
        ).group_by(
            OrderLine.product_id, order_line_alias.product_id
        ).having(
            db.func.count() > 1 #only pairs with count > 1 have been bought with together
        )
    )
db.Index(
    'ix_pairs_of_products_ordered_together_product1_id_product2_id',
    PairsofProductsOrderedTogetherMV.product1_id,
    PairsofProductsOrderedTogetherMV.product2_id, unique=True)



class TotalofProductOrderedbyCustomerMV(MaterializedView):
    __table__ = create_mat_view(
        'total_of_product_ordered_by_customer',
        db.select(
            Customer.id.label('customer_id'),
            OrderLine.product_id.label('product_id'),
            db.func.sum(OrderLine.quantity).label('total')
        ).join(
            Order, Customer.id==Order.customer_id
        ).join(
            OrderLine, Order.id==OrderLine.order_id
        ).group_by(
            Customer.id, OrderLine.product_id
        )
    )
db.Index(
    'ix_total_of_item_ordered_by_customer_customer_id_product_id',
    TotalofProductOrderedbyCustomerMV.customer_id,
    TotalofProductOrderedbyCustomerMV.product_id, unique=True
)



#creating all materialized views

def create_views():
    temp_tables = db.metadata.tables # temporarily holding place for all db.Model tables
                                        # this is to ensure the command for creating
                                        # the these tables in the database isn't ran. Creating 
                                        # tables in the database should only be done using
                                        # the flask migrations.
                                        # i.e. when db.metadata.create_all is ran
                                        # it creates all tables in the database, therefore
                                        # I temporarily remove those tables from metadata 
                                        # in order for it to not delete them
    db.metadata.tables = {} 

    db.metadata.drop_all(db.engine) #drop all tables, however dict of tables is empty so no tables are dropped, only views
    db.metadata.create_all(db.engine)  #create all materialized views
    db.metadata.tables = temp_tables    #repopulate metadata with table info


    #SQLalchemy relationships that can't be defined on original class definition
    #because the views aren't created at alembic migration time (it creates a Object reference error). 
    #Therefore I created a hack to allow migrations to be created.
    Customer.count_of_product_prev_ordered = db.relationship('TotalofProductOrderedbyCustomerMV', backref='customer',
                        uselist=True, # makes it a one-to-many relationship, this is the default setting
                        primaryjoin='Customer.id==TotalofProductOrderedbyCustomerMV.customer_id',
                        foreign_keys='TotalofProductOrderedbyCustomerMV.customer_id', lazy='select')

    Product.avg_rating = db.relationship('ProductAvgRatingMV', backref='product',
                        uselist=False, # makes it a one-to-one relationship
                        primaryjoin='Product.id==ProductAvgRatingMV.product_id',
                        foreign_keys='ProductAvgRatingMV.product_id', lazy='joined')
    
    Product.total_product_ordered_last_three_months= db.relationship('TotalProductOrderedLastThreeMonthsMV', backref='product',
                        uselist=False, # makes it a one-to-one relationship
                        primaryjoin='Product.id==TotalProductOrderedLastThreeMonthsMV.product_id',
                        foreign_keys='TotalProductOrderedLastThreeMonthsMV.product_id') #, lazy='joined') #maybe I want to change this later

