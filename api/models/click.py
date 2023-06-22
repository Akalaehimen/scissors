from datetime import datetime
from utils import db
from api.models.shorturl import ShortUrl


class Click(db.Model):
    __tablename__ = "clicks"

    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey("url.id"), nullable=False)
    user_agent = db.Column(db.String(255), nullable=True)
    referrer = db.Column(db.String(255), nullable=True)
    clicked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Click {self.short_url_id} {self.clicked_at}>"