from utils import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    posts = db.relationship('ShortUrl', backref='poster', lazy=True)
    
    
    def __repr__(self):
        return f"<Student {self.username}"