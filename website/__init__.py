from flask import Flask
from.views import view
from.auth import auth

def create_app():
    """ This function creates the flask app when 
    this module is loaded. It also configures the 
    'secret key' which is used to sign session cookies 
    and registers the blueprints used for the routes.  
    """

    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'gfyrifhnrgxyrfngyufggrege'
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
