import os
from flask import Flask, Blueprint, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
admin = Admin()

def create_app():
	app = Flask(__name__)

	#Config
	if app.config["ENV"] == "production":
		app.config.from_object("config.ProductionConfig")
	else:
	    app.config.from_object("config.DevelopmentConfig")

	from .models import User

	db.init_app(app)
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	mail.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	#Admin
	class MyModelView(ModelView):
		def is_accessible(self):
			if current_user.is_authenticated:
				return current_user.is_admin
			else:
				return False

	class MyAdminIndexView(AdminIndexView):
		def is_accessible(self):
			if current_user.is_authenticated:
				return current_user.is_admin
			else:
				return False

	admin.init_app(app, index_view=MyAdminIndexView())
	admin.add_view(MyModelView(User, db.session))

	#Import Blueprints
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app