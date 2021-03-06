from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST", "GET"])
def login():
    """ this function creates the route for the user 
    to login to an account on Communitiez. It checks 
    to see if the details entered match in the database
    and uses the werkzeug.security library to check 
    compare the hashed pw. 
    """

    if request.method == "POST":
        login_username = request.form["usernameInput"]
        login_password = request.form["passwordInput"]
        username_exists = User.query.filter_by(username=login_username).first()

        if username_exists is not None: 
            if check_password_hash(username_exists.password, login_password):
                flash("Logged in Successfully!", category="success")
                login_user(username_exists, remember=True)
                return redirect(url_for("view.home"))
            else: 
                flash("Incorrect Password, please try again!", category="error")
        else: 
            flash("Email does not exist", category="error")
        
        return redirect(url_for("auth.login"))

    else: 
        if current_user.is_authenticated:
            flash("You are already logged in!", category="error")
            return redirect(url_for("view.home"))
        else: 
            return render_template("login.html")


@auth.route('/signup', methods=["POST", "GET"])
def signup():
    """ this function creates the route for the user 
    to register an account Communitiez. The function 
    checks if data entered meets the minimum requirements
    and queries the database to see if no other users exist 
    with the same details. If all criteria is met 
    the users details are added to the DB.
    """
  
    if request.method == "POST":
        signup_email = request.form["emailInput"]
        signup_username = request.form["usernameInput"]
        signup_password1 = request.form["passwordInput1"]
        signup_password2 = request.form["passwordInput2"]

        if len(signup_email) < 4:
            flash("Email length must be greater than 4 characters", category="error") 
        elif len(signup_username) < 4:
            flash("Username length must be greater than 4 characters", category="error")
        elif len(signup_password1) < 7:
            flash("Password length must be greater than 7 characters", category="error")
        elif signup_password1 != signup_password2:
            flash("Passwords do not match", category="error")
        else:
            email_exists = User.query.filter_by(email=signup_email).first()
            username_exists = User.query.filter_by(username=signup_username).first()

            if email_exists is not None or username_exists is not None:
                flash("The email or username already exists, please try again with different ones", category="error")
            else:
                new_user = User(email=signup_email, username=signup_username, password=generate_password_hash(signup_password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                flash(f"Account Created Successfully - welcome to Communitiez {signup_username}. Please log in.",category="success")
                return redirect(url_for("auth.login"))

        return redirect(url_for("auth.signup"))

    else: 
        if current_user.is_authenticated:
            flash("You are already logged in. Log out to create another account.", category="error")
            return redirect(url_for("view.home"))
        else: 
            return render_template("signup.html") 


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!", category="success")
    return(redirect(url_for("auth.login")))
