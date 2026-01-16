# COREcare Access Architecture

This document provides an overview of the system architecture for new engineers.

## System Overview

COREcare Access is a Django-based web application for managing home care operations, including client management, caregiver scheduling, time tracking, credential management, **and family communication**.

It operates as a **Progressive Web App (PWA)**, providing offline capabilities for caregivers in the field.

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
                                ▲
                                │
                        ┌───────┴───────┐
                        │  Client PWA   │
                        │ Service Worker│
                        │ Offline Sync  │
                        └───────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Django 5.2 | Web application framework |
| Database | PostgreSQL 16 | Persistent data storage |
| Web Server | Gunicorn | WSGI HTTP server |
| Static Files | WhiteNoise | Static file serving |
| Hosting | Render | Cloud platform |
| **PWA** | Service Worker | Offline support & Caching |
| **Geolocation** | HTML5 Geolocation | GPS Tracking at Clock-in/out |

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
| **clients** | Client profiles & family access | Client, ClientFamilyMember, ClientMessage |
| **caregiver_portal** | Caregiver interface | Visit, ClockEvent, WeeklySummary |
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
2. **Caregivers** - Access caregiver portal, clock in/out (online/offline), view schedules
3. **Employees** - Access employee dashboard after signup
4. **Family Members** - Access Family Portal to view loved one's schedule

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

### Caregiver Time Tracking Flow (with Offline Sync)

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐
│Clock In │─▶Does│  Verify  │─▶Yes│  Record  │───▶│   Visit     │
│  Page   │  Con │ Location │     │  Entry   │    │   Active    │
└─────────┘  Exis│          │     │(AuditLog)│    └─────────────┘
    │        t?  └──────────┘     └──────────┘           │
    │ No                                                 ▼
    ▼                                             ┌─────────────┐
┌───────────┐                                     │Clock Out    │
│Queue in   │                                     │(Offline/On) │
│LocalStore │                                     └──────┬──────┘
└─────┬─────┘                                            │
      │ (Connection Restored)                            ▼
      ▼                                           ┌─────────────┐
┌───────────┐                                     │   Weekly    │
│ Auto-Sync │────────────────────────────────────▶│   Summary   │
│ to Server │                                     │ (Pre-Calc)  │
└───────────┘                                     └─────────────┘
```

## Database Schema

### Key Relationships

```
User (Django Auth)
  │
  ├── CareTeam (proxy)
  ├── FamilyMembers (via Client)
  │     └── ClientMessages
  │
  └── Visits
        │
        ├── Client
        ├── ClockEvents (Audit)
        └── Shifts
```

### Data Flow

1. **Clients** are created by administrators
2. **Shifts** are scheduled for clients with assigned caregivers
3. **Visits** are recorded when caregivers clock in/out
4. **ClockEvents** store immutable audit logs + GPS data
5. **WeeklySummaries** aggregate hours nightly for performance
6. **Family Members** communicate via ClientMessages

## Template Structure

```
templates/
├── base.html                 # Main layout (includes PWA manifest)
├── offline.html              # PWA Fallback page
├── sw.js                     # Service Worker
├── admin/                    # Django admin overrides
├── portal/                   # Portal templates
│   ├── login.html
│   ├── signup.html
│   ├── employee_dashboard.html
│   ├── family_home.html          # New
│   └── family_client_detail.html # New
├── caregiver_portal/         # Caregiver templates
│   └── clock_out.html        # Enhanced UI
└── ...
```

## URL Structure

| Pattern | App | Description |
|---------|-----|-------------|
| `/admin/` | Django Admin | Administration interface |
| `/portal/` | portal | Main portal & auth |
| `/portal/dashboard/` | portal | Employee dashboard |
| `/portal/family/` | portal | Family Portal root |
| `/portal/offline/` | portal | PWA Offline fallback |
| `/caregiver/` | caregiver_portal | Caregiver features |
| `/sw.js` | elitecare | Service Worker (App Root) |

## Security and Integrity

### Authentication
- Django's built-in authentication system
- Session-based authentication
- Invite code required for new registrations

### Audit & Compliance
- **ClockEvent**: Immutable log of every clock-in/out attempt.
- **Geolocation**: GPS coordinates captured on every action.
- **CSRF**: Protection enabled on all forms.

### Access Control
- `@login_required` decorator for protected views
- **Row-Level Security**:
    - Caregivers only see *their* shifts.
    - Family Members only see *their* linked clients.

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

### Static Files & PWA

- Collected to `staticfiles/` directory
- Served by WhiteNoise middleware
- PWA Manifest linked in `base.html`
- Service Worker served from root `/sw.js`

## Future Considerations

- **Native Mobile Integration** - Wrap PWA in Capacitor/Cordova.
- **Real-time Updates** - WebSocket for live family messages.
- **Reporting** - Analytics and reporting dashboard (partially solved by WeeklySummary).
