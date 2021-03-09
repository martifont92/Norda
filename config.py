class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "7uXedmEt2tMMWvS"

    #Configure mail server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'martifont92@gmail.com'
    MAIL_PASSWORD = 'wkxttnikikkdixrg'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True