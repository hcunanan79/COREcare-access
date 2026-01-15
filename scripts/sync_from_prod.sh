#!/bin/bash
# Sync production database to local development database
# This script creates a backup from production and restores it locally

set -e

# Production database credentials (external connection string)
PROD_HOST="dpg-d5kad4fpm1nc73fv31n0-a.virginia-postgres.render.com"
PROD_PORT="5432"
PROD_DB="corecare_db"
PROD_USER="corecare_db_user"
PROD_PASSWORD="u2BqbK5R4siSH6LWo6ZyV2N7Oyax2uZz"

# Local database credentials
LOCAL_DB="corecare_dev"
LOCAL_USER="corecare_user"
LOCAL_PASSWORD="corecare_dev_password"

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/prod_backup_$TIMESTAMP.sql"

echo "=== COREcare Production to Local Sync ==="
echo ""

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Check if pg_dump is available
if ! command -v pg_dump &> /dev/null; then
    echo "Error: pg_dump not found. Please install PostgreSQL client tools."
    exit 1
fi

echo "Step 1: Creating backup from production..."
echo "  Host: $PROD_HOST"
echo "  Database: $PROD_DB"
echo ""

PGPASSWORD=$PROD_PASSWORD pg_dump \
    -h $PROD_HOST \
    -p $PROD_PORT \
    -U $PROD_USER \
    -d $PROD_DB \
    --no-owner \
    --no-acl \
    --clean \
    --if-exists \
    -f $BACKUP_FILE

echo "  Backup saved to: $BACKUP_FILE"
echo "  Size: $(du -h $BACKUP_FILE | cut -f1)"
echo ""

echo "Step 2: Restoring to local database..."
echo "  Database: $LOCAL_DB"
echo ""

# Check if local database exists
if ! psql -lqt | cut -d \| -f 1 | grep -qw $LOCAL_DB; then
    echo "Error: Local database '$LOCAL_DB' does not exist."
    echo "Run ./scripts/setup_local_db.sh first."
    exit 1
fi

# Restore backup to local database
PGPASSWORD=$LOCAL_PASSWORD psql \
    -h localhost \
    -U $LOCAL_USER \
    -d $LOCAL_DB \
    -f $BACKUP_FILE \
    --quiet

echo "Step 3: Verifying restore..."
echo ""

# Count tables
TABLE_COUNT=$(PGPASSWORD=$LOCAL_PASSWORD psql -h localhost -U $LOCAL_USER -d $LOCAL_DB -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
echo "  Tables restored: $TABLE_COUNT"

# Count users
USER_COUNT=$(PGPASSWORD=$LOCAL_PASSWORD psql -h localhost -U $LOCAL_USER -d $LOCAL_DB -t -c "SELECT COUNT(*) FROM auth_user;" 2>/dev/null || echo "0")
echo "  Users: $USER_COUNT"

echo ""
echo "=== Sync completed successfully! ==="
echo ""
echo "Your local database now mirrors production."
echo ""
echo "To connect with Django, ensure DATABASE_URL is set:"
echo "  export DATABASE_URL=\"postgresql://$LOCAL_USER:$LOCAL_PASSWORD@localhost:5432/$LOCAL_DB\""
echo ""

# Cleanup old backups (keep last 5)
echo "Cleaning up old backups (keeping last 5)..."
ls -t $BACKUP_DIR/prod_backup_*.sql 2>/dev/null | tail -n +6 | xargs -r rm
echo "Done."
