#import sqlite3
import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    print("Calling get_db...")
    if 'db' not in g:
        #g.db = sqlite3.connect(
         #       current_app.config['DATABASE'],
          #      detect_types=sqlite3.PARSE_DECLTYPES
           #     )
        #g.db.row_factory = sqlite3.Row
        g.db = psycopg2.connect(host="db",database="flask_blog", user="nathan", password='password')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    print("Calling init_db...")
    db = get_db()
    cur = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read().decode('utf-8'))
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    print("Calling init_app...")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_post(id, check_author=True):
    db  = get_db()
    cur = db.cursor()
    query = cur.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN users u ON p.author_id = u.id'
            ' WHERE p.id = %s;',
            (id,)
            )
    post = cur.fetchone()

    if post is None:
        abort(404, "Post id {} does not exist").format(id)
    if check_author and post[4] != g.user[0]:
        abort(403, "You are not authorized to do this.")

    return post
