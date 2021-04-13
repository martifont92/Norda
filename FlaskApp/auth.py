import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from FlaskApp import db, mail
from flask_mail import Message
from .models import User
from .forms import SignupForm, LoginForm, RequestUsernameForm, RequestResetForm, ResetPasswordForm

auth = Blueprint('auth', __name__)

#SIGNUP
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		new_user = User(username=form.username.data, password = generate_password_hash(form.password.data, method='sha256'))
		db.session.add(new_user)
		db.session.commit()
		flash('Account successfully created. You can log in now.', 'is-success')
		return redirect(url_for('auth.login'))

	return render_template('signup.html', form=form)

#LOGIN
@auth.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if not user or not check_password_hash(user.password, form.password.data):
			flash('Please check your login details and try again.', 'is-danger')
			return redirect(url_for('auth.login'))

		login_user(user, remember=form.remember.data)
		return redirect(url_for('main.account', id=current_user.id))

	return render_template('login.html', form=form)

#LOGOUT
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

#DELETE
@auth.route('/delete_accunt')
@login_required
def delete_account():
	user_to_delete = User.query.filter_by(id=current_user.id).delete()
	logout_user()
	db.session.commit()
	flash("We are sorry to see you go! Your account and all its data have been deleted.", 'is-primary')
	return redirect(url_for('main.index'))

#PASSWORD RESET
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
finyzz.com
'''
	mail.send(msg)

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		return redirect(url_for('auth.password_reset_sent'))
	return render_template('reset_password.html', form=form)

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
def send_recovery_email(user):
	msg = Message()
	msg.subject = ('Username Recovery')
	msg.sender = ('martifont92@gmail.com')
	msg.recipients = [user.email]
	msg.body = f'''
Hello { user.name },

As requested, here is your finyzz.com username:

{ user.username }

If you didn't request your username, don't worry.  You are the only one receiving this information.

Thanks!
finyzz.com
'''
	mail.send(msg)

@auth.route('/recover_username', methods=['GET', 'POST'])
def recover_username():
	form = RequestUsernameForm()

	user = User.query.filter_by(email=form.email.data).first()
	if form.validate_on_submit():
		send_recovery_email(user)
		return redirect(url_for('auth.recover_username_sent'))
	return render_template('recover_username.html', form=form)

@auth.route('/recover_username/sent')
def recover_username_sent():
	return render_template('recover_username_sent.html')
