"""Seed file for populating database with roles and users.

This script creates roles and sample users for each role in the system:
- Superuser: Full system access
- Admin: Administrative access
- Team Lead: Team management access
- Doorholder: Basic user access
"""

import sys
import os
from werkzeug.security import generate_password_hash

# Add parent directory to path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import create_app
from src.models import db
from src.models.user import User
from src.models.role import Role


def clear_all():
    """Delete all existing users and roles from the database.
    
    WARNING: This will remove all user and role data!
    """
    print("Clearing existing users and roles...")
    User.query.delete()
    Role.query.delete()
    db.session.commit()
    print("All users and roles cleared.")


def seed_roles():
    """Create the four system roles.
    
    Returns:
        Dictionary mapping role names to Role instances
    """
    print("\nCreating roles...")
    
    roles_data = [
        {
            'name': 'superuser',
            'display_name': 'Superuser',
            'description': 'Full system access with all administrative privileges'
        },
        {
            'name': 'admin',
            'display_name': 'Administrator',
            'description': 'Administrative access to manage courses, users, and content'
        },
        {
            'name': 'team_lead',
            'display_name': 'Team Lead',
            'description': 'Team management and oversight capabilities'
        },
        {
            'name': 'doorholder',
            'display_name': 'Doorholder',
            'description': 'Basic user access to courses and learning materials'
        },
    ]
    
    roles = {}
    for role_data in roles_data:
        existing_role = Role.get_by_name(role_data['name'])
        if existing_role:
            print(f"  ⚠ Role '{role_data['display_name']}' already exists")
            roles[role_data['name']] = existing_role
        else:
            role = Role.create(
                name=role_data['name'],
                display_name=role_data['display_name'],
                description=role_data['description']
            )
            roles[role_data['name']] = role
            print(f"  ✓ Created role: {role_data['display_name']}")
    
    return roles


def seed_users():
    """Seed the database with sample users for each role.
    
    Creates 2 users for each role (superuser, admin, team_lead, doorholder)
    with predefined credentials for testing and development.
    """
    print("\nStarting user seeding process...")
    
    # Common password for all test users (in production, use strong unique passwords)
    password = "Password123!"
    password_hash = generate_password_hash(password)
    
    # Define users with their roles
    users_data = [
        # Superusers
        {
            'email': 'sarah.johnson@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Sarah Johnson',
            'role_names': ['superuser'],
            'phone': '555-0101'
        },
        {
            'email': 'michael.chen@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Michael Chen',
            'role_names': ['superuser'],
            'phone': '555-0102'
        },
        
        # Admins
        {
            'email': 'emily.rodriguez@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Emily Rodriguez',
            'role_names': ['admin'],
            'phone': '555-0201'
        },
        {
            'email': 'james.wilson@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'James Wilson',
            'role_names': ['admin'],
            'phone': '555-0202'
        },
        
        # Team Leads
        {
            'email': 'jessica.martinez@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Jessica Martinez',
            'role_names': ['team_lead'],
            'phone': '555-0301'
        },
        {
            'email': 'david.thompson@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'David Thompson',
            'role_names': ['team_lead'],
            'phone': '555-0302'
        },
        
        # Doorholders
        {
            'email': 'ashley.anderson@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Ashley Anderson',
            'role_names': ['doorholder'],
            'phone': '555-0401'
        },
        {
            'email': 'robert.garcia@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Robert Garcia',
            'role_names': ['doorholder'],
            'phone': '555-0402'
        },
        
        # Multi-role user example: Admin + Team Lead
        {
            'email': 'jennifer.lee@graceuniversity.com',
            'password_hash': password_hash,
            'name': 'Jennifer Lee',
            'role_names': ['admin', 'team_lead'],
            'phone': '555-0501'
        },
    ]
    
    # Create users
    created_count = 0
    for user_data in users_data:
        try:
            # Check if user already exists
            existing_user = User.get_by_email(user_data['email'])
            if existing_user:
                print(f"  ⚠ User {user_data['email']} already exists, skipping...")
                continue
            
            # Get role instances from database
            user_roles = []
            for role_name in user_data['role_names']:
                role = Role.get_by_name(role_name)
                if not role:
                    print(f"  ✗ Error: Role '{role_name}' not found. Please run seed_roles first.")
                    continue
                user_roles.append(role)
            
            # Create new user
            user = User.create(
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                name=user_data['name'],
                roles=user_roles,
                phone=user_data['phone']
            )
            created_count += 1
            roles_display = ', '.join(user_data['role_names'])
            print(f"  ✓ Created user: {user_data['name']} ({user_data['email']}) - Roles: {roles_display}")
            
        except Exception as e:
            print(f"  ✗ Error creating user {user_data['email']}: {str(e)}")
            db.session.rollback()
    
    print(f"\n{'='*60}")
    print(f"Seeding complete! Created {created_count} users.")
    print(f"{'='*60}")
    print("\nTest Credentials (all users have the same password):")
    print(f"Password: {password}")
    print("\nRole breakdown:")
    print("  - Superusers: 2")
    print("  - Admins: 2")
    print("  - Team Leads: 2")
    print("  - Doorholders: 2")
    print("  - Multi-role users: 1 (Admin + Team Lead)")
    print(f"\nTotal: {len(users_data)} users")
    print("\nExample logins:")
    print("  Superuser:")
    print("    Email: sarah.johnson@graceuniversity.com")
    print(f"    Password: {password}")
    print("  Admin:")
    print("    Email: emily.rodriguez@graceuniversity.com")
    print(f"    Password: {password}")
    print("  Team Lead:")
    print("    Email: jessica.martinez@graceuniversity.com")
    print(f"    Password: {password}")
    print("  Doorholder:")
    print("    Email: ashley.anderson@graceuniversity.com")
    print(f"    Password: {password}")
    print("  Multi-role:")
    print("    Email: jennifer.lee@graceuniversity.com")
    print(f"    Password: {password}")


def main():
    """Main entry point for seeding script.
    
    Creates app context and runs seeding process.
    Optionally clears existing users and roles with --clear flag.
    """
    app = create_app()
    
    with app.app_context():
        # Check for --clear flag
        if '--clear' in sys.argv:
            response = input("⚠ WARNING: This will delete ALL users and roles! Continue? (yes/no): ")
            if response.lower() == 'yes':
                clear_all()
            else:
                print("Aborted.")
                return
        
        # Seed roles first
        seed_roles()
        
        # Then seed users
        seed_users()


if __name__ == '__main__':
    main()
