from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(30), unique=True, nullable=False, server_default='Untitled')
    author = db.relationship(User, lazy='joined', backref='posts')
    created = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title