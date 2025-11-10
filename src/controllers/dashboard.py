"""Dashboard controller for role-based dashboard routing.

This module handles routing to appropriate dashboards based on user roles.
Each role (superuser, admin, team_lead, doorholder) has a dedicated dashboard.
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from functools import wraps
from typing import Callable, Any

from src.services.dashboard_service import (
    get_superuser_dashboard_data,
    get_admin_dashboard_data,
    get_team_lead_dashboard_data,
    get_doorholder_dashboard_data
)

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def login_required(f: Callable) -> Callable:
    """Decorator to require user login.
    
    Args:
        f: Function to wrap
        
    Returns:
        Wrapped function that checks for authentication
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*required_roles: str) -> Callable:
    """Decorator to require specific user roles.
    
    Args:
        *required_roles: Role names required to access the route
        
    Returns:
        Decorator function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            if 'user_id' not in session:
                flash('Please log in to access this page', 'warning')
                return redirect(url_for('auth.login_page'))
            
            user_roles = session.get('user_roles', [])
            if not any(role in user_roles for role in required_roles):
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@dashboard_bp.route('/')
@login_required
def index():
    """Route to appropriate dashboard based on user's primary role.
    
    Returns:
        Redirect to role-specific dashboard
    """
    primary_role = session.get('user_primary_role')
    
    if primary_role == 'superuser':
        return redirect(url_for('dashboard.superuser'))
    elif primary_role == 'admin':
        return redirect(url_for('dashboard.admin'))
    elif primary_role == 'team_lead':
        return redirect(url_for('dashboard.team_lead'))
    elif primary_role == 'doorholder':
        return redirect(url_for('dashboard.doorholder'))
    else:
        flash('Invalid role configuration', 'danger')
        return redirect(url_for('auth.logout'))


@dashboard_bp.route('/superuser')
@role_required('superuser')
def superuser():
    """Render superuser dashboard.
    
    Returns:
        Rendered superuser dashboard template
    """
    try:
        data = get_superuser_dashboard_data()
        return render_template(
            'private/superuser/dashboard/index.html',
            data=data,
            user_name=session.get('user_name', 'User')
        )
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))


@dashboard_bp.route('/admin')
@role_required('admin', 'superuser')
def admin():
    """Render admin dashboard.
    
    Returns:
        Rendered admin dashboard template
    """
    try:
        data = get_admin_dashboard_data()
        return render_template(
            'private/admin/dashboard/index.html',
            data=data,
            user_name=session.get('user_name', 'User')
        )
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))


@dashboard_bp.route('/team-lead')
@role_required('team_lead', 'admin', 'superuser')
def team_lead():
    """Render team lead dashboard.
    
    Returns:
        Rendered team lead dashboard template
    """
    try:
        user_id = session.get('user_id')
        data = get_team_lead_dashboard_data(user_id)
        return render_template(
            'private/teamLead/dashboard/index.html',
            data=data,
            user_name=session.get('user_name', 'User')
        )
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))


@dashboard_bp.route('/doorholder')
@login_required
def doorholder():
    """Render doorholder (basic user) dashboard.
    
    Returns:
        Rendered doorholder dashboard template
    """
    try:
        user_id = session.get('user_id')
        data = get_doorholder_dashboard_data(user_id)
        return render_template(
            'private/doorholder/dashboard/index.html',
            data=data,
            user_name=session.get('user_name', 'User')
        )
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('main.index'))
