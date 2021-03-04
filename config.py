class Config:
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = '86e6c98251544abb91729a875fb2badf'
    SQLALCHEMY_DATABASE_URI = 'postgresql://nathan:password@db/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"