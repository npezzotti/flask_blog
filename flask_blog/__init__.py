print("Calling init")
import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from config import Config

version_info = (1, 0, 0)
__version__ = ".".join([str(v) for v in version_info])

db = SQLAlchemy()

def create_app(test_config=None):
    print("Calling create_app in __init__.py...")
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)
    print('config: ', app.config)
    db.init_app(app)
    print(dir(db))

    from . import db_utils
    db_utils.init_app(app)

    from flask_blog.cli import init_db_command
    app.cli.add_command(init_db_command)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app