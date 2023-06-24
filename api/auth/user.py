from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint
from flask_login import logout_user, login_required
from passlib.hash import pbkdf2_sha256
from utils import db
from flask import request, render_template
from datetime import timedelta
from api.models.user import User


auth = Blueprint("Users", "users", description="Operations on Users")

@auth.route('/index')
@auth.route('/')
def index():
    return render_template('index.html')
 

@auth.route('/register', methods=['GET', 'POST'])
# @login_required
def register_page():
    if request.method == 'POST': 
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
                return render_template('register.html', error="Email already exists.")
        if password != confirm_password:
                return render_template('register.html', error="Check that your password and confirm password match.")
        if len (password) < 6:
            return render_template('register.html', error="Check that your password is up to 6 characters.")
        
        new_user = User(
            email=email,
            username=username,
            password = pbkdf2_sha256.hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


                
# Login a user
@auth.route("/login", methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        existing_email = User.query.filter_by(email=email).first()

        if not existing_email:
            return render_template('login.html', error="User does not exist.")

        if pbkdf2_sha256.verify(password, existing_email.password):
            return render_template('login.html', error='Check Your Email and password and try again')

    return render_template('shorten.html')
    


@auth.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False, expires_delta=timedelta(days=5)
        )

        return {"access_token": new_token}

# Logout a user


@auth.route("/logout")
def logout():
	logout_user()
	# flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return render_template('index.html', error='Succesfully logged out.')



# # Delete a user 
# @auth.route('/users')
# def delete(username):
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         return render_template('login.html', error='You need to be logged in')

#     db.session.delete(user)
#     db.session.commit()

#     return render_template('register.html')