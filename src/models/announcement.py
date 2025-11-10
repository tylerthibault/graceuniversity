"""Announcement model for system and team announcements.

This module defines the Announcement model for managing
system-wide and team-specific announcements.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class Announcement(db.Model):
    """Announcement model for communications.
    
    Attributes:
        id: Primary key
        title: Announcement title
        content: Announcement content
        created_by: Foreign key to users table (creator)
        team_id: Foreign key to teams table (None = system-wide)
        priority: Announcement priority (normal, high, urgent)
        created_at: Creation timestamp
        expires_at: Expiration timestamp (optional)
    """
    
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), index=True)
    priority = db.Column(db.String(50), default='normal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    creator = db.relationship('User', backref='announcements', lazy='joined')
    
    @classmethod
    def create(cls, title: str, content: str, created_by: int,
               team_id: Optional[int] = None, priority: str = 'normal',
               expires_at: Optional[datetime] = None) -> 'Announcement':
        """Create a new announcement.
        
        Args:
            title: Announcement title
            content: Announcement content
            created_by: User ID of creator
            team_id: Team ID for team announcement (None = system-wide)
            priority: Priority level (default: 'normal')
            expires_at: Expiration timestamp (optional)
            
        Returns:
            Created Announcement instance
        """
        announcement = cls(
            title=title,
            content=content,
            created_by=created_by,
            team_id=team_id,
            priority=priority,
            expires_at=expires_at
        )
        db.session.add(announcement)
        db.session.commit()
        return announcement
    
    @classmethod
    def get_by_id(cls, announcement_id: int) -> Optional['Announcement']:
        """Retrieve announcement by ID.
        
        Args:
            announcement_id: Announcement's unique identifier
            
        Returns:
            Announcement instance or None if not found
        """
        return cls.query.filter_by(id=announcement_id).first()
    
    @classmethod
    def get_all(cls, active_only: bool = True) -> List['Announcement']:
        """Retrieve all announcements.
        
        Args:
            active_only: Only return non-expired announcements (default: True)
            
        Returns:
            List of Announcement instances
        """
        query = cls.query
        if active_only:
            query = query.filter(
                (cls.expires_at.is_(None)) | (cls.expires_at > datetime.utcnow())
            )
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_system_wide(cls, active_only: bool = True) -> List['Announcement']:
        """Retrieve all system-wide announcements.
        
        Args:
            active_only: Only return non-expired announcements (default: True)
            
        Returns:
            List of Announcement instances
        """
        query = cls.query.filter_by(team_id=None)
        if active_only:
            query = query.filter(
                (cls.expires_at.is_(None)) | (cls.expires_at > datetime.utcnow())
            )
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_team(cls, team_id: int, active_only: bool = True) -> List['Announcement']:
        """Retrieve all announcements for a specific team.
        
        Args:
            team_id: Team's unique identifier
            active_only: Only return non-expired announcements (default: True)
            
        Returns:
            List of Announcement instances
        """
        query = cls.query.filter_by(team_id=team_id)
        if active_only:
            query = query.filter(
                (cls.expires_at.is_(None)) | (cls.expires_at > datetime.utcnow())
            )
        return query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_priority(cls, priority: str, active_only: bool = True) -> List['Announcement']:
        """Retrieve announcements by priority level.
        
        Args:
            priority: Priority level
            active_only: Only return non-expired announcements (default: True)
            
        Returns:
            List of Announcement instances
        """
        query = cls.query.filter_by(priority=priority)
        if active_only:
            query = query.filter(
                (cls.expires_at.is_(None)) | (cls.expires_at > datetime.utcnow())
            )
        return query.order_by(cls.created_at.desc()).all()
    
    def update(self, **kwargs) -> 'Announcement':
        """Update announcement attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Announcement instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete announcement from database."""
        db.session.delete(self)
        db.session.commit()
    
    def is_active(self) -> bool:
        """Check if announcement is still active.
        
        Returns:
            True if announcement has not expired
        """
        if not self.expires_at:
            return True
        return datetime.utcnow() < self.expires_at
    
    def is_system_wide(self) -> bool:
        """Check if announcement is system-wide.
        
        Returns:
            True if team_id is None
        """
        return self.team_id is None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert announcement to dictionary.
        
        Returns:
            Dictionary representation of announcement
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_by': self.created_by,
            'team_id': self.team_id,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active(),
            'is_system_wide': self.is_system_wide(),
        }
    
    def __repr__(self) -> str:
        """String representation of Announcement."""
        scope = 'System' if self.is_system_wide() else f'Team {self.team_id}'
        return f'<Announcement "{self.title}" ({scope})>'
