import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from FlaskApp import db, mail
from flask_mail import Message
from .models import User
from .forms import ResetPasswordForm

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
		flash('Please check your login details and try again.', 'is-danger')
		return redirect(url_for('auth.login'))

	login_user(user)

	return redirect(url_for('main.account', id=current_user.id))

#LOGOUT
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

#PASSWORD RESET
@auth.route('/reset_password')
def reset_password():
	return render_template('reset_password.html')

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message()
	msg.subject = ('Password Reset')
	msg.sender = ('martifont92@gmail.com')
	msg.recipients = [user.email]
	msg.body = f'''
Hello { user.name },

You may change your password with the link below.

{url_for('auth.reset_token', token=token, _external=True)}

Your password won't change until you access the link above and create a new one.

Thanks!
norda.com
'''
	mail.send(msg)

@auth.route('/reset_password', methods=['POST'])
def reset_password_post():
	email = request.form.get('email')

	user = User.query.filter_by(email=email).first()
	if not user:
		flash('Sorry, the provided email was not found. Please try again or contact support.', 'is-danger')
		return redirect(url_for('auth.reset_password'))

	send_reset_email(user)
	return redirect(url_for('auth.password_reset_sent'))

@auth.route('/reset_token/<token>', methods=['GET', 'POST'])
def reset_token(token):

	user = User.verify_reset_token(token)
	if not user:
		flash('This is an invalid or expired token.', 'is-warning')
		return redirect(url_for('auth.reset_password'))
	form = ResetPasswordForm()

	if form.validate_on_submit():
		user.password = generate_password_hash(form.password.data, method='sha256')
		db.session.commit()
		flash('Your password has been updated. You are now able to log in.', 'is-info')
		return redirect(url_for('auth.login'))
	return render_template('reset_token.html', form=form)

@auth.route('/password_reset/sent')
def password_reset_sent():
	return render_template('password_reset_sent.html')

#Username recovery
@auth.route('/recover_username')
def recover_username():
	return render_template('recover_username.html')

def send_recovery_email(user):
	msg = Message()
	msg.subject = ('Username Recovery')
	msg.sender = ('martifont92@gmail.com')
	msg.recipients = [user.email]
	msg.body = f'''
Hello { user.name },

As requested, here is your norda.com username:

{ user.username }

If you didn't request your username, don't worry.  You are the only one receiving this information.

Thanks!
norda.com
'''
	mail.send(msg)

@auth.route('/recover_username', methods=['POST'])
def recover_username_post():
	email = request.form.get('email')

	user = User.query.filter_by(email=email).first()
	if not user:
		flash('Sorry, the provided email was not found. Please try again or contact support.', 'is-danger')
		return redirect(url_for('auth.recover_username'))
	send_recovery_email(user)
	return redirect(url_for('auth.recover_username_sent'))

@auth.route('/recover_username/sent')
def recover_username_sent():
	return render_template('recover_username_sent.html')

