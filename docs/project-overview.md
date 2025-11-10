# Grace University LMS - Project Overview

## Project Description

Grace University is a Learning Management System (LMS) developed for Grace City Church to facilitate training and management of their volunteer program, specifically focusing on "Doorholders" (the church's term for volunteers).

## Purpose

The primary purpose of this application is to:
- Provide structured training materials for church volunteers
- Track volunteer progress and certifications
- Manage volunteer teams and assignments
- Enable team leads and administrators to oversee volunteer development
- Create a centralized hub for all volunteer-related learning and communication

## Target Users

### Primary Audience
**Doorholders** - Church volunteers who need to complete training modules and access learning materials

### Administrative Users
- **Superusers** - Highest level of system access, full administrative control
- **Admins** - Administrative privileges for managing users, content, and system settings
- **Team Leads** - Manage specific teams of doorholders, track their progress, and provide support

## Role Hierarchy & Permissions

### Superuser
- Full system access and control
- Can manage all users across all roles
- System configuration and settings
- Access to all features and data
- Can create/edit/delete admins

### Admin
- Manage users (team leads and doorholders)
- Create and manage training content/courses
- View system-wide reports and analytics
- Manage team assignments
- Cannot modify superuser accounts or critical system settings

### Team Lead
- Manage assigned doorholder teams
- Track team member progress
- Assign courses to team members
- View team-specific reports
- Communication with team members

### Doorholder (Base Volunteer Role)
- Access assigned training modules/courses
- Complete coursework and assessments
- View personal progress and certifications
- Access team communications
- Update personal profile

## Technical Architecture

### Framework & Structure
- **Backend:** Flask (Python)
- **Architecture Pattern:** MVC with thin controllers, thick services
- **Frontend:** Jinja2 templates with Bootstrap + custom CSS
- **File Organization:** Page-based template structure with component reusability

### Project Structure
```
Grace University/
├── run.py                          # Application entry point
├── docs/                           # Project documentation
├── src/
│   ├── controllers/                # Route handlers (thin)
│   │   └── routes.py
│   ├── models/                     # Database models (CRUD only)
│   ├── services/                   # Business logic (thick)
│   ├── utils/                      # Helper functions and utilities
│   ├── static/
│   │   ├── css/                    # Stylesheets
│   │   ├── js/                     # JavaScript files
│   │   └── img/                    # Images and assets
│   └── templates/
│       ├── bases/                  # Base templates
│       │   ├── public.html         # Base for pre-login pages
│       │   └── private.html        # Base for post-login pages
│       ├── public/                 # Public-facing pages
│       │   ├── landing/
│       │   ├── about/
│       │   ├── contact/
│       │   └── auth/
│       │       ├── login/
│       │       └── register/
│       └── private/                # Role-specific dashboards
│           ├── superuser/
│           │   └── dashboard/
│           ├── admin/
│           │   └── dashboard/
│           ├── teamLead/
│           │   └── dashboard/
│           └── doorholder/
│               └── dashboard/
```

## Core Features (Planned)

### User Management
- User authentication and authorization
- Role-based access control (RBAC)
- User profile management
- Team assignments and hierarchy

### Learning Management
- Course/training module creation and management
- Content delivery (videos, documents, interactive lessons)
- Progress tracking
- Assessment and quizzes
- Certification upon completion

### Team Management
- Team creation and member assignment
- Team-specific course assignments
- Team communication tools
- Team progress monitoring

### Reporting & Analytics
- Individual progress reports
- Team performance analytics
- Course completion statistics
- Custom report generation

### Communication
- Announcements system
- Team messaging
- Notification system
- Email integration

## Development Principles

### Code Quality
- Follow Python's Zen principles (simple, explicit, readable)
- Comprehensive documentation with Google-style docstrings
- Type hints for all functions
- Maximum function length: 20-25 lines
- Single Responsibility Principle

### Architecture Pattern
**Thin Controllers, Thick Services:**
- **Controllers:** Handle routing and template rendering only
- **Services:** Contain all business logic and orchestration
- **Models:** Database interaction only (CRUD operations)

### Styling Approach
- Bootstrap as the foundation
- Custom CSS for branding and enhancements
- NO inline styles (use CSS classes only)
- CSS variables for consistency

### Template Structure
- All pages extend base templates (`public.html` or `private.html`)
- Component-based approach for reusability
- Clear separation between public and private pages
- Role-based template organization

## Technology Stack (Proposed)

### Backend
- **Framework:** Flask
- **Database:** TBD (PostgreSQL recommended for production)
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5.3
- **JavaScript:** Vanilla JS + potential for Alpine.js or HTMX
- **Icons:** Bootstrap Icons or Font Awesome

### Development Tools
- **Version Control:** Git
- **Environment Management:** Python venv
- **Code Formatting:** Black (88 char limit)
- **Linting:** Pylint/Flake8

## Implementation Phases

### Phase 1: Foundation (Current)
- [ ] Database schema design
- [ ] User model and authentication system
- [ ] Role-based access control
- [ ] Basic dashboard layouts for each role

### Phase 2: Core LMS Features
- [ ] Course/module management
- [ ] Content delivery system
- [ ] Progress tracking
- [ ] Assessment system

### Phase 3: Team Management
- [ ] Team creation and management
- [ ] Team assignments
- [ ] Team-specific features
- [ ] Communication tools

### Phase 4: Reporting & Analytics
- [ ] Progress reports
- [ ] Analytics dashboard
- [ ] Export functionality
- [ ] Custom report builder

### Phase 5: Enhancement & Polish
- [ ] Email notifications
- [ ] Mobile responsiveness optimization
- [ ] Performance optimization
- [ ] User feedback implementation

## Success Metrics

- Number of active doorholders using the platform
- Course completion rates
- User engagement metrics
- Team lead satisfaction with management tools
- Reduction in manual training coordination time

## Future Considerations

- Mobile app development
- Integration with church management software
- Advanced gamification features
- Multi-language support
- API for third-party integrations

---

**Document Version:** 1.0  
**Last Updated:** November 9, 2025  
**Project Status:** Initial Planning & Setup Phase
