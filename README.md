# COREcare Access

A Django-based home care management platform for coordinating caregivers, clients, scheduling, and credentials tracking.

## Quick Links

| Resource | Description |
|----------|-------------|
| [Production App](https://corecare-access.onrender.com) | Live application |
| [Admin Panel](https://corecare-access.onrender.com/admin/) | Administration interface |
| [Architecture Guide](docs/ARCHITECTURE.md) | System design & overview |
| [Employee Onboarding](docs/EMPLOYEE_ONBOARDING.md) | New employee signup guide |
| [Contributing Guide](CONTRIBUTING.md) | Developer guidelines |

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
- **Database:** PostgreSQL 16 (both development and production)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **Geolocation:** GeoPy
- **Hosting:** Render

## Architecture

### Database

The application uses PostgreSQL 16 in both development and production for consistency:

- **Local Development:** PostgreSQL running locally (via Homebrew, apt, or Docker)
- **Production:** PostgreSQL 16 hosted on Render
  - Database: `corecare-db`
  - Region: Virginia (US East)
  - Persistent storage ensures data survives deployments

The database is configured via the `DATABASE_URL` environment variable using `dj_database_url`.

### Data Sync

Developers can sync production data to their local database:
```bash
./scripts/sync_from_prod.sh
```

This creates a backup from production and restores it locally, ensuring developers work with realistic data. Backups are stored in `./backups/` (last 5 retained).

### Deployment Pipeline

1. Code pushed to `main` branch triggers auto-deploy on Render
2. Build phase: Install dependencies and collect static files
3. Migrations are run manually via SSH after deployment
4. Gunicorn serves the application

## Prerequisites

- Python 3.11+
- pip
- PostgreSQL 16 (local installation)

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

4. **Set up local PostgreSQL database**
   ```bash
   # Install PostgreSQL if not already installed
   # macOS: brew install postgresql@16 && brew services start postgresql@16
   # Ubuntu: sudo apt-get install postgresql postgresql-contrib

   # Run the setup script
   ./scripts/setup_local_db.sh
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults should work)

   # Load environment variables
   export $(cat .env | xargs)
   ```

6. **Sync data from production (recommended)**
   ```bash
   ./scripts/sync_from_prod.sh
   ```

7. **Or run fresh migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

### Docker Alternative

If you prefer Docker for PostgreSQL:
```bash
docker run --name corecare-postgres \
  -e POSTGRES_PASSWORD=corecare_dev_password \
  -e POSTGRES_USER=corecare_user \
  -e POSTGRES_DB=corecare_dev \
  -p 5432:5432 \
  -d postgres:16
```

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
├── scripts/            # Development and deployment scripts
│   ├── setup_local_db.sh   # Create local PostgreSQL database
│   └── sync_from_prod.sh   # Sync production data to local
├── shifts/             # Shift management
├── static/             # Static assets
├── templates/          # HTML templates
├── timeclock/          # Time tracking
├── backups/            # Database backups (gitignored)
├── .env.example        # Example environment variables
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed developer guidelines, including:

- Branch strategy and workflow
- Code style conventions
- Pull request process
- Common development tasks

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture, app structure, data flow |
| [EMPLOYEE_ONBOARDING.md](docs/EMPLOYEE_ONBOARDING.md) | How to invite and onboard new employees |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer setup and contribution guidelines |

## License

This project is proprietary software. All rights reserved.
