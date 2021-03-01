from flask import Blueprint, render_template, redirect, url_for, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')

@auth.route('/signup', methods=["POST", "GET"])
def signup():
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
            print("#Write Code functionality to add details to the database here")

        return redirect(url_for("auth.signup"))
    else: 
        return render_template("signup.html")