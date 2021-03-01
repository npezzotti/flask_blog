from flask import  g

def get_db():
    print("Calling get_db...")
    if 'db' not in g:
        print(current_app.config)
        try: 
            # Code to get db object and set g.db to its value
            pass
            print("Connected to database!")
        except psycopg2.Error as e:
            print("Unable to connect to database: ", e)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    print("Calling init_app...")
    app.teardown_appcontext(close_db)