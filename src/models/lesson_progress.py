"""LessonProgress model for tracking lesson completion.

This module defines the LessonProgress model for tracking individual
lesson progress for each user.
"""

from typing import Optional, List, Dict, Any
import json
from datetime import datetime
from src.models import db


class LessonProgress(db.Model):
    """LessonProgress model for lesson completion tracking.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        lesson_id: Foreign key to lessons table
        completed: Whether lesson is completed
        time_spent: Time spent on lesson in seconds
        answer_data: JSON data for quiz answers
        completed_at: Completion timestamp
    """
    
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False)
    time_spent = db.Column(db.Integer, default=0)
    answer_data = db.Column(db.Text)
    completed_at = db.Column(db.DateTime)
    
    # Unique constraint for user-lesson combination
    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),
    )
    
    @classmethod
    def create(cls, user_id: int, lesson_id: int) -> 'LessonProgress':
        """Create a new lesson progress record.
        
        Args:
            user_id: User's unique identifier
            lesson_id: Lesson's unique identifier
            
        Returns:
            Created LessonProgress instance
        """
        progress = cls(
            user_id=user_id,
            lesson_id=lesson_id
        )
        db.session.add(progress)
        db.session.commit()
        return progress
    
    @classmethod
    def get_by_id(cls, progress_id: int) -> Optional['LessonProgress']:
        """Retrieve lesson progress by ID.
        
        Args:
            progress_id: Progress record's unique identifier
            
        Returns:
            LessonProgress instance or None if not found
        """
        return cls.query.filter_by(id=progress_id).first()
    
    @classmethod
    def get_by_user_and_lesson(cls, user_id: int, lesson_id: int) -> Optional['LessonProgress']:
        """Retrieve progress for a specific user and lesson.
        
        Args:
            user_id: User's unique identifier
            lesson_id: Lesson's unique identifier
            
        Returns:
            LessonProgress instance or None if not found
        """
        return cls.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    
    @classmethod
    def get_by_user(cls, user_id: int, completed_only: bool = False) -> List['LessonProgress']:
        """Retrieve all lesson progress for a user.
        
        Args:
            user_id: User's unique identifier
            completed_only: Only return completed lessons (default: False)
            
        Returns:
            List of LessonProgress instances
        """
        query = cls.query.filter_by(user_id=user_id)
        if completed_only:
            query = query.filter_by(completed=True)
        return query.all()
    
    @classmethod
    def get_by_lesson(cls, lesson_id: int, completed_only: bool = False) -> List['LessonProgress']:
        """Retrieve all progress records for a lesson.
        
        Args:
            lesson_id: Lesson's unique identifier
            completed_only: Only return completed progress (default: False)
            
        Returns:
            List of LessonProgress instances
        """
        query = cls.query.filter_by(lesson_id=lesson_id)
        if completed_only:
            query = query.filter_by(completed=True)
        return query.all()
    
    @classmethod
    def get_or_create(cls, user_id: int, lesson_id: int) -> 'LessonProgress':
        """Get existing progress or create new one.
        
        Args:
            user_id: User's unique identifier
            lesson_id: Lesson's unique identifier
            
        Returns:
            LessonProgress instance
        """
        progress = cls.get_by_user_and_lesson(user_id, lesson_id)
        if not progress:
            progress = cls.create(user_id, lesson_id)
        return progress
    
    def update(self, **kwargs) -> 'LessonProgress':
        """Update lesson progress attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Updated LessonProgress instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'answer_data' and isinstance(value, dict):
                    setattr(self, key, json.dumps(value))
                else:
                    setattr(self, key, value)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        """Delete lesson progress from database."""
        db.session.delete(self)
        db.session.commit()
    
    def mark_complete(self, answer_data: Optional[Dict] = None) -> 'LessonProgress':
        """Mark lesson as completed.
        
        Args:
            answer_data: Dictionary of quiz answers (optional)
            
        Returns:
            Updated LessonProgress instance
        """
        self.completed = True
        self.completed_at = datetime.utcnow()
        if answer_data:
            self.answer_data = json.dumps(answer_data)
        db.session.commit()
        return self
    
    def add_time(self, seconds: int) -> 'LessonProgress':
        """Add time spent on lesson.
        
        Args:
            seconds: Number of seconds to add
            
        Returns:
            Updated LessonProgress instance
        """
        self.time_spent += seconds
        db.session.commit()
        return self
    
    def get_answer_data_dict(self) -> Optional[Dict]:
        """Parse and return answer_data as dictionary.
        
        Returns:
            Dictionary of answer data or None
        """
        if self.answer_data:
            try:
                return json.loads(self.answer_data)
            except json.JSONDecodeError:
                return None
        return None
    
    def set_answer_data(self, data: Dict) -> None:
        """Set answer_data from dictionary.
        
        Args:
            data: Dictionary to store as JSON
        """
        self.answer_data = json.dumps(data)
        db.session.commit()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lesson progress to dictionary.
        
        Returns:
            Dictionary representation of lesson progress
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'lesson_id': self.lesson_id,
            'completed': self.completed,
            'time_spent': self.time_spent,
            'answer_data': self.get_answer_data_dict(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of LessonProgress."""
        status = 'Completed' if self.completed else 'In Progress'
        return f'<LessonProgress user={self.user_id} lesson={self.lesson_id} ({status})>'
