import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():
	app = Flask(__name__)

	if app.config["ENV"] == "production":
		app.config.from_object("config.ProductionConfig")
	else:
	    app.config.from_object("config.DevelopmentConfig")

	db.init_app(app)

	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	mail.init_app(app)

	from .models import User

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app