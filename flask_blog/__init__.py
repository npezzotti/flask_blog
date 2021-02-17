print("Calling init")
import os
from flask import Flask

def create_app(test_config=None):
    print("Calling create_app in __init__.py...")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY = 'dev',
            )

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py')
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
