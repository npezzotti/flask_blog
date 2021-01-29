from flask import g
from flask_blog.db import get_db
from werkzeug.exceptions import abort

def get_post(id, check_author=True):
    post = get_db().execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id,)
            ).fetchone()

    if post is None:
        abort(404, "Post id {} does not exist").format(id)

    if check_author and post['author_id'] != g.user['id']:
      abort(403)

    return post
