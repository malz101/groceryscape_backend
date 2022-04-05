from app import create_app_db_migration # we import the app object from the app module
from app.util.extensions import db

if __name__ == '__main__':
    app = create_app_db_migration()
    app.run(debug=True, host="0.0.0.0")


