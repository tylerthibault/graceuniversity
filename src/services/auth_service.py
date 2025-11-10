"""Authentication service for user login, registration, and logout.

This module contains business logic for user authentication operations
including login validation, new user registration, and logout handling.
"""

from typing import Dict, Any, List
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User
from src.models.role import Role


def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticate user credentials and return user data.
    
    Validates email and password, checks if account is active,
    and updates last login timestamp on successful authentication.
    
    Args:
        email: User's email address
        password: Plain text password to verify
        
    Returns:
        Dictionary containing user data (id, email, name, roles, primary_role)
        
    Raises:
        ValueError: If email/password are missing, invalid, or account is inactive
    """
    if not email or not password:
        raise ValueError("Email and password are required")
    
    user = User.get_by_email(email)
    if not user:
        raise ValueError("Invalid email or password")
    
    if not check_password_hash(user.password_hash, password):
        raise ValueError("Invalid email or password")
    
    if not user.is_active:
        raise ValueError("Account is inactive. Please contact support.")
    
    user.update_last_login()
    
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'roles': user.get_role_names(),
        'primary_role': user.get_primary_role()
    }


def register_new_user(user_data: Dict[str, str]) -> Dict[str, Any]:
    """Register a new user account.
    
    Validates user input, checks for duplicate emails, hashes password,
    and creates new user with 'doorholder' role by default.
    
    Args:
        user_data: Dictionary containing:
            - email: User's email address
            - password: Plain text password
            - confirm_password: Password confirmation
            - name: User's full name
            - phone: User's phone number (optional)
            
    Returns:
        Dictionary containing created user data
        
    Raises:
        ValueError: If validation fails or email already exists
    """
    email = user_data.get('email', '').strip()
    password = user_data.get('password', '')
    confirm_password = user_data.get('confirm_password', '')
    name = user_data.get('name', '').strip()
    phone = user_data.get('phone', '').strip()
    
    # Validate required fields
    if not email or not password or not name:
        raise ValueError("Email, password, and name are required")
    
    # Validate email format
    if '@' not in email or '.' not in email:
        raise ValueError("Invalid email format")
    
    # Validate password match
    if password != confirm_password:
        raise ValueError("Passwords do not match")
    
    # Validate password strength
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    # Check if email already exists
    existing_user = User.get_by_email(email)
    if existing_user:
        raise ValueError("Email already registered")
    
    # Hash password
    password_hash = generate_password_hash(password)
    
    # Get doorholder role
    doorholder_role = Role.get_by_name('doorholder')
    if not doorholder_role:
        raise ValueError("Default role 'doorholder' not found. Please run seed script.")
    
    # Create new user with doorholder role by default
    user = User.create(
        email=email,
        password_hash=password_hash,
        name=name,
        roles=[doorholder_role],
        phone=phone if phone else None
    )
    
    return user.to_dict()


def logout_user() -> None:
    """Handle user logout.
    
    This function performs any necessary cleanup operations
    for user logout. Currently a placeholder for future logic
    such as invalidating tokens or logging logout events.
    
    Note:
        Session clearing is handled by the controller.
    """
    # Future: Add logout logging to activity_log
    # Future: Invalidate session tokens if using token-based auth
    pass


def get_all_users_for_testing() -> List[Dict[str, Any]]:
    """Retrieve all users with their role information for testing purposes.
    
    WARNING: This function is for TESTING/DEVELOPMENT ONLY.
    Should NOT be used in production environments.
    
    Returns:
        List of dictionaries containing user data with roles
    """
    users = User.get_all()

    print(f"[DEBUG] Retrieved {len(users)} users for testing purposes.")
    
    return [
        {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'roles': user.get_role_names(),
            'primary_role': user.get_primary_role()
        }
        for user in users
    ]


def quick_login_by_id(user_id: int) -> Dict[str, Any]:
    """Quick login a user by ID without password (TESTING ONLY).
    
    WARNING: This function bypasses authentication and is for
    TESTING/DEVELOPMENT ONLY. Must be disabled in production.
    
    Args:
        user_id: User's unique identifier
        
    Returns:
        Dictionary containing user data
        
    Raises:
        ValueError: If user not found or account inactive
    """
    user = User.get_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found")
    
    if not user.is_active:
        raise ValueError("Account is inactive")
    
    user.update_last_login()
    
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'roles': user.get_role_names(),
        'primary_role': user.get_primary_role()
    }
