from app import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from app.models.user import User

class OAuth(OAuthConsumerMixin, db.Model):
    """OAuth model for storing OAuth tokens."""
    __tablename__ = 'oauth'
    
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User) 