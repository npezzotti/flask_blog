class Config:
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = '86e6c98251544abb91729a875fb2badf'
    DB_HOST = 'db'
    DB = 'flask_blog'
    DB_USERNAME = 'nathan'
    DB_PASSWORD = 'password'
    SQLALCHEMY_DATABASE_URI = 'postgresql://nathan:password@db/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    """Configurations for development"""
    ENV = 'development'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True