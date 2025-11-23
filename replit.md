# Catholic Church Volunteer Management System (CCVMS)

## Project Overview
A comprehensive Django-based volunteer management system for Catholic parishes, built with Python, Django, and TailwindCSS.

## Current Status
**Status**: MVP Complete with Enhanced Volunteer Management  
**Server**: Django development server running on port 5000  
**Database**: SQLite with all migrations applied  
**Workflow**: Configured and running successfully  
**Latest Update**: Added coordinator event management with task assignment and reporting (Nov 23, 2025)  

## Architecture

### Django Apps
1. **accounts** - Custom User model with role-based access (Administrator, Priest, Coordinator, Volunteer)
2. **volunteers** - Full CRUD for volunteer management with search
3. **ministries** - Ministry and program management
4. **events** - Event scheduling with volunteer assignments
5. **attendance** - Attendance tracking and performance monitoring
6. **communications** - Announcements and email notifications
7. **reports** - Analytics dashboard with statistics
8. **feedback** - Volunteer evaluations and event feedback

### Technology Stack
- **Backend**: Django 5.2.8, Python 3.11
- **Frontend**: HTML5, TailwindCSS (CDN), Vanilla JavaScript
- **Database**: SQLite (development)
- **Authentication**: Django built-in auth with custom User model

## Features Implemented

### Core Functionality
✅ Custom User model with 4 role types  
✅ **Volunteer Self-Registration** - Public signup form at `/accounts/signup/` with document upload  
✅ **Supporting Document Upload** - Volunteers can upload resume/ID during signup  
✅ **Pending Approval System** - New volunteer accounts require admin/coordinator approval before login  
✅ **Role-Based Navigation Menu** - Menu items displayed based on user role (Volunteer, Coordinator, Priest, Administrator)  
✅ **Volunteer Approval Management** - Approve/reject pending volunteers from list or detail view  
✅ **Role-Based Dashboards** - Separate dashboards for Admin, Priest, Coordinator, Volunteer  
✅ Full CRUD operations for volunteers, ministries, events  
✅ **Task Management** - Coordinators assign tasks to volunteers with due dates and status tracking
✅ **Event Reports** - Coordinators submit comprehensive event reports with attendance, performance notes, and recommendations
✅ **Coordinator Event Interface** - Dedicated management view for coordinators with volunteer/task/report tools
✅ Role-based access control with permission checks  
✅ Admin panel for all models with customized displays  
✅ Responsive TailwindCSS UI with dashboard  
✅ Login/logout functionality  
✅ Search and filtering capabilities  
✅ Database relationships (ManyToMany, ForeignKey)  

### Security & Access
✅ LoginRequiredMixin on all views  
✅ UserPassesTestMixin for role-based permissions  
✅ CSRF protection with Replit trusted origins  
✅ Session-based authentication  
✅ Automatic user+profile creation in transaction (signup)  
✅ Pending account activation - new volunteers cannot login until approved  
✅ Role-based menu visibility - users only see authorized sections  

## Known Limitations & Future Improvements

### Recent Additions

**Nov 23, 2025 - Coordinator Event Management**
✅ **Task Assignment System** - Coordinators can create, assign, and track tasks for volunteers within their events
✅ **Event Reporting** - Coordinators submit detailed event reports (draft/submitted) to priests for review
✅ **Volunteer Management** - Coordinators can add/remove volunteers from their ministry to events they coordinate
✅ **Coordinator Dashboard** - Shows all assigned events with task/volunteer/report counts and quick management access
✅ **Ministry-Based Access** - Coordinators can only manage volunteers and events from their assigned ministry
✅ **Secure Report Workflow** - Draft→Submitted status for coordinators, only priests can mark as reviewed

**Earlier Nov 23, 2025 - Ministry Assignment & Priest Event Control**
✅ **Ministry Assignment UI** - Administrators can assign users to ministries directly from user management page
✅ **Priest-Only Event Creation** - Only priests (not admins) can create events
✅ **Auto-Ministry Assignment** - Events automatically assigned to priest's ministry
✅ **Filtered Volunteer Selection** - Priests can only assign volunteers and coordinators from their ministry to events
✅ **Ministry-Based Access Control** - Priests can only edit/delete events for their assigned ministry

**Nov 20, 2025 - Enhanced Volunteer Management**
✅ **Supporting Document Upload** - Volunteers can upload documents (resume, ID) during signup  
✅ **Pending Approval System** - New volunteer accounts set to pending/inactive until approved by admin/coordinator  
✅ **Approval Workflow** - Approve/reject volunteers directly from volunteer list or detail view  
✅ **Document Review** - Admins/coordinators can view uploaded documents before approving  
✅ **Role-Based Menu** - Navigation dynamically adjusts based on user role:
   - **Volunteers**: Dashboard, Events, Feedback only
   - **Coordinators**: Dashboard, Volunteers, Ministries, Events, Attendance, Communications
   - **Priests**: Dashboard, Ministries, Events, Reports, Feedback
   - **Administrators**: All sections including Admin panel

**Nov 19, 2025 - Role-Based Dashboards**
✅ **Public Volunteer Signup** - Complete registration form with user account and volunteer profile
✅ **Administrator Dashboard** - Full management access with system status
✅ **Priest Dashboard** - Parish overview, reports, and announcements
✅ **Coordinator Dashboard** - Volunteer/event management with quick actions
✅ **Volunteer Dashboard** - Personal events, ministries, and announcements

### Priority Items for Future Development
1. **CRUD Coverage** - Attendance and Feedback modules need full CRUD views (currently list-only).
2. **Enhanced Analytics** - Reports module shows counts; needs deeper analytics (participation rates, demographics breakdowns).
3. **Templates** - Need form/detail/delete templates for attendance and feedback modules.
4. **Email Notifications** - Implement actual email sending for event reminders

### Enhancements
- Email backend configuration for production
- CSV/PDF export for reports
- Advanced filtering and search
- Volunteer recognition system with badges
- Calendar view for events
- SMS notifications (optional)

## Quick Start

### First Time Setup
```bash
# Install dependencies
pip install django pillow

# Run migrations (already done)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver 0.0.0.0:5000
```

### Access Points
- **Main Dashboard**: http://localhost:5000/
- **Admin Panel**: http://localhost:5000/admin/
- **Login**: http://localhost:5000/accounts/login/

### Default Roles
- **Administrator**: Full system access including volunteer approval, ministry assignment, all menu items visible
- **Priest**: Exclusive event creation/management for assigned ministry, view reports, access to events and feedback
- **Coordinator**: Manage volunteers (including approval), events, attendance, communications (within assigned ministry)
- **Volunteer**: View assigned events and feedback only (limited menu access)

## File Structure
```
ccvms/
├── accounts/          # Authentication & user management
├── volunteers/        # Volunteer CRUD
├── ministries/        # Ministry management
├── events/           # Event scheduling
├── attendance/       # Attendance tracking
├── communications/   # Announcements
├── reports/          # Analytics
├── feedback/         # Evaluations
├── templates/        # HTML templates
├── static/           # Static files
├── ccvms/            # Project settings
├── README.md         # Installation guide
└── .gitignore       # Git ignore rules
```

## Development Notes

### Database Models
- All models have proper `__str__` methods
- Proper use of `related_name` for reverse relationships
- **User model**: Added `approval_status` field (pending/approved/rejected)
- **Volunteer model**: Added `supporting_document` FileField for document uploads
- ManyToMany relationships where appropriate
- Timestamp fields (created_at, updated_at) where needed

### Forms
- ModelForms for all CRUD operations
- Custom widgets for better UX (Textarea, DateInput, etc.)
- Form validation included

### Views
- Class-based views (ListView, CreateView, UpdateView, DeleteView, DetailView)
- Permission mixins for access control
- Proper success redirects

### URL Configuration
- App-level URL namespacing
- RESTful URL patterns
- Hierarchical routing

## Maintenance

### Adding New Users
Use the Admin panel or Volunteers module to add users. Note: Volunteers created through the form need passwords set manually via Admin.

### Updating Roles
Change user roles in Admin panel under Users section.

### Backing Up Data
```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Backup media files
cp -r media media.backup
```

## Production Deployment Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure `SECRET_KEY` from environment
- [ ] Update `ALLOWED_HOSTS`
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up proper email backend
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Set up logging
- [ ] Configure backup strategy

## Support & Maintenance
For issues or questions, refer to the Django documentation or contact the system administrator.

---

**Last Updated**: November 19, 2025  
**Version**: 1.0 MVP  
**Django Version**: 5.2.8  
**Python Version**: 3.11
