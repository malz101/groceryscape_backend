from pprint import pprint
from flask import Flask
from .util.extensions import db, mail, csrf, cors, sess, encryp, migrate

def create_app():
    """Initialize the core application"""
    app = Flask(__name__)
    from .config import DevelopmentConfig
    #load application configuration from its object
    app.config.from_object(DevelopmentConfig)
    
    register_extensions(app)
    register_blueprints(app)
    register_global_decorators(app)
    #include routes for the application
    # from .routes import customer_routes, employee_routes

    #below is for test queries until I setup a testing environment
    # with app.app_context():
    #     from app.service import customer_access
    #     pprint(str(customer_access.get_customer(email='email')))
    return app

# def create_app():
#     app = Flask(__name__)
#      from .config import DevelopmentConfig
#     #load application configuration from its object
#     app.config.from_object(DevelopmentConfig)
#     # pprint(app.config)
#     # input()
#     #object that does encryption
#     encryp.init_app(app)
#     # pprint(encryp.key)
#     # input()
#     db.init_app(app)
#     with app.app_context():
#         from .database.models import Customer, Employee, Product, Category,\
#             ProductCategory, Order, OrderItem, CartItem, CustomerProductRating, Payment,\
#                 Parish, ShippingTimeSlot, Tax, ProductAvgRatingMV,\
#                     PairsofProductsOrderedTogetherMV,TotalProductOrderedLastThreeMonthsMV,\
#                         TotalofProductOrderedbyCustomerMV, create_views
        
#         temp_tables = db.metadata.tables # temporarily holding place for all db.Model tables
#                                         # this is to ensure the command for creating
#                                         # the these tables in the database isn't ran. Creating 
#                                         # tables in the database should only be done using
#                                         # the flask migrations.
#                                         # i.e. db.metadata.create_all is ran
#                                         # it creates all tables in the database, therefore
#                                         # I temporarily remove those tables from metadata 
#                                         # in order for it to not delete them
#         db.metadata.tables = {} 

#         db.metadata.drop_all(db.engine) #drop all tables, however dict of tables is empty so no tables are dropped, only materialized views
#         db.metadata.tables = temp_tables    #repopulate metadata with table info
#         migrate.init_app(app,db)
        
#         # par = db.session.query(ProductAvgRatingMV).all()
#         # tiobc = db.session.query(TotalofItemOrderedbyCustomerMV)
#         # print(par)
#         # print(tiobc)
#     return app

def register_extensions(app):
    """initialize installed extension instances"""
    db.init_app(app)
    mail.init_app(app)
    app.extensions['mail'].debug = 0 #disable flask mail debugger
    # cors.init_app(app, resources={r"/*": {"origins": ["https://groceryscape.web.app","https://groceryscape-admin.web.app"]}})
    csrf.init_app(app)
    sess.init_app(app)
    encryp.init_app(app)
    

    

def register_blueprints(app):
    """initialize api blueprints"""
    from .customer import create_blueprint as create_customer_blueprint
    # from .employee import employee_bp

    #register api blueprints
    app.register_blueprint(create_customer_blueprint(), url_prefix='/api/v1')
    # app.register_blueprint(employee_bp, url_prefix='/employee/api/v1')

    #initialize customer and employee endpoints
    # initialize_customer_routes()


def register_global_decorators(app):
    '''initialize decorators that should be established app wide (i.e to all
    blueprints'''
    from .util.decorators import regenerate_session
    regenerate_session(app)