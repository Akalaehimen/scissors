from datetime import datetime
from utils import db
from api.models.user import User


class ShortUrl(db.Model):
    __tablename__ = "url"

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(1000), nullable=False)
    short_url = db.Column(db.String(7), unique=False, nullable=False)
    domain_name = db.Column(db.String(255), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    clicks = db.Column(db.Integer, default=0)

    licks = db.relationship('Click', backref='short_url', lazy=True)


    def __repr__(self):
        return f"Url('{self.long_url}', '{self.short_url}')"

    