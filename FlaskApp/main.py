from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from .models import User
from .forms import ContactForm
from FlaskApp import db, mail
import datetime
from flask_mail import Message

main = Blueprint('main',__name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/pricing')
def pricing():
	return render_template('pricing.html')

@main.route('/account/<int:id>')
@login_required
def account(id):
	user_id = current_user.id
	name = current_user.name
	username = current_user.username
	email = current_user.email

	return render_template('account.html', name=name, username=username, email=email)

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account_details():
	name = request.form.get('name')
	username = request.form.get('username')
	email = request.form.get('email')
	password = request.form.get('password')

	if username != current_user.username:
		user = User.query.filter_by(username=username).first()
		if user:
			flash('Username already exists.', 'is-danger')
			return redirect(url_for('main.account'))

	if email != current_user.email:
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists.', 'is-danger')
			return redirect(url_for('main.account', id = current_user.id))

	current_user.name=name
	current_user.username=username
	current_user.email=email
	current_user.password=generate_password_hash(password, method='sha256')

	db.session.commit()
	flash('Your details have been saved.', 'is-primary')

	return redirect(url_for('main.account', id = current_user.id))

#CONTACT
def send_message(message):
	msg = Message(message.get('name'),
		sender = message.get('email'),
		recipients = ['martifont92@gmail.com'],
	)
	msg.body = f'''
Email: { message.get('email') }
Name: { message.get('name') }
Message: { message.get('message') }
'''

	mail.send(msg)

@main.route("/contact", methods=['GET', 'POST'])
def contact():
	form = ContactForm()

	if form.validate_on_submit():
		send_message(request.form)
		flash("Your message has been sent! We will contact you as soon as possible!", 'is-primary')
		return redirect(url_for('main.contact'))

	return render_template('contact.html', form=form)

