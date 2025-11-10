"""Team model for ministry areas.

This module defines the Team model for organizing doorholders
by ministry area (parking, greeting, ushers, kids, etc.).
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class Team(db.Model):
    """Team model for ministry organization.
    
    Attributes:
        id: Primary key
        name: Team name
        ministry_area: Ministry area (parking, greeting, ushers, kids)
        description: Team description
        is_active: Whether the team is active
        created_at: Team creation timestamp
    """
    
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ministry_area = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='team', lazy='dynamic')
    announcements = db.relationship('Announcement', backref='team', lazy='dynamic')
    
    @classmethod
    def create(cls, name: str, ministry_area: str, description: Optional[str] = None) -> 'Team':
        """Create a new team.
        
        Args:
            name: Team name
            ministry_area: Ministry area
            description: Team description (optional)
            
        Returns:
            Created Team instance
        """
        team = cls(
            name=name,
            ministry_area=ministry_area,
            description=description
        )
        db.session.add(team)
        db.session.commit()
        return team
    
    @classmethod
    def get_by_id(cls, team_id: int) -> Optional['Team']:
        """Retrieve team by ID.
        
        Args:
            team_id: Team's unique identifier
            
        Returns:
            Team instance or None if not found
        """
        return cls.query.filter_by(id=team_id).first()
    
    @classmethod
    def get_all(cls, is_active: Optional[bool] = None) -> List['Team']:
        """Retrieve all teams with optional active filter.
        
        Args:
            is_active: Filter by active status (None = all teams)
            
        Returns:
            List of Team instances
        """
        query = cls.query
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        return query.all()
    
    @classmethod
    def get_by_ministry_area(cls, ministry_area: str) -> List['Team']:
        """Retrieve all teams in a ministry area.
        
        Args:
            ministry_area: Ministry area to filter by
            
        Returns:
            List of Team instances
        """
        return cls.query.filter_by(ministry_area=ministry_area, is_active=True).all()
    
    def update(self, **kwargs) -> 'Team':
        """Update team attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Team instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete team from database."""
        db.session.delete(self)
        db.session.commit()
    
    def deactivate(self) -> 'Team':
        """Deactivate team.
        
        Returns:
            Updated Team instance
        """
        self.is_active = False
        db.session.commit()
        return self
    
    def activate(self) -> 'Team':
        """Activate team.
        
        Returns:
            Updated Team instance
        """
        self.is_active = True
        db.session.commit()
        return self
    
    def get_member_count(self) -> int:
        """Get total number of team members.
        
        Returns:
            Number of members
        """
        return self.members.count()
    
    def get_team_leads(self) -> List['TeamMember']:
        """Get all team leads for this team.
        
        Returns:
            List of TeamMember instances where is_team_lead=True
        """
        return self.members.filter_by(is_team_lead=True).all()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert team to dictionary.
        
        Returns:
            Dictionary representation of team
        """
        return {
            'id': self.id,
            'name': self.name,
            'ministry_area': self.ministry_area,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'member_count': self.get_member_count(),
        }
    
    def __repr__(self) -> str:
        """String representation of Team."""
        return f'<Team {self.name} ({self.ministry_area})>'
