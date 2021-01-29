import sqlite3
import pytest
from flask_blog.db import get_db

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    print(db)

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
        assert 'Cannot operate on a closed database' in str(e.value)
    print(str(e.value))

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flask_blog.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    print(result.output) 
    assert 'Initialized the database.' in result.output
    assert Recorder.called
