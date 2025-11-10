"""Database initialization and base model setup.

This module initializes the SQLAlchemy database instance and provides
the base model class for all database models.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """Initialize the database with the Flask application.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        db.create_all()


# Import all models for easy access
from src.models.user import User
from src.models.session import Session
from src.models.team import Team
from src.models.team_member import TeamMember
from src.models.course import Course
from src.models.course_prerequisite import CoursePrerequisite
from src.models.lesson import Lesson
from src.models.enrollment import Enrollment
from src.models.lesson_progress import LessonProgress
from src.models.certificate import Certificate
from src.models.announcement import Announcement
from src.models.message import Message
from src.models.activity_log import ActivityLog

__all__ = [
    'db',
    'init_db',
    'User',
    'Session',
    'Team',
    'TeamMember',
    'Course',
    'CoursePrerequisite',
    'Lesson',
    'Enrollment',
    'LessonProgress',
    'Certificate',
    'Announcement',
    'Message',
    'ActivityLog',
]
