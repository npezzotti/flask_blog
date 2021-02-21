import os
import tempfile

import pytest
from flask_blog import create_app
from flask_blog.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'tests/data.sql'), 'rb') as f:
        _data_sql = f.read().decode('utf8')
        print("Created data.sql...\n")

@pytest.fixture
def app():
    print("\nCalling app fixture...\n")
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    print("\nCalling the client fixture...\n")
    return app.test_client()

@pytest.fixture
def runner(app):
    print("\n Calling the runner fixture...\n")
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        print("In the AuthActions class...")
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
                '/auth/login',
                data={'username': username, 'password': password}
                )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    print("\nCalling the auth fixture...\n")
    return AuthActions(client)
