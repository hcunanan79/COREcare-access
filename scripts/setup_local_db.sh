#!/bin/bash
# Setup local PostgreSQL database for development
# This script creates a local database that mirrors the production schema

set -e

DB_NAME="corecare_dev"
DB_USER="corecare_user"
DB_PASSWORD="corecare_dev_password"

echo "=== COREcare Local Database Setup ==="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed."
    echo ""
    echo "Install it using one of these methods:"
    echo ""
    echo "  macOS (Homebrew):"
    echo "    brew install postgresql@16"
    echo "    brew services start postgresql@16"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get install postgresql postgresql-contrib"
    echo "    sudo systemctl start postgresql"
    echo ""
    echo "  Docker:"
    echo "    docker run --name corecare-postgres -e POSTGRES_PASSWORD=corecare_dev_password -e POSTGRES_USER=corecare_user -e POSTGRES_DB=corecare_dev -p 5432:5432 -d postgres:16"
    echo ""
    exit 1
fi

echo "PostgreSQL found: $(psql --version)"
echo ""

# Check if database already exists
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Database '$DB_NAME' already exists."
    read -p "Do you want to drop and recreate it? (y/N): " confirm
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        echo "Dropping existing database..."
        dropdb $DB_NAME 2>/dev/null || sudo -u postgres dropdb $DB_NAME
    else
        echo "Keeping existing database."
        exit 0
    fi
fi

# Create user if it doesn't exist
echo "Creating database user '$DB_USER'..."
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || \
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || \
    echo "User may already exist, continuing..."

# Create database
echo "Creating database '$DB_NAME'..."
createdb -O $DB_USER $DB_NAME 2>/dev/null || \
    sudo -u postgres createdb -O $DB_USER $DB_NAME

# Grant privileges
echo "Granting privileges..."
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo ""
echo "=== Database created successfully! ==="
echo ""
echo "Add this to your .env file or export it:"
echo ""
echo "  export DATABASE_URL=\"postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME\""
echo ""
echo "Or create a .env file:"
echo ""
echo "  echo 'DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME' > .env"
echo ""
echo "Then run migrations:"
echo ""
echo "  python manage.py migrate"
echo ""
echo "To sync data from production, run:"
echo ""
echo "  ./scripts/sync_from_prod.sh"
echo ""
