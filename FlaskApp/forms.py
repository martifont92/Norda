from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

#SIGNUP
class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})
	password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
	submit = SubmitField('SUBMIT')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists.')

#LOGIN
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})
	password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
	remember = BooleanField('Remember Me')
	submit = SubmitField('LOGIN')

#USERNAME RECOVERY
class RequestUsernameForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
	submit = SubmitField('REMAIL MY USERNAME')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('Sorry, the provided email was not found. Please try again or contact support.')

#PASSWORD RESET
class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
	submit = SubmitField('REQUEST PASSWORD RESET')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('Sorry, the provided email was not found. Please try again or contact support.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "new password"})
    submit = SubmitField('RESET MY PASSWORD')
