"""Session model for user authentication sessions.

This module defines the Session model for managing user login sessions
with token-based authentication.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from src.models import db


class Session(db.Model):
    """Session model for user authentication.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        token: Unique session token
        expires_at: Session expiration timestamp
        created_at: Session creation timestamp
    """
    
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def create(cls, user_id: int, token: str, expires_in_hours: int = 24) -> 'Session':
        """Create a new session.
        
        Args:
            user_id: User's unique identifier
            token: Unique session token
            expires_in_hours: Session duration in hours (default: 24)
            
        Returns:
            Created Session instance
        """
        expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
        session = cls(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.session.add(session)
        db.session.commit()
        return session
    
    @classmethod
    def get_by_token(cls, token: str) -> Optional['Session']:
        """Retrieve session by token.
        
        Args:
            token: Session token
            
        Returns:
            Session instance or None if not found
        """
        return cls.query.filter_by(token=token).first()
    
    @classmethod
    def get_valid_session(cls, token: str) -> Optional['Session']:
        """Retrieve valid (non-expired) session by token.
        
        Args:
            token: Session token
            
        Returns:
            Session instance or None if not found or expired
        """
        session = cls.query.filter_by(token=token).first()
        if session and session.is_valid():
            return session
        return None
    
    @classmethod
    def get_by_user_id(cls, user_id: int) -> List['Session']:
        """Retrieve all sessions for a user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            List of Session instances
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def cleanup_expired(cls) -> int:
        """Delete all expired sessions.
        
        Returns:
            Number of sessions deleted
        """
        expired_sessions = cls.query.filter(cls.expires_at < datetime.utcnow()).all()
        count = len(expired_sessions)
        for session in expired_sessions:
            db.session.delete(session)
        db.session.commit()
        return count
    
    def is_valid(self) -> bool:
        """Check if session is still valid.
        
        Returns:
            True if session has not expired
        """
        return datetime.utcnow() < self.expires_at
    
    def extend(self, hours: int = 24) -> 'Session':
        """Extend session expiration time.
        
        Args:
            hours: Number of hours to extend
            
        Returns:
            Updated Session instance
        """
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete session from database."""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def delete_user_sessions(cls, user_id: int) -> int:
        """Delete all sessions for a specific user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Number of sessions deleted
        """
        sessions = cls.query.filter_by(user_id=user_id).all()
        count = len(sessions)
        for session in sessions:
            db.session.delete(session)
        db.session.commit()
        return count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary.
        
        Returns:
            Dictionary representation of session
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_valid': self.is_valid(),
        }
    
    def __repr__(self) -> str:
        """String representation of Session."""
        return f'<Session user_id={self.user_id} expires={self.expires_at}>'
