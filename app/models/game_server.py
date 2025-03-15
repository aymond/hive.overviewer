from app import db
from datetime import datetime

class GameServer(db.Model):
    """Model for storing game server information."""
    __tablename__ = 'game_servers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    game_type = db.Column(db.String(64), nullable=False)  # minecraft, valheim, etc.
    server_port = db.Column(db.Integer, nullable=False)
    query_port = db.Column(db.Integer, nullable=True)
    max_players = db.Column(db.Integer, default=10)
    status = db.Column(db.String(20), default='stopped')  # running, stopped, restarting
    auto_start = db.Column(db.Boolean, default=False)
    install_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=False)
    
    # One game server can have many configurations
    configs = db.relationship('GameConfig', backref='game_server', lazy='dynamic',
                             cascade="all, delete-orphan")
    
    def __init__(self, name, game_type, server_port, host_id, query_port=None, 
                 max_players=10, auto_start=False, install_path=None):
        self.name = name
        self.game_type = game_type
        self.server_port = server_port
        self.query_port = query_port
        self.max_players = max_players
        self.auto_start = auto_start
        self.install_path = install_path
        self.host_id = host_id
    
    def update_status(self, status):
        """Update server status."""
        valid_statuses = ['running', 'stopped', 'restarting', 'installing', 'error']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}")
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Return server as dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'game_type': self.game_type,
            'server_port': self.server_port,
            'query_port': self.query_port,
            'max_players': self.max_players,
            'status': self.status,
            'auto_start': self.auto_start,
            'install_path': self.install_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'host_id': self.host_id,
            'configs_count': self.configs.count()
        }
    
    def __repr__(self):
        return f'<GameServer {self.name} ({self.game_type})>' 