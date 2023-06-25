import os
from flask import Flask, jsonify, redirect, url_for, flash
from flask_smorest import Api
from flask_jwt_extended import JWTManager, get_jwt_identity
from api.models.user import User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from utils import db
from flask import url_for, redirect, flash
from flask_migrate import Migrate
from Blocklist import BLOCKLIST
from api.config.config import config_dict
from api.main.main import blp as main_blueprint
from api.auth.user import auth as user_blueprint



def create_app(db_url=None, config=config_dict['dev']):
    app = Flask(__name__)
    app.secret_key = 'veryr53462626wdomstuff'
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Scissors API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///scissors.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "very_very_discreet"
    db.init_app(app)


   
    api = Api(app)
    login_manager = LoginManager(app)


    migrate = Migrate(app, db)

    @login_manager.user_loader
    def user_loader(id):
      return User.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        flash('Login to access this page', category='info')
        return redirect(url_for('Users.index'))

    
    app.config["JWT_SECRET_KEY"] = "veryrandomstuff"
    jwt = JWTManager(app)

   # If the user isn't logged in and tries to access a login required route, this decorator allows the page to
    # redirect page to the homepage
    # @login_manager.unauthorized_handler
    # def unauthorized_handler():
    #     flash('Login to access this page', category='info')
    #     return redirect(url_for('Mains.get_user_history'))

    
    # app.config["JWT_SECRET_KEY"] = "veryr53462626wdomstuff"
    # jwt = JWTManager(app)

    
    
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({
    #             "description": "This token has expired",
    #             "error": "token_expired"
    #         }), 401
    #     )

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (
    #         jsonify({
    #             "description": "Signature verification failed",
    #             "error": "invalid_token"
    #         }), 401
    #     )
    
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return (
    #         jsonify({
    #             "desciption": "Request does not contain an access token",
    #             "error": "authorization_required"
    #         }), 401
    #     )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(main_blueprint)
    api.register_blueprint(user_blueprint)
    
    
    return app