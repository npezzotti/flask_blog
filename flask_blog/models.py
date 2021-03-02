from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column(db.String(120), unique=True, nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return f"User({self.username})"
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(30), unique=True, nullable=False, server_default='Untitled')
    author = db.relationship(User, lazy=True, backref='post')
    created = db.Column(db.DateTime, nullable=False, server_default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.created})"