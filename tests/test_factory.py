from flask_blog import create_app

def test_config():
    assert not create_app().testing
    assert create_app(testing=True).testing
