from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
        )
from werkzeug.security import check_password_hash, generate_password_hash
from flask_blog import db
from flask_blog.auth.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        print(request.form)
        print(request.form['username'], request.form['password'])
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        print(user)

        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif user is not None:
            error = f"User {username} is already registered."        
        
        if error is None:
            db.session.add(User(username=username, password=password))
            db.session.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print('form: ', request.form)
        username = request.form['username']
        password = request.form['password']
        print('request data: ', username, password)
        user = User.query.filter_by(username=username).first()
        print('dir of user...: ', dir(user))
        error = None
        if user is None:
            error = "Incorrect username."
        elif not user.check_password(password):
            error = "Incorrect password."
        
        print('login error: ', error)

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.query.filter_by(id=user_id).first()
        g.user = user
        print(g.user)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))