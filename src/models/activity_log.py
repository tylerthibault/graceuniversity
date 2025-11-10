"""ActivityLog model for tracking user actions.

This module defines the ActivityLog model for logging
user activities throughout the system.
"""

from typing import Optional, List, Dict, Any
import json
from datetime import datetime, timedelta
from src.models import db


class ActivityLog(db.Model):
    """ActivityLog model for user activity tracking.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        action: Action performed (login, logout, course_complete, etc)
        details: JSON data with additional context
        created_at: Activity timestamp
    """
    
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', backref='activity_logs', lazy='joined')
    
    @classmethod
    def create(cls, user_id: int, action: str, details: Optional[Dict] = None) -> 'ActivityLog':
        """Create a new activity log entry.
        
        Args:
            user_id: User's unique identifier
            action: Action performed
            details: Dictionary with additional context (optional)
            
        Returns:
            Created ActivityLog instance
        """
        log = cls(
            user_id=user_id,
            action=action,
            details=json.dumps(details) if details else None
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def get_by_id(cls, log_id: int) -> Optional['ActivityLog']:
        """Retrieve activity log by ID.
        
        Args:
            log_id: Log's unique identifier
            
        Returns:
            ActivityLog instance or None if not found
        """
        return cls.query.filter_by(id=log_id).first()
    
    @classmethod
    def get_by_user(cls, user_id: int, limit: Optional[int] = None) -> List['ActivityLog']:
        """Retrieve activity logs for a user.
        
        Args:
            user_id: User's unique identifier
            limit: Maximum number of logs to return (optional)
            
        Returns:
            List of ActivityLog instances
        """
        query = cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_by_action(cls, action: str, limit: Optional[int] = None) -> List['ActivityLog']:
        """Retrieve logs by action type.
        
        Args:
            action: Action type to filter by
            limit: Maximum number of logs to return (optional)
            
        Returns:
            List of ActivityLog instances
        """
        query = cls.query.filter_by(action=action).order_by(cls.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_recent(cls, limit: int = 100) -> List['ActivityLog']:
        """Retrieve most recent activity logs.
        
        Args:
            limit: Maximum number of logs to return (default: 100)
            
        Returns:
            List of ActivityLog instances
        """
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_by_date_range(cls, start_date: datetime, end_date: datetime,
                          user_id: Optional[int] = None) -> List['ActivityLog']:
        """Retrieve logs within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            user_id: Filter by user (optional)
            
        Returns:
            List of ActivityLog instances
        """
        query = cls.query.filter(
            cls.created_at >= start_date,
            cls.created_at <= end_date
        )
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.order_by(cls.created_at.desc()).all()
    
    def delete(self) -> None:
        """Delete activity log from database."""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def cleanup_old_logs(cls, days: int = 90) -> int:
        """Delete logs older than specified days.
        
        Args:
            days: Number of days to keep (default: 90)
            
        Returns:
            Number of logs deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_logs = cls.query.filter(cls.created_at < cutoff_date).all()
        count = len(old_logs)
        for log in old_logs:
            db.session.delete(log)
        db.session.commit()
        return count
    
    def get_details_dict(self) -> Optional[Dict]:
        """Parse and return details as dictionary.
        
        Returns:
            Dictionary of details or None
        """
        if self.details:
            try:
                return json.loads(self.details)
            except json.JSONDecodeError:
                return None
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert activity log to dictionary.
        
        Returns:
            Dictionary representation of activity log
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'details': self.get_details_dict(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of ActivityLog."""
        return f'<ActivityLog user={self.user_id} action={self.action}>'
