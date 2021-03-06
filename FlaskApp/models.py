from flask_login import UserMixin
from FlaskApp import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), default='')
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), default='')
    password = db.Column(db.String(100))