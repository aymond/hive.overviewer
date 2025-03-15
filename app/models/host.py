from app import db
from datetime import datetime

class Host(db.Model):
    """Model for storing host information (physical or virtual servers)."""
    __tablename__ = 'hosts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    port = db.Column(db.Integer, default=22)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='offline')  # online, offline, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('hosts', lazy='dynamic'))
    
    # One host can have many game servers
    game_servers = db.relationship('GameServer', backref='host', lazy='dynamic',
                                  cascade="all, delete-orphan")
    
    def __init__(self, name, address, port=22, description=None, user_id=None):
        self.name = name
        self.address = address
        self.port = port
        self.description = description
        self.user_id = user_id
    
    def update_status(self, status):
        """Update host status."""
        valid_statuses = ['online', 'offline', 'maintenance']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}")
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Return host as dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'port': self.port,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'game_servers_count': self.game_servers.count()
        }
    
    def __repr__(self):
        return f'<Host {self.name} ({self.address})>' 