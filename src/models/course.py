"""Course model for training courses.

This module defines the Course model for managing training courses
in the Grace University LMS.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from src.models import db


class Course(db.Model):
    """Course model for training content.
    
    Attributes:
        id: Primary key
        title: Course title
        description: Course description
        is_campus_wide: Whether course is campus-wide or team-specific
        completion_method: How course is completed (honor_system, assessment, manual_approval)
        passing_score: Percentage required to pass (for assessment method)
        certificate_enabled: Whether certificates are issued
        certificate_expires: Whether certificates expire
        expiration_months: Months until recertification needed
        created_by: Foreign key to users table (creator)
        is_active: Whether the course is active
        created_at: Course creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_campus_wide = db.Column(db.Boolean, default=False, index=True)
    completion_method = db.Column(db.String(50), default='honor_system')
    passing_score = db.Column(db.Integer, default=0)
    certificate_enabled = db.Column(db.Boolean, default=True)
    certificate_expires = db.Column(db.Boolean, default=False)
    expiration_months = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_courses', lazy='joined')
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    prerequisites = db.relationship(
        'CoursePrerequisite',
        foreign_keys='CoursePrerequisite.course_id',
        backref='course',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    @classmethod
    def create(cls, title: str, created_by: int, description: Optional[str] = None,
               is_campus_wide: bool = False, completion_method: str = 'honor_system',
               passing_score: int = 0, certificate_enabled: bool = True) -> 'Course':
        """Create a new course.
        
        Args:
            title: Course title
            created_by: User ID of creator
            description: Course description (optional)
            is_campus_wide: Whether course is campus-wide (default: False)
            completion_method: Completion method (default: 'honor_system')
            passing_score: Required passing score percentage (default: 0)
            certificate_enabled: Whether to issue certificates (default: True)
            
        Returns:
            Created Course instance
        """
        course = cls(
            title=title,
            created_by=created_by,
            description=description,
            is_campus_wide=is_campus_wide,
            completion_method=completion_method,
            passing_score=passing_score,
            certificate_enabled=certificate_enabled
        )
        db.session.add(course)
        db.session.commit()
        return course
    
    @classmethod
    def get_by_id(cls, course_id: int) -> Optional['Course']:
        """Retrieve course by ID.
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            Course instance or None if not found
        """
        return cls.query.filter_by(id=course_id).first()
    
    @classmethod
    def get_all(cls, is_active: Optional[bool] = None) -> List['Course']:
        """Retrieve all courses with optional active filter.
        
        Args:
            is_active: Filter by active status (None = all courses)
            
        Returns:
            List of Course instances
        """
        query = cls.query
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        return query.all()
    
    @classmethod
    def get_campus_wide(cls) -> List['Course']:
        """Retrieve all campus-wide courses.
        
        Returns:
            List of Course instances
        """
        return cls.query.filter_by(is_campus_wide=True, is_active=True).all()
    
    @classmethod
    def get_by_creator(cls, user_id: int) -> List['Course']:
        """Retrieve all courses created by a specific user.
        
        Args:
            user_id: Creator's user ID
            
        Returns:
            List of Course instances
        """
        return cls.query.filter_by(created_by=user_id).all()
    
    def update(self, **kwargs) -> 'Course':
        """Update course attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Course instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete course from database."""
        db.session.delete(self)
        db.session.commit()
    
    def deactivate(self) -> 'Course':
        """Deactivate course.
        
        Returns:
            Updated Course instance
        """
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def activate(self) -> 'Course':
        """Activate course.
        
        Returns:
            Updated Course instance
        """
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
    
    def get_lesson_count(self) -> int:
        """Get total number of lessons in course.
        
        Returns:
            Number of lessons
        """
        return self.lessons.count()
    
    def get_enrollment_count(self) -> int:
        """Get total number of enrollments.
        
        Returns:
            Number of enrollments
        """
        return self.enrollments.count()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert course to dictionary.
        
        Returns:
            Dictionary representation of course
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_campus_wide': self.is_campus_wide,
            'completion_method': self.completion_method,
            'passing_score': self.passing_score,
            'certificate_enabled': self.certificate_enabled,
            'certificate_expires': self.certificate_expires,
            'expiration_months': self.expiration_months,
            'created_by': self.created_by,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'lesson_count': self.get_lesson_count(),
            'enrollment_count': self.get_enrollment_count(),
        }
    
    def __repr__(self) -> str:
        """String representation of Course."""
        return f'<Course {self.title}>'
