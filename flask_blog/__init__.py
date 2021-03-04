print("Calling flask_blog init...")
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

version_info = (1, 0, 0)
__version__ = ".".join([str(v) for v in version_info])

db = SQLAlchemy()

def create_app(testing=False):
    print("Calling create_app in __init__.py...")
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='default',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if testing:
        app.config.from_object(config.TestingConfig)
    else: 
        app.config.from_object(config.Config)

    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
        db_path = os.path.join(app.instance_path, 'flask_blog.sqlite')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    print(app.config)

    db.init_app(app)

    from . import db_utils
    db_utils.init_app(app)

    from flask_blog.cli import init_db_command
    app.cli.add_command(init_db_command)

    from flask_blog.auth.views import bp as auth_bp
    app.register_blueprint(auth_bp)

    from flask_blog.blog.views import bp as blog_bp
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint='index')

    return app