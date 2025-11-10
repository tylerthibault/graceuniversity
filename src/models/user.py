"""User model for authentication and role management.

This module defines the User model for the Grace University LMS.
Users can have multiple roles: superuser, admin, team_lead, or doorholder.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db
from src.models.role import user_roles


class User(db.Model):
    """User model for authentication and authorization.
    
    Attributes:
        id: Primary key
        email: User's unique email address
        password_hash: Bcrypt hashed password
        name: User's full name
        phone: User's phone number
        roles: Many-to-many relationship with Role model
        is_active: Whether the account is active
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    roles = db.relationship(
        'Role',
        secondary=user_roles,
        back_populates='users',
        lazy='dynamic'
    )
    sessions = db.relationship('Session', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', foreign_keys='Enrollment.user_id')
    certificates = db.relationship('Certificate', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    @classmethod
    def create(cls, email: str, password_hash: str, name: str, 
               roles: Optional[List['Role']] = None, phone: Optional[str] = None) -> 'User':
        """Create a new user.
        
        Args:
            email: User's email address
            password_hash: Bcrypt hashed password
            name: User's full name
            roles: List of Role instances to assign (optional)
            phone: User's phone number (optional)
            
        Returns:
            Created User instance
        """
        user = cls(
            email=email,
            password_hash=password_hash,
            name=name,
            phone=phone
        )
        db.session.add(user)
        
        # Assign roles if provided
        if roles:
            for role in roles:
                user.roles.append(role)
        
        db.session.commit()
        return user
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Retrieve user by ID.
        
        Args:
            user_id: User's unique identifier
            
        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Retrieve user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User instance or None if not found
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_all(cls, is_active: Optional[bool] = None) -> List['User']:
        """Retrieve all users with optional active filter.
        
        Args:
            is_active: Filter by active status (None = all users)
            
        Returns:
            List of User instances
        """
        query = cls.query
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        return query.all()
    
    @classmethod
    def get_by_role(cls, role_name: str) -> List['User']:
        """Retrieve all users with a specific role.
        
        Args:
            role_name: Role name to filter by
            
        Returns:
            List of User instances with that role
        """
        from models.role import Role
        role = Role.get_by_name(role_name)
        if not role:
            return []
        return role.users.all()
    
    def add_role(self, role: 'Role') -> 'User':
        """Add a role to the user.
        
        Args:
            role: Role instance to add
            
        Returns:
            Updated User instance
        """
        if role not in self.roles:
            self.roles.append(role)
            db.session.commit()
        return self
    
    def remove_role(self, role: 'Role') -> 'User':
        """Remove a role from the user.
        
        Args:
            role: Role instance to remove
            
        Returns:
            Updated User instance
        """
        if role in self.roles:
            self.roles.remove(role)
            db.session.commit()
        return self
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role.
        
        Args:
            role_name: Role name to check
            
        Returns:
            True if user has the role, False otherwise
        """
        return any(role.name == role_name for role in self.roles)
    
    def has_any_role(self, role_names: List[str]) -> bool:
        """Check if user has any of the specified roles.
        
        Args:
            role_names: List of role names to check
            
        Returns:
            True if user has at least one role, False otherwise
        """
        return any(self.has_role(role_name) for role_name in role_names)
    
    def has_all_roles(self, role_names: List[str]) -> bool:
        """Check if user has all of the specified roles.
        
        Args:
            role_names: List of role names to check
            
        Returns:
            True if user has all roles, False otherwise
        """
        return all(self.has_role(role_name) for role_name in role_names)
    
    def get_role_names(self) -> List[str]:
        """Get list of role names for this user.
        
        Returns:
            List of role names
        """
        return [role.name for role in self.roles]
    
    def get_primary_role(self) -> Optional[str]:
        """Get the primary (highest priority) role for the user.
        
        Priority order: superuser > admin > team_lead > doorholder
        
        Returns:
            Primary role name or None if no roles
        """
        role_priority = ['superuser', 'admin', 'team_lead', 'doorholder']
        user_roles = self.get_role_names()
        
        for role in role_priority:
            if role in user_roles:
                return role
        
        # If user has roles but none match priority, return first role
        return user_roles[0] if user_roles else None
    
    def update(self, **kwargs) -> 'User':
        """Update user attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated User instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()
    
    def deactivate(self) -> 'User':
        """Deactivate user account.
        
        Returns:
            Updated User instance
        """
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def activate(self) -> 'User':
        """Activate user account.
        
        Returns:
            Updated User instance
        """
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary.
        
        Returns:
            Dictionary representation of user
        """
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'roles': self.get_role_names(),
            'primary_role': self.get_primary_role(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
    
    def __repr__(self) -> str:
        """String representation of User."""
        roles_str = ', '.join(self.get_role_names()) if self.get_role_names() else 'No roles'
        return f'<User {self.email} ({roles_str})>'
