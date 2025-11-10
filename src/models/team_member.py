"""TeamMember model for team membership management.

This module defines the TeamMember model for managing team membership
and team lead assignments.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class TeamMember(db.Model):
    """TeamMember model for team membership.
    
    Attributes:
        id: Primary key
        team_id: Foreign key to teams table
        user_id: Foreign key to users table
        is_team_lead: Whether user is a team lead
        joined_at: Membership start timestamp
    """
    
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    is_team_lead = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint for team-user combination
    __table_args__ = (
        db.UniqueConstraint('team_id', 'user_id', name='unique_team_user'),
    )
    
    # Relationships
    member = db.relationship('User', backref='team_memberships', lazy='joined')
    
    @classmethod
    def create(cls, team_id: int, user_id: int, is_team_lead: bool = False) -> 'TeamMember':
        """Create a new team membership.
        
        Args:
            team_id: Team's unique identifier
            user_id: User's unique identifier
            is_team_lead: Whether user is a team lead (default: False)
            
        Returns:
            Created TeamMember instance
        """
        membership = cls(
            team_id=team_id,
            user_id=user_id,
            is_team_lead=is_team_lead
        )
        db.session.add(membership)
        db.session.commit()
        return membership
    
    @classmethod
    def get_by_id(cls, membership_id: int) -> Optional['TeamMember']:
        """Retrieve team membership by ID.
        
        Args:
            membership_id: Membership's unique identifier
            
        Returns:
            TeamMember instance or None if not found
        """
        return cls.query.filter_by(id=membership_id).first()
    
    @classmethod
    def get_by_team_and_user(cls, team_id: int, user_id: int) -> Optional['TeamMember']:
        """Retrieve membership by team and user.
        
        Args:
            team_id: Team's unique identifier
            user_id: User's unique identifier
            
        Returns:
            TeamMember instance or None if not found
        """
        return cls.query.filter_by(team_id=team_id, user_id=user_id).first()
    
    @classmethod
    def get_by_team(cls, team_id: int) -> List['TeamMember']:
        """Retrieve all members of a team.
        
        Args:
            team_id: Team's unique identifier
            
        Returns:
            List of TeamMember instances
        """
        return cls.query.filter_by(team_id=team_id).all()
    
    @classmethod
    def get_by_user(cls, user_id: int) -> List['TeamMember']:
        """Retrieve all teams a user belongs to.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            List of TeamMember instances
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_team_leads(cls, team_id: int) -> List['TeamMember']:
        """Retrieve all team leads for a specific team.
        
        Args:
            team_id: Team's unique identifier
            
        Returns:
            List of TeamMember instances where is_team_lead=True
        """
        return cls.query.filter_by(team_id=team_id, is_team_lead=True).all()
    
    def update(self, **kwargs) -> 'TeamMember':
        """Update team membership attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated TeamMember instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete team membership from database."""
        db.session.delete(self)
        db.session.commit()
    
    def promote_to_lead(self) -> 'TeamMember':
        """Promote member to team lead.
        
        Returns:
            Updated TeamMember instance
        """
        self.is_team_lead = True
        db.session.commit()
        return self
    
    def demote_from_lead(self) -> 'TeamMember':
        """Demote team lead to regular member.
        
        Returns:
            Updated TeamMember instance
        """
        self.is_team_lead = False
        db.session.commit()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert team membership to dictionary.
        
        Returns:
            Dictionary representation of team membership
        """
        return {
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id,
            'is_team_lead': self.is_team_lead,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of TeamMember."""
        lead_status = 'Lead' if self.is_team_lead else 'Member'
        return f'<TeamMember user_id={self.user_id} team_id={self.team_id} ({lead_status})>'
