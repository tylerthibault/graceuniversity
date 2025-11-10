"""Enrollment model for course assignments.

This module defines the Enrollment model for managing user course
enrollments and progress tracking.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class Enrollment(db.Model):
    """Enrollment model for user course assignments.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        course_id: Foreign key to courses table
        team_id: Foreign key to teams table (which team assigned this)
        assigned_by: Foreign key to users table (who assigned)
        soft_deadline: Recommended completion date
        hard_deadline: Required completion date
        enrolled_at: Enrollment timestamp
        started_at: When user started the course
        completed_at: When user completed the course
        status: Enrollment status (not_started, in_progress, completed, expired)
        score: Final percentage score if applicable
    """
    
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), index=True)
    assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    soft_deadline = db.Column(db.DateTime)
    hard_deadline = db.Column(db.DateTime)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='not_started', index=True)
    score = db.Column(db.Integer)
    
    # Relationships
    assigner = db.relationship('User', foreign_keys=[assigned_by], lazy='joined')
    
    # Unique constraint for user-course-team combination
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', 'team_id', name='unique_user_course_team'),
    )
    
    @classmethod
    def create(cls, user_id: int, course_id: int, assigned_by: int,
               team_id: Optional[int] = None, soft_deadline: Optional[datetime] = None,
               hard_deadline: Optional[datetime] = None) -> 'Enrollment':
        """Create a new enrollment.
        
        Args:
            user_id: User's unique identifier
            course_id: Course's unique identifier
            assigned_by: User ID who assigned the course
            team_id: Team's unique identifier (optional)
            soft_deadline: Recommended completion date (optional)
            hard_deadline: Required completion date (optional)
            
        Returns:
            Created Enrollment instance
        """
        enrollment = cls(
            user_id=user_id,
            course_id=course_id,
            assigned_by=assigned_by,
            team_id=team_id,
            soft_deadline=soft_deadline,
            hard_deadline=hard_deadline
        )
        db.session.add(enrollment)
        db.session.commit()
        return enrollment
    
    @classmethod
    def get_by_id(cls, enrollment_id: int) -> Optional['Enrollment']:
        """Retrieve enrollment by ID.
        
        Args:
            enrollment_id: Enrollment's unique identifier
            
        Returns:
            Enrollment instance or None if not found
        """
        return cls.query.filter_by(id=enrollment_id).first()
    
    @classmethod
    def get_by_user(cls, user_id: int, status: Optional[str] = None) -> List['Enrollment']:
        """Retrieve all enrollments for a user.
        
        Args:
            user_id: User's unique identifier
            status: Filter by status (optional)
            
        Returns:
            List of Enrollment instances
        """
        query = cls.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()
    
    @classmethod
    def get_by_course(cls, course_id: int, status: Optional[str] = None) -> List['Enrollment']:
        """Retrieve all enrollments for a course.
        
        Args:
            course_id: Course's unique identifier
            status: Filter by status (optional)
            
        Returns:
            List of Enrollment instances
        """
        query = cls.query.filter_by(course_id=course_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()
    
    @classmethod
    def get_by_team(cls, team_id: int, status: Optional[str] = None) -> List['Enrollment']:
        """Retrieve all enrollments for a team.
        
        Args:
            team_id: Team's unique identifier
            status: Filter by status (optional)
            
        Returns:
            List of Enrollment instances
        """
        query = cls.query.filter_by(team_id=team_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()
    
    @classmethod
    def get_user_course_enrollment(cls, user_id: int, course_id: int) -> Optional['Enrollment']:
        """Get specific user-course enrollment.
        
        Args:
            user_id: User's unique identifier
            course_id: Course's unique identifier
            
        Returns:
            Enrollment instance or None if not found
        """
        return cls.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    def update(self, **kwargs) -> 'Enrollment':
        """Update enrollment attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Enrollment instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete enrollment from database."""
        db.session.delete(self)
        db.session.commit()
    
    def start(self) -> 'Enrollment':
        """Mark enrollment as started.
        
        Returns:
            Updated Enrollment instance
        """
        if not self.started_at:
            self.started_at = datetime.utcnow()
        self.status = 'in_progress'
        db.session.commit()
        return self
    
    def complete(self, score: Optional[int] = None) -> 'Enrollment':
        """Mark enrollment as completed.
        
        Args:
            score: Final score percentage (optional)
            
        Returns:
            Updated Enrollment instance
        """
        self.completed_at = datetime.utcnow()
        self.status = 'completed'
        if score is not None:
            self.score = score
        db.session.commit()
        return self
    
    def expire(self) -> 'Enrollment':
        """Mark enrollment as expired.
        
        Returns:
            Updated Enrollment instance
        """
        self.status = 'expired'
        db.session.commit()
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert enrollment to dictionary.
        
        Returns:
            Dictionary representation of enrollment
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'team_id': self.team_id,
            'assigned_by': self.assigned_by,
            'soft_deadline': self.soft_deadline.isoformat() if self.soft_deadline else None,
            'hard_deadline': self.hard_deadline.isoformat() if self.hard_deadline else None,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'score': self.score,
        }
    
    def __repr__(self) -> str:
        """String representation of Enrollment."""
        return f'<Enrollment user={self.user_id} course={self.course_id} status={self.status}>'
