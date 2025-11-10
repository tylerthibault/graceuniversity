# Database Seeding

This directory contains scripts for populating the database with sample data for development and testing.

## Available Seed Scripts

### `seed_users.py`
Seeds the database with roles and sample users.

**Roles Created:**
- **Superuser**: Full system access
- **Admin**: Administrative access  
- **Team Lead**: Team management access
- **Doorholder**: Basic user access

**Users Created:**
- 2 Superusers
- 2 Admins
- 2 Team Leads
- 2 Doorholders
- 1 Multi-role user (Admin + Team Lead)

**Total:** 4 roles and 9 test users

## Usage

### Running Seeds

**Standard seeding (adds roles and users if they don't exist):**
```bash
python seed/seed_users.py
```

**Clear all users and roles, then reseed:**
```bash
python seed/seed_users.py --clear
```

### Test Credentials

All seeded users share the same password for easy testing:

**Password:** `Password123!`

**Example Login Credentials:**
- Superuser: `sarah.johnson@graceuniversity.com` / `Password123!`
- Admin: `emily.rodriguez@graceuniversity.com` / `Password123!`
- Team Lead: `jessica.martinez@graceuniversity.com` / `Password123!`
- Doorholder: `ashley.anderson@graceuniversity.com` / `Password123!`
- Multi-role: `jennifer.lee@graceuniversity.com` / `Password123!`

### User List

| Role(s) | Email | Name | Phone |
|---------|-------|------|-------|
| Superuser | sarah.johnson@graceuniversity.com | Sarah Johnson | 555-0101 |
| Superuser | michael.chen@graceuniversity.com | Michael Chen | 555-0102 |
| Admin | emily.rodriguez@graceuniversity.com | Emily Rodriguez | 555-0201 |
| Admin | james.wilson@graceuniversity.com | James Wilson | 555-0202 |
| Team Lead | jessica.martinez@graceuniversity.com | Jessica Martinez | 555-0301 |
| Team Lead | david.thompson@graceuniversity.com | David Thompson | 555-0302 |
| Doorholder | ashley.anderson@graceuniversity.com | Ashley Anderson | 555-0401 |
| Doorholder | robert.garcia@graceuniversity.com | Robert Garcia | 555-0402 |
| Admin + Team Lead | jennifer.lee@graceuniversity.com | Jennifer Lee | 555-0501 |

## Multi-Role System

Users can now have multiple roles assigned simultaneously. The system supports:

- **Multiple Role Assignment**: Users can have any combination of roles
- **Primary Role**: The highest priority role determines dashboard routing
- **Role Priority**: superuser > admin > team_lead > doorholder
- **Role Checking**: Methods to check if user has specific role(s)

### Role Methods in User Model

```python
user.has_role('admin')  # Check single role
user.has_any_role(['admin', 'superuser'])  # Check if has any
user.has_all_roles(['admin', 'team_lead'])  # Check if has all
user.get_role_names()  # Get list of role names
user.get_primary_role()  # Get highest priority role
```

## Important Notes

⚠️ **Security Warning:** These credentials are for development/testing only!
- Never use these credentials in production
- Never commit production passwords to version control
- Change all default passwords before deploying
- Run seed script with `--clear` before deploying to reset data

## Adding More Seed Scripts

When creating additional seed scripts:

1. Follow the naming convention: `seed_<entity>.py`
2. Include proper error handling
3. Add rollback on failures
4. Provide clear console output
5. Check for existing data before creating duplicates
6. Document usage in this README
