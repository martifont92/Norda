from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from FlaskApp import db

auth = Blueprint('auth', __name__)

#SIGNUP
@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	username = request.form.get('username')
	password = request.form.get('password')

	user = User.query.filter_by(username=username).first()

	if user:
		flash('Username already exists.')
		return redirect(url_for('auth.signup'))

	new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

	db.session.add(new_user)
	db.session.commit()

	return redirect(url_for('auth.login'))

#LOGIN
@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	username = request.form.get('username')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(username=username).first()

	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login'))

	login_user(user)

	return redirect(url_for('main.account', id=current_user.id))

#LOGOUT
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))