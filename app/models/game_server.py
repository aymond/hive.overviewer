from app import db
from datetime import datetime
from app.utils.game_server import check_game_server
from typing import Tuple, Optional

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
    status_message = db.Column(db.String(120), nullable=True)  # Detailed status message
    status_data = db.Column(db.JSON, nullable=True)  # Additional status data (player count, etc.)
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
    
    def check_status(self) -> Tuple[bool, str, Optional[dict]]:
        """
        Check the actual status of the game server.
        Updates the server's status, status_message, and status_data.
        
        Returns:
            Tuple[bool, str, Optional[dict]]: (is_running, message, status_data)
        """
        # Don't check status if server is in installing or restarting state
        if self.status in ['installing', 'restarting']:
            return False, "Server is in maintenance state", None
            
        # Get the host's address
        host = self.host
        if not host:
            self.status = 'error'
            self.status_message = "Host not found"
            return False, "Host not found", None
            
        # Check server status
        is_running, message, status_data = check_game_server(
            host.address,
            self.game_type,
            self.server_port
        )
        
        # Update server status
        self.status = 'running' if is_running else 'stopped'
        self.status_message = message
        self.status_data = status_data
        self.updated_at = datetime.utcnow()
        
        return is_running, message, status_data
    
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
            'status_message': self.status_message,
            'status_data': self.status_data,
            'auto_start': self.auto_start,
            'install_path': self.install_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'host_id': self.host_id,
            'configs_count': self.configs.count()
        }
    
    def __repr__(self):
        return f'<GameServer {self.name} ({self.game_type})>' 