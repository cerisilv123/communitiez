from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from.views import view
from.auth import auth

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """ This function creates the flask app when 
    this module is loaded. It also configures the 
    'secret key' which is used to sign session cookies, 
    registers the blueprints used for the routes and 
    initialises the database.  
    """

    app=Flask(__name__)
    app.config["SECRET_KEY"] = "gfyrifhnrgxyrfngyufggrege" # Make this more secure!
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    from .models import User
    create_database(app)

    return app

def create_database(app):
    """ This function checks to see if a path to 
    the database already exists using the os module. 
    If a path does not exist, the database is created. 
    """

    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database")
