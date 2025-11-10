from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from typing import Dict, Any

"""Authentication controller for handling user login and registration.

This module provides routes for user authentication including login,
registration, and logout functionality.
"""

from src.services.auth_service import (
    authenticate_user,
    register_new_user,
    logout_user,
    get_all_users_for_testing,
    quick_login_by_id
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render the login page.
    
    Returns:
        str: Rendered HTML template for login page
    """
    # Get all users for testing purposes
    test_users = get_all_users_for_testing()
    return render_template('public/auth/login/index.html', test_users=test_users)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Process user login request.
    
    Returns:
        Response: Redirect to dashboard on success, login page on failure
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    try:
        user_data = authenticate_user(email, password)
        session['user_id'] = user_data['id']
        session['user_name'] = user_data['name']
        session['user_roles'] = user_data['roles']
        session['user_primary_role'] = user_data['primary_role']
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard.index'))
        
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('auth.login_page'))


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Render the registration page.
    
    Returns:
        str: Rendered HTML template for registration page
    """
    return render_template('public/auth/register/index.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Process user registration request.
    
    Returns:
        Response: Redirect to login on success, registration page on failure
    """
    user_data = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'name': request.form.get('name'),
        'confirm_password': request.form.get('confirm_password')
    }
    
    try:
        register_new_user(user_data)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login_page'))
        
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('auth.register_page'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Process user logout request.
    
    Returns:
        Response: Redirect to login page
    """
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/quick-login/<int:user_id>', methods=['POST'])
def quick_login(user_id: int):
    """Quick login as a user by ID (TESTING ONLY).
    
    WARNING: This endpoint bypasses authentication and should
    ONLY be used in development/testing environments.
    
    Args:
        user_id: User ID to log in as
        
    Returns:
        Response: Redirect to dashboard on success, login page on failure
    """
    try:
        user_data = quick_login_by_id(user_id)
        session['user_id'] = user_data['id']
        session['user_name'] = user_data['name']
        session['user_roles'] = user_data['roles']
        session['user_primary_role'] = user_data['primary_role']
        
        flash(f"Logged in as {user_data['name']} ({user_data['primary_role']})", 'success')
        return redirect(url_for('dashboard.index'))
        
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('auth.login_page'))