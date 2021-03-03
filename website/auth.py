from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST", "GET"])
def login():
    """ this function creates the route for the user 
    to login to an account on Communitiez. 
    """

    if request.method == "POST":
        login_username = request.form["usernameInput"]
        login_password = request.form["passwordInput"]
        user_account = User.query.filter_by(username=login_username).first()

        if user_account is not None: 
            if check_password_hash(user_account.password, login_password):
            # Finish this code - watch tech with tim tutorial
    else: 
        if "user" in session:
            flash("You are already logged in", category="error")
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
    the users details are added to the DB and a session
    is created storing the users username. 
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
                return redirect(url_for("auth.signup"))
            else:
                new_user = User(email=signup_email, username=signup_username, password=generate_password_hash(signup_password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                session["user"] = signup_username
                flash(f"Account Created Successfully - welcome to Communitiez {signup_username}", category="success")
                return redirect(url_for("view.home"))
    else: 
        if "user" in session:
            flash(f"You are already signed up and logged in. Please log out to create another account, {session['user']}", category="error")
            return redirect(url_for("view.home"))
        else:
            return render_template("signup.html") 
