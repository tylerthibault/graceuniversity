"""Role model for user role management.

This module defines the Role model and user-role association table
for the Grace University LMS. Users can have multiple roles.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


# Association table for many-to-many relationship between users and roles
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow)
)


class Role(db.Model):
    """Role model for user authorization.
    
    Attributes:
        id: Primary key
        name: Role name (superuser, admin, team_lead, doorholder)
        display_name: Human-readable role name
        description: Role description
        is_active: Whether the role is currently active
        created_at: Role creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to users (many-to-many)
    users = db.relationship(
        'User',
        secondary=user_roles,
        back_populates='roles',
        lazy='dynamic'
    )
    
    @classmethod
    def create(cls, name: str, display_name: str, description: Optional[str] = None) -> 'Role':
        """Create a new role.
        
        Args:
            name: Role system name (lowercase, underscores)
            display_name: Human-readable role name
            description: Role description (optional)
            
        Returns:
            Created Role instance
        """
        role = cls(
            name=name,
            display_name=display_name,
            description=description
        )
        db.session.add(role)
        db.session.commit()
        return role
    
    @classmethod
    def get_by_id(cls, role_id: int) -> Optional['Role']:
        """Retrieve role by ID.
        
        Args:
            role_id: Role's unique identifier
            
        Returns:
            Role instance or None if not found
        """
        return cls.query.filter_by(id=role_id).first()
    
    @classmethod
    def get_by_name(cls, name: str) -> Optional['Role']:
        """Retrieve role by name.
        
        Args:
            name: Role's system name
            
        Returns:
            Role instance or None if not found
        """
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_all(cls, is_active: Optional[bool] = None) -> List['Role']:
        """Retrieve all roles with optional active filter.
        
        Args:
            is_active: Filter by active status (None = all roles)
            
        Returns:
            List of Role instances
        """
        query = cls.query
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        return query.all()
    
    @classmethod
    def get_active_roles(cls) -> List['Role']:
        """Retrieve all active roles.
        
        Returns:
            List of active Role instances
        """
        return cls.query.filter_by(is_active=True).all()
    
    def update(self, **kwargs) -> 'Role':
        """Update role attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Role instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete role from database."""
        db.session.delete(self)
        db.session.commit()
    
    def deactivate(self) -> 'Role':
        """Deactivate role.
        
        Returns:
            Updated Role instance
        """
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def activate(self) -> 'Role':
        """Activate role.
        
        Returns:
            Updated Role instance
        """
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def get_users(self) -> List['User']:
        """Get all users with this role.
        
        Returns:
            List of User instances
        """
        return self.users.all()
    
    def get_user_count(self) -> int:
        """Get count of users with this role.
        
        Returns:
            Number of users with this role
        """
        return self.users.count()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert role to dictionary.
        
        Returns:
            Dictionary representation of role
        """
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'is_active': self.is_active,
            'user_count': self.get_user_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of Role."""
        return f'<Role {self.name}>'
