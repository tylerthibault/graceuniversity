"""Lesson model for course content.

This module defines the Lesson model for managing individual lessons
within courses. Supports multiple content types.
"""

from typing import Optional, List, Dict, Any
import json
from datetime import datetime
from src.models import db


class Lesson(db.Model):
    """Lesson model for course content.
    
    Attributes:
        id: Primary key
        course_id: Foreign key to courses table
        title: Lesson title
        content_type: Type of content (video, pdf, quiz, interactive, link, live_session)
        content_url: URL or file path to content
        content_data: JSON data for quizzes, interactive content
        order_index: Display order within course
        is_required: Whether lesson is required for completion
        created_at: Lesson creation timestamp
    """
    
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    content_url = db.Column(db.Text)
    content_data = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    is_required = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress_records = db.relationship('LessonProgress', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    
    # Composite index for course ordering
    __table_args__ = (
        db.Index('idx_course_order', 'course_id', 'order_index'),
    )
    
    @classmethod
    def create(cls, course_id: int, title: str, content_type: str, order_index: int,
               content_url: Optional[str] = None, content_data: Optional[Dict] = None,
               is_required: bool = True) -> 'Lesson':
        """Create a new lesson.
        
        Args:
            course_id: Course's unique identifier
            title: Lesson title
            content_type: Type of content
            order_index: Display order within course
            content_url: URL or file path (optional)
            content_data: Dictionary for quiz/interactive content (optional)
            is_required: Whether lesson is required (default: True)
            
        Returns:
            Created Lesson instance
        """
        lesson = cls(
            course_id=course_id,
            title=title,
            content_type=content_type,
            order_index=order_index,
            content_url=content_url,
            content_data=json.dumps(content_data) if content_data else None,
            is_required=is_required
        )
        db.session.add(lesson)
        db.session.commit()
        return lesson
    
    @classmethod
    def get_by_id(cls, lesson_id: int) -> Optional['Lesson']:
        """Retrieve lesson by ID.
        
        Args:
            lesson_id: Lesson's unique identifier
            
        Returns:
            Lesson instance or None if not found
        """
        return cls.query.filter_by(id=lesson_id).first()
    
    @classmethod
    def get_by_course(cls, course_id: int, ordered: bool = True) -> List['Lesson']:
        """Retrieve all lessons for a course.
        
        Args:
            course_id: Course's unique identifier
            ordered: Whether to order by order_index (default: True)
            
        Returns:
            List of Lesson instances
        """
        query = cls.query.filter_by(course_id=course_id)
        if ordered:
            query = query.order_by(cls.order_index)
        return query.all()
    
    @classmethod
    def get_required_lessons(cls, course_id: int) -> List['Lesson']:
        """Retrieve all required lessons for a course.
        
        Args:
            course_id: Course's unique identifier
            
        Returns:
            List of required Lesson instances
        """
        return cls.query.filter_by(
            course_id=course_id,
            is_required=True
        ).order_by(cls.order_index).all()
    
    def update(self, **kwargs) -> 'Lesson':
        """Update lesson attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated Lesson instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'content_data' and isinstance(value, dict):
                    setattr(self, key, json.dumps(value))
                else:
                    setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete lesson from database."""
        db.session.delete(self)
        db.session.commit()
    
    def get_content_data_dict(self) -> Optional[Dict]:
        """Parse and return content_data as dictionary.
        
        Returns:
            Dictionary of content data or None
        """
        if self.content_data:
            try:
                return json.loads(self.content_data)
            except json.JSONDecodeError:
                return None
        return None
    
    def set_content_data(self, data: Dict) -> None:
        """Set content_data from dictionary.
        
        Args:
            data: Dictionary to store as JSON
        """
        self.content_data = json.dumps(data)
        db.session.commit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lesson to dictionary.
        
        Returns:
            Dictionary representation of lesson
        """
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'content_type': self.content_type,
            'content_url': self.content_url,
            'content_data': self.get_content_data_dict(),
            'order_index': self.order_index,
            'is_required': self.is_required,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of Lesson."""
        return f'<Lesson {self.title} ({self.content_type})>'
