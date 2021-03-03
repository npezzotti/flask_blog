import pytest
from flask import g, session
from flask_blog import db
from flask_blog.auth.models import User

def test_register(client, app):
    print("Calling test_register...")
    assert client.get('/auth/register').status_code == 200
    response = client.post(
            '/auth/register', data={'username': 'a', 'password': 'a'}
            )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert User.query.filter_by(username='a').first() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('','', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'User test is already registered')
    ))
def test_register_validate_input(client, username, password, message):
    print("Calling test_register_validate_input with args: ", username, password, message)
    response = client.post(
            '/auth/register',
            data={'username': username, 'password': password}
            )
    assert message in response.data

def test_login(client, auth):
    print("Calling test_login...")
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    print(response.location)
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.')
    ))
def test_login_validate_input(auth, username, password, message):
    print("Calling test_login_validate_input with args: ", username, password, message)
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    print("Calling test_logout...")
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
