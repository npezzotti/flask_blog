class Config:
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = '86e6c98251544abb91729a875fb2badf'
    DB_HOST = 'db'
    DB = 'flask_blog'
    DB_USERNAME = 'nathan'
    DB_PASSWORD = 'password'

class DevelopmentConfig(Config):
    """Configurations for development"""
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
