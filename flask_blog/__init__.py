print("Calling init")
import os
from flask import Flask
from config import Config

version_info = (1, 0, 0)
__version__ = ".".join([str(v) for v in version_info])

def create_app(test_config=None):
    print("Calling create_app in __init__.py...")
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(config)
    print('config: ', app.config)
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
