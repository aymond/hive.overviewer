from app import db
from datetime import datetime
import json

class GameConfig(db.Model):
    """Model for storing game configuration files."""
    __tablename__ = 'game_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(32), nullable=False, default='json')  # json, ini, yaml, etc.
    is_active = db.Column(db.Boolean, default=True)
    content = db.Column(db.Text, nullable=True)  # Stores the actual config content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    game_server_id = db.Column(db.Integer, db.ForeignKey('game_servers.id'), nullable=False)
    
    def __init__(self, name, file_path, game_server_id, file_type='json', content=None, is_active=True):
        self.name = name
        self.file_path = file_path
        self.file_type = file_type
        self.content = content
        self.is_active = is_active
        self.game_server_id = game_server_id
    
    def get_content_as_dict(self):
        """Parse and return the content as a Python dictionary."""
        if not self.content:
            return {}
            
        if self.file_type == 'json':
            try:
                return json.loads(self.content)
            except json.JSONDecodeError:
                return {}
        else:
            # For non-JSON formats, return a simple message
            return {"message": f"Content is in {self.file_type} format and can't be displayed as JSON"}
    
    def update_content(self, new_content):
        """Update the configuration content."""
        self.content = new_content
        self.updated_at = datetime.utcnow()
    
    def toggle_active(self):
        """Toggle the active status of this configuration."""
        self.is_active = not self.is_active
        self.updated_at = datetime.utcnow()
        return self.is_active
    
    def to_dict(self):
        """Return config as dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'is_active': self.is_active,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'game_server_id': self.game_server_id
        }
    
    def __repr__(self):
        return f'<GameConfig {self.name} ({self.file_type})>' 