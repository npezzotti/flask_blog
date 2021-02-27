import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    print("Calling get_db...")
    if 'db' not in g:
        print(current_app.config)
        try: 
            g.db = psycopg2.connect(
                host=current_app.config['DB_HOST'], 
                database=current_app.config['DB'], 
                user=current_app.config['DB_USERNAME'], 
                password=current_app.config['DB_PASSWORD']
                )
            print("Connected to database!")
        except psycopg2.Error as e:
            print("Unable to connect to database: ", e)

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
