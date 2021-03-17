from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from FlaskApp import db, login_manager, create_app
from flask_login import UserMixin
import datetime

#USERS
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), default='')
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), default='')
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean(), default=False)

    def get_reset_token(self, expires_sec=1800):
    	s = Serializer('SECRET_KEY', expires_sec)
    	return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
    	s = Serializer('SECRET_KEY')
    	try:
    		user_id = s.loads(token)['user_id']
    	except:
    		return None
    	return User.query.get(user_id)