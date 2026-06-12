#!/bin/bash

# =============================================================================
# LUMINA OS - DATABASE BACKUP SCRIPT
# =============================================================================
# PostgreSQL Database Backup Utility for Docker Container
# Usage: ./scripts/backup_db.sh [backup_name]
# Example: ./scripts/backup_db.sh lumina_backup_$(date +%Y%m%d_%H%M%S)

set -e  # Exit on any error

# Configuration
CONTAINER_NAME="lumina_postgres"
DB_NAME="lumina_os"
DB_USER="lumina_user"
BACKUP_DIR="./database/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEFAULT_BACKUP_NAME="lumina_backup_${TIMESTAMP}"

# Parse command line arguments
BACKUP_NAME=${1:-$DEFAULT_BACKUP_NAME}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup directory if it doesn't exist
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# Check if Docker container is running
check_container() {
    log_info "Checking if PostgreSQL container is running..."
    
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        log_error "Container '$CONTAINER_NAME' is not running!"
        echo "Please start the container with: docker-compose up -d postgres"
        exit 1
    fi
    
    log_success "PostgreSQL container is running"
}

# Test database connection
test_connection() {
    log_info "Testing database connection..."
    
    if docker exec "$CONTAINER_NAME" pg_isready -U "$DB_USER" -d "$DB_NAME" > /dev/null 2>&1; then
        log_success "Database connection successful"
    else
        log_error "Cannot connect to database!"
        exit 1
    fi
}

# Create backup
create_backup() {
    local backup_file="$BACKUP_DIR/${BACKUP_NAME}.sql"
    local compressed_file="$BACKUP_DIR/${BACKUP_NAME}.sql.gz"
    
    log_info "Creating database backup: $backup_file"
    
    # Create SQL dump
    if docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" > "$backup_file"; then
        log_success "SQL dump created successfully"
        
        # Compress the backup
        log_info "Compressing backup file..."
        gzip "$backup_file"
        
        # Get file size
        local file_size=$(du -h "$compressed_file" | cut -f1)
        log_success "Backup compressed: $compressed_file ($file_size)"
        
        # Create checksum
        log_info "Creating checksum..."
        sha256sum "$compressed_file" > "$compressed_file.sha256"
        
        # Show backup info
        echo ""
        echo "=============================================="
        echo "BACKUP COMPLETED SUCCESSFULLY"
        echo "=============================================="
        echo "Backup File: $compressed_file"
        echo "File Size: $file_size"
        echo "Checksum: $compressed_file.sha256"
        echo "Created: $(date)"
        echo "=============================================="
        
    else
        log_error "Failed to create database backup!"
        exit 1
    fi
}

# List existing backups
list_backups() {
    log_info "Listing existing backups:"
    
    if [ -d "$BACKUP_DIR" ] && [ "$(ls -A $BACKUP_DIR 2>/dev/null)" ]; then
        ls -lah "$BACKUP_DIR"/*.sql.gz 2>/dev/null | while read -r line; do
            echo "  $line"
        done
    else
        log_warning "No backups found in $BACKUP_DIR"
    fi
}

# Restore backup function (for future use)
restore_backup() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        log_error "Please provide backup file to restore"
        echo "Usage: $0 restore <backup_file.sql.gz>"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    log_warning "This will overwrite the current database. Are you sure? (y/N)"
    read -r confirmation
    
    if [[ $confirmation =~ ^[Yy]$ ]]; then
        log_info "Restoring database from: $backup_file"
        
        # Extract and restore
        gunzip -c "$backup_file" | docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME"
        
        log_success "Database restored successfully"
    else
        log_info "Restore cancelled"
    fi
}

# Main execution
main() {
    echo ""
    echo "=============================================="
    echo "LUMINA OS - DATABASE BACKUP UTILITY"
    echo "=============================================="
    echo ""
    
    # Handle restore command
    if [ "$1" = "restore" ]; then
        restore_backup "$2"
        exit 0
    fi
    
    # Handle list command
    if [ "$1" = "list" ]; then
        list_backups
        exit 0
    fi
    
    # Create backup
    create_backup_dir
    check_container
    test_connection
    create_backup
    list_backups
    
    echo ""
    log_info "To restore this backup later, run:"
    echo "  $0 restore $BACKUP_DIR/${BACKUP_NAME}.sql.gz"
    echo ""
}

# Run main function with all arguments
main "$@"
