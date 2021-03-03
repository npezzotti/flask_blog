from flask_blog import db
from flask_blog.auth.models import User

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(30), unique=True, nullable=False, server_default='Untitled')
    author = db.relationship(User, lazy=True, backref='post')
    created = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title