"""Dashboard service for retrieving system statistics and data.

This module contains business logic for dashboard operations including
system stats, user analytics, and administrative overview data.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import func
from src.models.user import User
from src.models.role import Role
from src.models.course import Course
from src.models.enrollment import Enrollment
from src.models import db


def get_superuser_dashboard_data() -> Dict[str, Any]:
    """Retrieve comprehensive dashboard data for superuser.
    
    Returns:
        Dictionary containing system statistics, recent users, and analytics
    """
    return {
        'stats': _get_system_stats(),
        'recent_users': _get_recent_users(limit=10),
        'user_growth': _get_user_growth_data(),
        'role_distribution': _get_role_distribution(),
        'activity_summary': _get_activity_summary()
    }


def get_admin_dashboard_data() -> Dict[str, Any]:
    """Retrieve dashboard data for admin users.
    
    Returns:
        Dictionary containing course stats, enrollments, and user overview
    """
    return {
        'stats': _get_admin_stats(),
        'recent_enrollments': _get_recent_enrollments(limit=10),
        'course_overview': _get_course_overview()
    }


def get_team_lead_dashboard_data(user_id: int) -> Dict[str, Any]:
    """Retrieve dashboard data for team lead.
    
    Args:
        user_id: Team lead's user ID
        
    Returns:
        Dictionary containing team stats and member overview
    """
    return {
        'stats': _get_team_stats(user_id),
        'team_members': _get_team_members(user_id)
    }


def get_doorholder_dashboard_data(user_id: int) -> Dict[str, Any]:
    """Retrieve dashboard data for doorholder (basic user).
    
    Args:
        user_id: User's ID
        
    Returns:
        Dictionary containing user's courses, progress, and certificates
    """
    return {
        'enrollments': _get_user_enrollments(user_id),
        'progress': _get_user_progress(user_id),
        'certificates': _get_user_certificates(user_id)
    }


# Private helper functions

def _get_system_stats() -> Dict[str, int]:
    """Get overall system statistics.
    
    Returns:
        Dictionary with counts for users, courses, enrollments, etc.
    """
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    # Users created in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': total_users - active_users,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'new_users_30d': new_users
    }


def _get_recent_users(limit: int = 10) -> List[Dict[str, Any]]:
    """Get most recently created users.
    
    Args:
        limit: Maximum number of users to return
        
    Returns:
        List of user dictionaries with basic info
    """
    users = User.query.order_by(User.created_at.desc()).limit(limit).all()
    
    return [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'roles': user.get_role_names(),
            'created_at': user.created_at,
            'is_active': user.is_active
        }
        for user in users
    ]


def _get_user_growth_data() -> Dict[str, int]:
    """Get user growth statistics over time.
    
    Returns:
        Dictionary with user counts for different time periods
    """
    now = datetime.utcnow()
    
    # Last 7 days
    seven_days_ago = now - timedelta(days=7)
    last_7_days = User.query.filter(User.created_at >= seven_days_ago).count()
    
    # Last 30 days
    thirty_days_ago = now - timedelta(days=30)
    last_30_days = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Last 90 days
    ninety_days_ago = now - timedelta(days=90)
    last_90_days = User.query.filter(User.created_at >= ninety_days_ago).count()
    
    return {
        'last_7_days': last_7_days,
        'last_30_days': last_30_days,
        'last_90_days': last_90_days
    }


def _get_role_distribution() -> List[Dict[str, Any]]:
    """Get distribution of users across roles.
    
    Returns:
        List of dictionaries with role names and user counts
    """
    roles = Role.query.all()
    
    distribution = []
    for role in roles:
        user_count = role.users.count()
        distribution.append({
            'role': role.display_name,
            'role_name': role.name,
            'count': user_count,
            'description': role.description
        })
    
    return distribution


def _get_activity_summary() -> Dict[str, Any]:
    """Get summary of recent activity.
    
    Returns:
        Dictionary with activity metrics
    """
    # Get users who logged in today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    active_today = User.query.filter(User.last_login >= today_start).count()
    
    # Get users who logged in this week
    week_start = datetime.utcnow() - timedelta(days=7)
    active_this_week = User.query.filter(User.last_login >= week_start).count()
    
    return {
        'active_today': active_today,
        'active_this_week': active_this_week
    }


def _get_admin_stats() -> Dict[str, int]:
    """Get statistics relevant to admin users.
    
    Returns:
        Dictionary with course and enrollment stats
    """
    return {
        'total_courses': Course.query.count(),
        'total_enrollments': Enrollment.query.count(),
        'total_users': User.query.count()
    }


def _get_recent_enrollments(limit: int = 10) -> List[Dict[str, Any]]:
    """Get most recent course enrollments.
    
    Args:
        limit: Maximum number of enrollments to return
        
    Returns:
        List of enrollment dictionaries
    """
    enrollments = Enrollment.query.order_by(
        Enrollment.enrolled_at.desc()
    ).limit(limit).all()
    
    return [
        {
            'id': enrollment.id,
            'user_name': enrollment.student.name,
            'course_title': enrollment.course.title,
            'enrolled_at': enrollment.enrolled_at,
            'status': enrollment.status
        }
        for enrollment in enrollments
    ]


def _get_course_overview() -> List[Dict[str, Any]]:
    """Get overview of all courses.
    
    Returns:
        List of course dictionaries with enrollment counts
    """
    courses = Course.query.all()
    
    return [
        {
            'id': course.id,
            'title': course.title,
            'enrollment_count': course.enrollments.count(),
            'is_active': course.is_active
        }
        for course in courses
    ]


def _get_team_stats(user_id: int) -> Dict[str, int]:
    """Get statistics for team lead's team.
    
    Args:
        user_id: Team lead's user ID
        
    Returns:
        Dictionary with team statistics
    """
    # Placeholder - implement based on Team model structure
    return {
        'team_members': 0,
        'active_members': 0
    }


def _get_team_members(user_id: int) -> List[Dict[str, Any]]:
    """Get team members for a team lead.
    
    Args:
        user_id: Team lead's user ID
        
    Returns:
        List of team member dictionaries
    """
    # Placeholder - implement based on Team model structure
    return []


def _get_user_enrollments(user_id: int) -> List[Dict[str, Any]]:
    """Get user's course enrollments.
    
    Args:
        user_id: User's ID
        
    Returns:
        List of enrollment dictionaries
    """
    user = User.get_by_id(user_id)
    if not user:
        return []
    
    enrollments = user.enrollments.all()
    
    return [
        {
            'id': enrollment.id,
            'course_title': enrollment.course.title,
            'status': enrollment.status,
            'enrolled_at': enrollment.enrolled_at,
            'progress': enrollment.progress
        }
        for enrollment in enrollments
    ]


def _get_user_progress(user_id: int) -> Dict[str, Any]:
    """Get user's overall learning progress.
    
    Args:
        user_id: User's ID
        
    Returns:
        Dictionary with progress metrics
    """
    user = User.get_by_id(user_id)
    if not user:
        return {'total_courses': 0, 'completed': 0, 'in_progress': 0}
    
    enrollments = user.enrollments.all()
    completed = sum(1 for e in enrollments if e.status == 'completed')
    in_progress = sum(1 for e in enrollments if e.status == 'in_progress')
    
    return {
        'total_courses': len(enrollments),
        'completed': completed,
        'in_progress': in_progress
    }


def _get_user_certificates(user_id: int) -> List[Dict[str, Any]]:
    """Get user's earned certificates.
    
    Args:
        user_id: User's ID
        
    Returns:
        List of certificate dictionaries
    """
    user = User.get_by_id(user_id)
    if not user:
        return []
    
    certificates = user.certificates.all()
    
    return [
        {
            'id': cert.id,
            'course_title': cert.course.title,
            'issued_at': cert.issued_at,
            'certificate_url': cert.certificate_url
        }
        for cert in certificates
    ]
