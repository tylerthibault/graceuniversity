# Grace University LMS - User Stories & Application Flow

## Overview
This document outlines user stories for each role in the Grace University LMS, describing the journey from login to key tasks and workflows.

---

## Superuser Role (Pastors/Church Leadership)

### Role Context
**Who:** Senior church leadership (pastors, executive staff)  
**Responsibility:** Oversee entire volunteer training system, manage all users, configure system settings  
**Access Level:** Full system access - can perform any action in the application

### Core Capabilities
- Manage all user accounts (create, edit, delete across all roles)
- Oversee system-wide training and volunteer performance
- Configure system settings and permissions
- Access comprehensive analytics and reporting
- Manage admin accounts
- Emergency intervention and problem resolution

---

## Superuser User Stories

### Authentication & Initial Access

#### US-SU-001: First-Time Login
**As a** superuser (pastor),  
**I want to** log in with my credentials,  
**So that** I can access the volunteer management system.

**Acceptance Criteria:**
- Navigate to `/auth/login`
- Enter email and password
- System verifies credentials and role
- Redirected to superuser dashboard (`/private/superuser/dashboard`)
- Navigation bar displays superuser-specific menu items

**Flow:**
```
1. Landing page → Click "Login" → Login form
2. Enter credentials → Submit
3. Backend validates (controller → service → model)
4. Session created → Redirect to dashboard
5. Dashboard loads with superuser privileges
```

---

#### US-SU-002: Dashboard Overview
**As a** superuser,  
**I want to** see a comprehensive overview of the entire system,  
**So that** I can quickly assess the health and status of the volunteer program.

**Dashboard Components:**
1. **Key Metrics Cards**
   - Total active volunteers (doorholders)
   - Total teams
   - Active courses
   - Recent completions (last 7 days)
   - Volunteers needing attention (overdue training)

2. **Quick Actions**
   - Create new admin account
   - Add new course
   - Send system-wide announcement
   - View all users
   - Access system settings

3. **Recent Activity Feed**
   - New enrollments
   - Course completions
   - New user registrations
   - Team lead actions

4. **Alerts/Notifications**
   - Users with expired certifications
   - Courses pending approval
   - System issues or errors

**Technical Implementation:**
- Service layer aggregates data from multiple models
- Real-time or cached statistics
- Role-based component visibility

---

### User Management

#### US-SU-003: View All Users
**As a** superuser,  
**I want to** view a list of all users across all roles,  
**So that** I can monitor and manage the user base.

**Features:**
- Paginated table of all users
- Filter by role (admin, team_lead, doorholder)
- Filter by status (active, inactive)
- Search by name, email, or team
- Sort by: name, email, role, join date, last login
- Click user row to view detailed profile

**Table Columns:**
- Name
- Email
- Role
- Team(s)
- Status (active/inactive)
- Last Login
- Actions (view, edit, deactivate)

**Flow:**
```
Dashboard → "Manage Users" → All Users List
→ Filter/Search/Sort
→ Click user → User Detail Page
```

---

#### US-SU-004: Create Admin Account
**As a** superuser,  
**I want to** create new admin accounts,  
**So that** I can delegate administrative responsibilities.

**Acceptance Criteria:**
- Button: "Create Admin User"
- Form fields:
  - Name (required)
  - Email (required, unique validation)
  - Phone (optional)
  - Temporary password (auto-generated or custom)
  - Send welcome email (checkbox)
- Validation:
  - Email format check
  - Email uniqueness check
  - Strong password requirements
- Success: Admin created, optional email sent, redirect to admin's profile
- Error handling: Display clear error messages

**Flow:**
```
Dashboard → "Create Admin" → Admin Creation Form
→ Fill form → Submit
→ Service validates and creates user (role: 'admin')
→ Optional: Send welcome email with credentials
→ Success message → Redirect to new admin's profile
```

---

#### US-SU-005: Edit Any User Account
**As a** superuser,  
**I want to** edit any user's profile information,  
**So that** I can keep user data accurate and manage permissions.

**Editable Fields:**
- Name
- Email
- Phone
- Role (dropdown: superuser, admin, team_lead, doorholder)
- Status (active/inactive toggle)
- Team assignments (for team_lead and doorholder roles)

**Restrictions:**
- Cannot edit own role or status (prevent self-lockout)
- Warning when changing user roles
- Confirmation modal for role changes

**Flow:**
```
User List → Click user → User Profile Page
→ "Edit Profile" button → Edit Form
→ Modify fields → Submit
→ Service validates changes
→ Update database → Success message
→ Updated profile displayed
```

---

#### US-SU-006: Deactivate/Reactivate User Account
**As a** superuser,  
**I want to** deactivate or reactivate user accounts,  
**So that** I can manage access without deleting accounts.

**Acceptance Criteria:**
- Toggle button on user profile: "Deactivate" / "Activate"
- Confirmation modal: "Are you sure you want to deactivate [Name]?"
- Deactivation effects:
  - User cannot log in
  - User status marked as inactive
  - User retains all historical data
  - User's sessions invalidated
- Reactivation restores full access
- Cannot deactivate own account

**Flow:**
```
User Profile → "Deactivate User" button
→ Confirmation modal → Confirm
→ Service updates user.is_active = False
→ Clear user sessions
→ Success message → Profile shows "Inactive" status
```

---

#### US-SU-007: Delete User Account (Permanent)
**As a** superuser,  
**I want to** permanently delete user accounts,  
**So that** I can remove users who should no longer exist in the system.

**Acceptance Criteria:**
- "Delete Account" button (red, danger styling)
- Strong confirmation modal:
  - "This action CANNOT be undone"
  - Type user's email to confirm
- Deletion cascades or handles:
  - Team memberships removed
  - Enrollments archived or deleted
  - Activity logs retained for audit
  - Certificates archived
- Cannot delete own account
- Redirect to user list after deletion

**Flow:**
```
User Profile → "Delete Account" (danger zone)
→ Confirmation modal with email verification
→ Type email to confirm → "Delete Forever"
→ Service handles cascading deletion
→ Success message → Redirect to user list
```

---

### System Management

#### US-SU-008: View System Settings
**As a** superuser,  
**I want to** access and modify system-wide settings,  
**So that** I can configure the application to meet our church's needs.

**Settings Categories:**

1. **General Settings**
   - Church name
   - Contact email
   - Support email
   - Application timezone
   - Default language

2. **User Settings**
   - Allow self-registration (on/off)
   - Email verification required
   - Password requirements
   - Session timeout duration

3. **Course Settings**
   - Default completion method
   - Certificate templates
   - Passing score threshold
   - Expiration defaults

4. **Notification Settings**
   - Email notifications enabled
   - Reminder frequency for deadlines
   - Announcement templates

**Flow:**
```
Dashboard → "System Settings" → Settings Page
→ Navigate tabs/sections
→ Edit settings → Save
→ Service validates → Update config
→ Success message
```

---

#### US-SU-009: Access System-Wide Reports
**As a** superuser,  
**I want to** generate and view comprehensive reports,  
**So that** I can make informed decisions about the volunteer program.

**Report Types:**

1. **Volunteer Overview Report**
   - Total volunteers
   - Active vs inactive
   - Breakdown by team
   - Certification status
   - Date range filter

2. **Training Progress Report**
   - Courses in progress
   - Completion rates
   - Average completion time
   - Overdue enrollments
   - Filter by course/team

3. **Team Performance Report**
   - Team-by-team breakdown
   - Team lead effectiveness
   - Team completion rates
   - Comparison metrics

4. **Certification Report**
   - Valid certifications
   - Expiring soon (30/60/90 days)
   - Expired certifications
   - Recertification needed

**Features:**
- Export to PDF/Excel
- Date range filters
- Team/course filters
- Visual charts and graphs
- Print-friendly format

**Flow:**
```
Dashboard → "Reports" → Reports Page
→ Select report type
→ Configure filters/parameters
→ "Generate Report"
→ Service queries data and formats
→ Display report → Option to export
```

---

#### US-SU-010: Send System-Wide Announcement
**As a** superuser,  
**I want to** send announcements to all users or specific roles/teams,  
**So that** I can communicate important information.

**Features:**
- Rich text editor for message
- Subject line
- Recipient selection:
  - All users
  - Specific role (admins, team leads, doorholders)
  - Specific team(s)
  - Custom user selection
- Send immediately or schedule for later
- Email notification option
- In-app notification display

**Flow:**
```
Dashboard → "Send Announcement" → Announcement Form
→ Compose message
→ Select recipients
→ Choose delivery method (in-app, email, both)
→ Preview → Send/Schedule
→ Service creates announcement records
→ Notifications sent → Success message
```

---

### Course Oversight

#### US-SU-011: View All Courses
**As a** superuser,  
**I want to** view all courses in the system,  
**So that** I can oversee the training curriculum.

**Features:**
- List all courses (campus-wide and team-specific)
- Filter by:
  - Active/inactive
  - Campus-wide vs team-specific
  - Created by (admin)
  - Completion method
- Search by title
- Sort by: title, creation date, enrollments, completion rate
- Click course to view details

**Display:**
- Course title
- Description
- Type (campus-wide/team-specific)
- Status (active/inactive)
- Total enrollments
- Completion rate
- Created by
- Actions (view, edit, deactivate)

---

#### US-SU-012: Edit Any Course
**As a** superuser,  
**I want to** edit any course in the system,  
**So that** I can correct errors or update content.

**Editable Elements:**
- Course metadata (title, description)
- Completion method
- Passing score
- Certificate settings
- Campus-wide flag
- Active status
- Lessons (add, edit, delete, reorder)

**Flow:**
```
All Courses → Click course → Course Details
→ "Edit Course" → Edit Form
→ Modify fields/lessons → Save
→ Service validates and updates
→ Success message → Updated course displayed
```

---

#### US-SU-013: Monitor Course Performance
**As a** superuser,  
**I want to** see detailed analytics for each course,  
**So that** I can identify successful training and areas for improvement.

**Course Analytics:**
- Total enrollments
- In progress / Completed / Not started breakdown
- Average completion time
- Pass/fail rates (if assessment-based)
- Feedback/ratings (if implemented)
- Dropout points (which lessons students abandon)
- Completion trend over time (chart)

**Flow:**
```
Course Details → "Analytics" tab
→ View metrics and charts
→ Filter by date range or team
→ Export data if needed
```

---

### Team Oversight

#### US-SU-014: View All Teams
**As a** superuser,  
**I want to** view all volunteer teams,  
**So that** I can monitor team organization and performance.

**Features:**
- List all teams
- Filter by ministry area (parking, greeting, ushers, kids, etc.)
- Filter by status (active/inactive)
- Search by team name
- Display:
  - Team name
  - Ministry area
  - Team lead(s)
  - Number of members
  - Active status
  - Actions (view, edit, manage members)

---

#### US-SU-015: Create/Edit Teams
**As a** superuser,  
**I want to** create new teams or edit existing ones,  
**So that** I can organize volunteers effectively.

**Team Form:**
- Team name (required)
- Ministry area (required, dropdown)
- Description
- Team lead assignment (select user with team_lead role)
- Active status toggle

**Flow:**
```
Teams List → "Create Team" → Team Form
→ Fill details → Assign team lead
→ Submit → Service creates team
→ Success message → Team details page
```

---

#### US-SU-016: Assign/Remove Team Members
**As a** superuser,  
**I want to** add or remove volunteers from teams,  
**So that** team composition stays accurate.

**Features:**
- Team detail page shows current members
- "Add Member" button → Search users
- Select user(s) to add
- Remove member button next to each member
- Confirmation for removal
- Designate/undesignate team leads

**Flow:**
```
Team Details → Current Members List
→ "Add Member" → User search modal
→ Select user → Confirm → Member added
OR
→ "Remove" next to member → Confirm → Member removed
```

---

### Emergency & Administrative Functions

#### US-SU-017: Impersonate User (View As)
**As a** superuser,  
**I want to** view the application as another user,  
**So that** I can troubleshoot issues they report.

**Features:**
- "View As User" button on user profiles
- Switch to that user's view/dashboard
- Banner at top: "Viewing as [Name] - Click to return to superuser"
- All permissions match the impersonated user
- Action logged for security/audit
- Cannot perform destructive actions while impersonating

**Flow:**
```
User Profile → "View As User"
→ Confirm action → Switch to user's view
→ Experience app as that user
→ "Exit Impersonation" → Return to superuser dashboard
```

---

#### US-SU-018: View Activity Logs
**As a** superuser,  
**I want to** view system activity logs,  
**So that** I can audit actions and troubleshoot issues.

**Log Information:**
- Timestamp
- User who performed action
- Action type (login, course_complete, enrollment, user_edit, etc.)
- Target (what was affected)
- IP address
- Success/failure status

**Features:**
- Filter by:
  - Date range
  - User
  - Action type
  - Success/failure
- Search logs
- Export logs
- Detailed view for each log entry

**Flow:**
```
Dashboard → "Activity Logs" → Logs Page
→ Apply filters → View logs
→ Click log entry → Detailed view
→ Export if needed
```

---

#### US-SU-019: Manual Certificate Override
**As a** superuser,  
**I want to** manually award or revoke certificates,  
**So that** I can handle special cases or correct errors.

**Use Cases:**
- Award certificate for in-person training
- Revoke certificate due to policy violation
- Extend expiration date
- Mark course complete without assessment

**Features:**
- Access from user profile or enrollment details
- Select course/certificate
- Action: Award / Revoke / Extend
- Reason field (required for audit)
- Confirmation modal
- Action logged

**Flow:**
```
User Profile → Enrollments tab
→ Select enrollment → "Override Certificate"
→ Choose action (award/revoke/extend)
→ Enter reason → Confirm
→ Service updates enrollment/certificate
→ User notified → Action logged
```

---

#### US-SU-020: Bulk User Import
**As a** superuser,  
**I want to** import multiple users from a CSV file,  
**So that** I can onboard volunteers efficiently.

**Features:**
- CSV template download
- CSV upload form
- Preview imported data before commit
- Validation:
  - Required fields present
  - Email format and uniqueness
  - Valid role values
  - Valid team references
- Error report for invalid rows
- Option to skip errors or fix and re-upload
- Success summary after import

**CSV Format:**
```
name,email,phone,role,team_name,send_welcome_email
John Doe,john@example.com,123-456-7890,doorholder,Parking Team,yes
Jane Smith,jane@example.com,098-765-4321,team_lead,Greeting Team,yes
```

**Flow:**
```
Dashboard → "Import Users" → Upload CSV
→ System validates → Preview table
→ Confirm import → Service creates users
→ Summary: X created, Y errors → Download error report
```

---

## Summary of Superuser Journey

### Typical Workflow:
1. **Login** → Redirected to superuser dashboard
2. **Review dashboard** → Check key metrics, alerts, recent activity
3. **Manage users** → Create admins, edit profiles, handle issues
4. **Oversee courses** → Review curriculum, monitor completion rates
5. **Monitor teams** → Ensure proper organization and leadership
6. **Generate reports** → Assess program effectiveness
7. **Send announcements** → Communicate with volunteers
8. **Handle exceptions** → Manual overrides, troubleshooting
9. **Audit activity** → Review logs for security and compliance

### Key Pages:
- `/private/superuser/dashboard` - Main dashboard
- `/private/superuser/users` - All users management
- `/private/superuser/courses` - Course oversight
- `/private/superuser/teams` - Team management
- `/private/superuser/reports` - System reports
- `/private/superuser/settings` - System configuration
- `/private/superuser/logs` - Activity logs
- `/private/superuser/announcements` - Communication center

---

## Navigation Structure for Superuser

```
Top Navigation Bar:
├── Dashboard (home icon)
├── Users
│   ├── All Users
│   ├── Create Admin
│   ├── Import Users
│   └── Inactive Users
├── Courses
│   ├── All Courses
│   ├── Create Course
│   └── Course Analytics
├── Teams
│   ├── All Teams
│   ├── Create Team
│   └── Team Performance
├── Reports
│   ├── Volunteer Overview
│   ├── Training Progress
│   ├── Team Performance
│   └── Certifications
├── Announcements
│   ├── Send Announcement
│   └── Past Announcements
├── System
│   ├── Settings
│   ├── Activity Logs
│   └── System Health
└── Profile (dropdown)
    ├── My Profile
    ├── Change Password
    └── Logout
```

---

*Next sections: Admin, Team Lead, and Doorholder user stories will follow similar detailed structure.*
