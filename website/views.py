from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_required, current_user
from .models import User

view = Blueprint('view', __name__)

@view.route('/')
def landing():
    return render_template('index.html')

@view.route('/home')
@login_required
def home():
    return render_template('home.html')

@view.route('/search_communitiez')
@login_required
def search_communitiez():
    return render_template("search_communitiez.html")

@view.route('create_community')
@login_required
def create_community():
    return render_template("create_community.html")