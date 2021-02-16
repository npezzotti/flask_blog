class Config(object):
    DEBUG = False
    TESTING = False
    DB_HOST = 'db'
    DB = 'flask_blog'
    DB_USERNAME = 'nathan'
    DB_PASSWORD = 'password'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
