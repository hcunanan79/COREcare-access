# COREcare Access

A Django-based home care management platform for coordinating caregivers, clients, scheduling, and credentials tracking.

## Live Application

**Production URL:** https://corecare-access.onrender.com

## Features

- **Portal** - Main user portal for authentication and dashboard access
- **Caregiver Portal** - Dedicated interface for caregivers to manage their work
- **Client Management** - Track and manage client information
- **Scheduling** - Coordinate shifts and appointments
- **Timeclock** - Clock in/out functionality for caregivers
- **Shifts** - Manage and view upcoming shifts
- **Credentials** - Track caregiver certifications and credentials
- **Assessments** - Client assessment tools
- **Notifications** - Automated notifications for credential expirations

## Tech Stack

- **Framework:** Django 5.2.9
- **Database:** SQLite (development) / PostgreSQL 16 (production)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Geolocation:** GeoPy
- **Hosting:** Render

## Architecture

### Database

The application uses a flexible database configuration via `dj_database_url`:

- **Local Development:** SQLite (`db.sqlite3`) - no setup required
- **Production:** PostgreSQL 16 hosted on Render
  - Database: `corecare-db`
  - Region: Virginia (US East)
  - Persistent storage ensures data survives deployments

The database configuration automatically detects the environment:
- If `DATABASE_URL` environment variable is set, it uses PostgreSQL
- Otherwise, it falls back to SQLite for local development

### Deployment Pipeline

1. Code pushed to `main` branch triggers auto-deploy on Render
2. Build phase: Install dependencies and collect static files
3. Migrations are run manually via SSH after deployment
4. Gunicorn serves the application

## Prerequisites

- Python 3.11+
- pip

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/hcunanan79/COREcare-access.git
   cd COREcare-access
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Project Structure

```
COREcare-access/
├── assessments/        # Client assessment functionality
├── caregiver_portal/   # Caregiver-specific views and features
├── clients/            # Client management
├── credentials/        # Caregiver credentials tracking
├── elitecare/          # Django project settings
├── employees/          # Employee management
├── notifications/      # Notification system
├── portal/             # Main portal and authentication
├── scheduling/         # Scheduling functionality
├── shifts/             # Shift management
├── static/             # Static assets
├── templates/          # HTML templates
├── timeclock/          # Time tracking
├── manage.py           # Django management script
├── Procfile            # Render deployment config
└── requirements.txt    # Python dependencies
```

## Environment Variables

For production deployment, set the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | Yes |
| `DEBUG` | Set to `False` in production | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
| `DATABASE_URL` | PostgreSQL connection string (internal Render URL) | Yes |
| `DJANGO_SETTINGS_MODULE` | `elitecare.settings` | Yes |
| `EMPLOYEE_INVITE_CODE` | Code for employee self-registration | No |

## Deployment

The application is configured for deployment on Render with auto-deploy from the `main` branch.

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command
```bash
gunicorn elitecare.wsgi:application
```

### Running Migrations

After deployment, run migrations via SSH:
```bash
ssh srv-d5iu087pm1nc73fhf8k0@ssh.virginia.render.com "python manage.py migrate"
```

### Creating Admin Users

To create or reset an admin user via SSH:
```bash
ssh srv-d5iu087pm1nc73fhf8k0@ssh.virginia.render.com "python manage.py createsuperuser"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.
