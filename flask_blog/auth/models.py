from werkzeug.security import generate_password_hash, check_password_hash
from flask_blog import db

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
        return '<User %r>' % self.username