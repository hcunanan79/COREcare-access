# COREcare Access Architecture

This document provides an overview of the system architecture for new engineers.

## System Overview

COREcare Access is a Django-based web application for managing home care operations, including client management, caregiver scheduling, time tracking, and credential management.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Render Cloud                             │
│  ┌───────────────┐    ┌──────────────────┐    ┌──────────────┐  │
│  │   Gunicorn    │    │    Django App    │    │  PostgreSQL  │  │
│  │  Web Server   │───▶│   (elitecare)    │───▶│   Database   │  │
│  └───────────────┘    └──────────────────┘    └──────────────┘  │
│                              │                                   │
│                       ┌──────┴──────┐                           │
│                       │ WhiteNoise  │                           │
│                       │Static Files │                           │
│                       └─────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Django 5.2 | Web application framework |
| Database | PostgreSQL 16 | Persistent data storage |
| Web Server | Gunicorn | WSGI HTTP server |
| Static Files | WhiteNoise | Static file serving |
| Hosting | Render | Cloud platform |
| Geolocation | GeoPy | Address/location services |

## Django Apps

The application is divided into 10 Django apps, each handling a specific domain:

### Core Apps

| App | Purpose | Key Models |
|-----|---------|------------|
| **portal** | Authentication & user management | SignUpForm |
| **elitecare** | Project configuration | Settings, URLs |

### Domain Apps

| App | Purpose | Key Models |
|-----|---------|------------|
| **clients** | Client profiles & information | Client, CareTeam |
| **caregiver_portal** | Caregiver interface | Visit |
| **shifts** | Shift scheduling | Shift |
| **timeclock** | Clock in/out tracking | TimeEntry |
| **employees** | Employee profiles | Employee |
| **credentials** | Certification tracking | Credential |
| **assessments** | Client assessments | Assessment |
| **scheduling** | Schedule coordination | (scheduling logic) |
| **notifications** | Alerts & notifications | (planned) |

## Application Flow

### User Types

1. **Administrators** - Access Django admin panel, manage all data
2. **Caregivers** - Access caregiver portal, clock in/out, view schedules
3. **Employees** - Access employee dashboard after signup

### Authentication Flow

```
┌──────────┐     ┌───────────┐     ┌─────────────┐     ┌───────────┐
│  Signup  │────▶│  Validate │────▶│   Create    │────▶│ Dashboard │
│   Page   │     │Invite Code│     │    User     │     │           │
└──────────┘     └───────────┘     └─────────────┘     └───────────┘
                       │
                       ▼ (invalid)
                 ┌───────────┐
                 │   Error   │
                 │  Message  │
                 └───────────┘
```

### Caregiver Time Tracking Flow

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐
│Clock In │────▶│  Select  │────▶│  Record  │────▶│   Visit     │
│  Page   │     │  Client  │     │  Entry   │     │   Active    │
└─────────┘     └──────────┘     └──────────┘     └─────────────┘
                                                         │
                                                         ▼
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│   Weekly    │◀────│Calculate │◀────│  Record  │◀────│Clock Out│
│   Summary   │     │ Duration │     │End Time  │     │  Page   │
└─────────────┘     └──────────┘     └──────────┘     └─────────┘
```

## Database Schema

### Key Relationships

```
User (Django Auth)
  │
  ├── CareTeam (proxy)
  │
  └── Visits
        │
        └── Client
              │
              └── Shifts
```

### Data Flow

1. **Clients** are created by administrators
2. **Shifts** are scheduled for clients with assigned caregivers
3. **Visits** are recorded when caregivers clock in/out
4. **Credentials** track caregiver certifications and expiration dates

## Template Structure

```
templates/
├── base.html                 # Main layout (header, nav, footer)
├── admin/                    # Django admin overrides
│   ├── base.html
│   ├── base_site.html
│   └── index.html
├── portal/                   # Portal templates
│   ├── login.html
│   ├── signup.html
│   └── employee_dashboard.html
├── caregiver_portal/         # Caregiver templates
├── clients/                  # Client templates
└── timeclock/                # Time tracking templates
```

### Template Inheritance

```
base.html
    │
    ├── portal/login.html
    ├── portal/signup.html
    ├── portal/employee_dashboard.html
    └── (other page templates)
```

## URL Structure

| Pattern | App | Description |
|---------|-----|-------------|
| `/admin/` | Django Admin | Administration interface |
| `/portal/` | portal | Main portal & auth |
| `/portal/login/` | portal | User login |
| `/portal/signup/` | portal | New user registration |
| `/portal/dashboard/` | portal | Employee dashboard |
| `/caregiver/` | caregiver_portal | Caregiver features |
| `/clients/` | clients | Client management |
| `/timeclock/` | timeclock | Time tracking |

## Security

### Authentication

- Django's built-in authentication system
- Session-based authentication
- Invite code required for new registrations

### Configuration

- `SECRET_KEY` - Environment variable (not in code)
- `EMPLOYEE_INVITE_CODE` - Configurable via environment
- CSRF protection enabled
- Session middleware active

### Access Control

- `@login_required` decorator for protected views
- Admin panel restricted to staff users
- Invite code gates new registrations

## Deployment Architecture

### Production (Render)

```
GitHub (main branch)
        │
        ▼ (push triggers)
┌───────────────────┐
│   Render Build    │
│  - pip install    │
│  - collectstatic  │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Render Service   │
│  - Gunicorn       │
│  - WhiteNoise     │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   PostgreSQL 16   │
│   (Render DB)     │
└───────────────────┘
```

### Development (Local)

```
Local Machine
┌───────────────────┐
│ Django runserver  │
│   Port 8000       │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   PostgreSQL 16   │
│   (Local/Docker)  │
└───────────────────┘
```

## Configuration

### Settings (`elitecare/settings.py`)

Key settings:

```python
# Database - uses DATABASE_URL or SQLite fallback
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# Authentication redirects
LOGIN_URL = "/portal/login/"
LOGIN_REDIRECT_URL = "/portal/dashboard/"

# Registration
EMPLOYEE_INVITE_CODE = os.environ.get("EMPLOYEE_INVITE_CODE", "CORECARE")
```

### Static Files

- Collected to `staticfiles/` directory
- Served by WhiteNoise middleware
- URL prefix: `/static/`

## Development Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup_local_db.sh` | Initialize local PostgreSQL database |
| `scripts/sync_from_prod.sh` | Sync production data to local |

## Future Considerations

- **API Layer** - REST API for mobile apps
- **Real-time Updates** - WebSocket for live notifications
- **Reporting** - Analytics and reporting dashboard
- **Mobile App** - Native iOS/Android apps
