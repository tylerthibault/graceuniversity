"""CoursePrerequisite model for course dependencies.

This module defines the CoursePrerequisite model for managing
prerequisite relationships between courses.
"""

from typing import Optional, List, Dict, Any
from src.models import db


class CoursePrerequisite(db.Model):
    """CoursePrerequisite model for course dependencies.
    
    Attributes:
        id: Primary key
        course_id: Foreign key to courses table (the course with prerequisites)
        prerequisite_course_id: Foreign key to courses table (the required course)
    """
    
    __tablename__ = 'course_prerequisites'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    prerequisite_course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    
    # Unique constraint for course-prerequisite combination
    __table_args__ = (
        db.UniqueConstraint('course_id', 'prerequisite_course_id', name='unique_course_prerequisite'),
    )
    
    # Relationships
    prerequisite = db.relationship('Course', foreign_keys=[prerequisite_course_id], lazy='joined')
    
    @classmethod
    def create(cls, course_id: int, prerequisite_course_id: int) -> 'CoursePrerequisite':
        """Create a new course prerequisite relationship.
        
        Args:
            course_id: Course's unique identifier
            prerequisite_course_id: Prerequisite course's unique identifier
            
        Returns:
            Created CoursePrerequisite instance
        """
        prerequisite = cls(
            course_id=course_id,
            prerequisite_course_id=prerequisite_course_id
        )
        db.session.add(prerequisite)
        db.session.commit()
        return prerequisite
    
    @classmethod
    def get_by_id(cls, prerequisite_id: int) -> Optional['CoursePrerequisite']:
        """Retrieve prerequisite by ID.
        
        Args:
            prerequisite_id: Prerequisite's unique identifier
            
        Returns:
            CoursePrerequisite instance or None if not found
        """
        return cls.query.filter_by(id=prerequisite_id).first()
    
    @classmethod
    def get_by_course(cls, course_id: int) -> List['CoursePrerequisite']:
        """Retrieve all prerequisites for a course.
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            List of CoursePrerequisite instances
        """
        return cls.query.filter_by(course_id=course_id).all()
    
    @classmethod
    def get_courses_requiring(cls, prerequisite_course_id: int) -> List['CoursePrerequisite']:
        """Retrieve all courses that require a specific prerequisite.
        
        Args:
            prerequisite_course_id: Prerequisite course's unique identifier
            
        Returns:
            List of CoursePrerequisite instances
        """
        return cls.query.filter_by(prerequisite_course_id=prerequisite_course_id).all()
    
    @classmethod
    def exists(cls, course_id: int, prerequisite_course_id: int) -> bool:
        """Check if a prerequisite relationship exists.
        
        Args:
            course_id: Course's unique identifier
            prerequisite_course_id: Prerequisite course's unique identifier
            
        Returns:
            True if relationship exists
        """
        return cls.query.filter_by(
            course_id=course_id,
            prerequisite_course_id=prerequisite_course_id
        ).first() is not None
    
    def delete(self) -> None:
        """Delete prerequisite relationship from database."""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def delete_by_course(cls, course_id: int) -> int:
        """Delete all prerequisites for a specific course.
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            Number of prerequisites deleted
        """
        prerequisites = cls.query.filter_by(course_id=course_id).all()
        count = len(prerequisites)
        for prereq in prerequisites:
            db.session.delete(prereq)
        db.session.commit()
        return count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert prerequisite to dictionary.
        
        Returns:
            Dictionary representation of prerequisite
        """
        return {
            'id': self.id,
            'course_id': self.course_id,
            'prerequisite_course_id': self.prerequisite_course_id,
        }
    
    def __repr__(self) -> str:
        """String representation of CoursePrerequisite."""
        return f'<CoursePrerequisite course={self.course_id} requires={self.prerequisite_course_id}>'
