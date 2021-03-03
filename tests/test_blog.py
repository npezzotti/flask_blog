import pytest
from flask_blog import db
from flask_blog.blog.models import Post

def test_index(client, auth):
    print("Running test_index...")
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2021-02-28' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete'
    ))
def test_login_required(client, path):
    print("Calling test_login_required with arg: ", path)
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

def test_author_required(app, client, auth):
    # change the author to another user
    print("Calling test_author_required...")
    with app.app_context():
        post = Post.query.filter_by(id=1).first()
        post.author_id = 2
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete'
    ))
def test_exists_required(client, auth, path):
    print("Calling test_exists_required with arg: ", path)
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    print("Calling test_create...")
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        post = Post.query.filter_by(id=1).first()
        assert post.title == 'updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update'
    ))
def test_create_update_validate(client, auth, path):
    print("Calling test_create_update_validate...")
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required' in response.data

def test_delete(client, auth, app):
    print("Calling test_delete...")
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        post = Post.query.filter_by(id=1).first()
        assert post is None
