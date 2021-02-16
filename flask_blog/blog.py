from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
        )
from werkzeug.exceptions import abort
from flask_blog.auth import login_required
from flask_blog.db import get_db, get_post

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    query = cur.execute(
            'SELECT post.id, post.title, post.body, post.created, post.author_id, users.username'
            ' FROM post JOIN users ON post.author_id = users.id'
            ' ORDER BY created DESC;'
            )
    posts = cur.fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                    'INSERT INTO post (title, body, author_id)'
                    ' VALUES (%s, %s, %s)',
                    (title, body, g.user[0])
                    )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST',))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()
            cur.execute(
                    'UPDATE post SET title = %s, body = %s'
                    ' WHERE id = %s',
                    (title, body, id)
                    )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_id(id):
    get_post(id)
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM post WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
