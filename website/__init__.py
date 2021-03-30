import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


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
    session_key = secrets.token_urlsafe(16)
    app.config["SECRET_KEY"] = f"{session_key}" 
    app.secret_key = session_key 
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from.views import view
    from.auth import auth

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    from .models import User, Community, Usercommunity, Post, Comment
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    """ This function checks to see if a path to 
    the database already exists using the os module. 
    If a path does not exist, the database is created. 
    """

    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database")
