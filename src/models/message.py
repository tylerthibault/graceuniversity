"""Message model for direct messaging between users.

This module defines the Message model for user-to-user
communication within the LMS.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class Message(db.Model):
    """Message model for direct messaging.
    
    Attributes:
        id: Primary key
        sender_id: Foreign key to users table (sender)
        recipient_id: Foreign key to users table (recipient)
        subject: Message subject
        body: Message body content
        is_read: Whether message has been read
        sent_at: Message sent timestamp
    """
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    subject = db.Column(db.String(200))
    body = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, index=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy='joined')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages', lazy='joined')
    
    @classmethod
    def create(cls, sender_id: int, recipient_id: int, body: str,
               subject: Optional[str] = None) -> 'Message':
        """Create a new message.
        
        Args:
            sender_id: Sender's user ID
            recipient_id: Recipient's user ID
            body: Message content
            subject: Message subject (optional)
            
        Returns:
            Created Message instance
        """
        message = cls(
            sender_id=sender_id,
            recipient_id=recipient_id,
            subject=subject,
            body=body
        )
        db.session.add(message)
        db.session.commit()
        return message
    
    @classmethod
    def get_by_id(cls, message_id: int) -> Optional['Message']:
        """Retrieve message by ID.
        
        Args:
            message_id: Message's unique identifier
            
        Returns:
            Message instance or None if not found
        """
        return cls.query.filter_by(id=message_id).first()
    
    @classmethod
    def get_by_sender(cls, sender_id: int) -> List['Message']:
        """Retrieve all messages sent by a user.
        
        Args:
            sender_id: Sender's user ID
            
        Returns:
            List of Message instances
        """
        return cls.query.filter_by(sender_id=sender_id).order_by(cls.sent_at.desc()).all()
    
    @classmethod
    def get_by_recipient(cls, recipient_id: int, unread_only: bool = False) -> List['Message']:
        """Retrieve all messages received by a user.
        
        Args:
            recipient_id: Recipient's user ID
            unread_only: Only return unread messages (default: False)
            
        Returns:
            List of Message instances
        """
        query = cls.query.filter_by(recipient_id=recipient_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(cls.sent_at.desc()).all()
    
    @classmethod
    def get_conversation(cls, user1_id: int, user2_id: int) -> List['Message']:
        """Retrieve all messages between two users.
        
        Args:
            user1_id: First user's ID
            user2_id: Second user's ID
            
        Returns:
            List of Message instances ordered by time
        """
        return cls.query.filter(
            ((cls.sender_id == user1_id) & (cls.recipient_id == user2_id)) |
            ((cls.sender_id == user2_id) & (cls.recipient_id == user1_id))
        ).order_by(cls.sent_at.asc()).all()
    
    @classmethod
    def get_unread_count(cls, user_id: int) -> int:
        """Get count of unread messages for a user.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            Number of unread messages
        """
        return cls.query.filter_by(recipient_id=user_id, is_read=False).count()
    
    def update(self, **kwargs) -> 'Message':
        """Update message attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Message instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete message from database."""
        db.session.delete(self)
        db.session.commit()
    
    def mark_as_read(self) -> 'Message':
        """Mark message as read.
        
        Returns:
            Updated Message instance
        """
        self.is_read = True
        db.session.commit()
        return self
    
    def mark_as_unread(self) -> 'Message':
        """Mark message as unread.
        
        Returns:
            Updated Message instance
        """
        self.is_read = False
        db.session.commit()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary.
        
        Returns:
            Dictionary representation of message
        """
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'subject': self.subject,
            'body': self.body,
            'is_read': self.is_read,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of Message."""
        read_status = 'Read' if self.is_read else 'Unread'
        return f'<Message from={self.sender_id} to={self.recipient_id} ({read_status})>'
