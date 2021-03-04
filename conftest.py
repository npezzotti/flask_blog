import os
import datetime
import pytest
from flask_blog import create_app, db
from flask_blog.auth.models import User
from flask_blog.blog.models import Post

@pytest.fixture
def app():
    print("\nCalling app fixture...\n")
    app = create_app(testing=True)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all(
            (            
                User(username='test', password='password'),
                User(username='other', password='password'), 
                Post(title='test title', body='test\nbody', author_id=1, created=datetime.date(2021, 2, 28))
            )
        )
        db.session.commit()
    
    yield app

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
    
    def login(self, username='test', password='password'):
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