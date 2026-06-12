#!/bin/bash
# LUMINA OVERMIND SYSTEM - PostgreSQL Backup Script
# Enterprise-grade automated backup solution

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/var/backups/lumina_overmind}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="lumina_overmind_backup_${TIMESTAMP}.sql"

# Environment variables
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-lumina_os}"
DB_USER="${DB_USER:-lumina_user}"
DB_PASSWORD="${DB_PASSWORD:-lumina_secure_password_2024}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "${BACKUP_DIR}/backup.log"
}

# Health check function
health_check() {
    if ! pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}"; then
        log "ERROR: PostgreSQL health check failed"
        exit 1
    fi
    log "PostgreSQL health check passed"
}

# Backup function
perform_backup() {
    log "Starting PostgreSQL backup for database: ${DB_NAME}"
    
    # Create backup using pg_dump
    PGPASSWORD="${DB_PASSWORD}" pg_dump \
        -h "${DB_HOST}" \
        -p "${DB_PORT}" \
        -U "${DB_USER}" \
        -d "${DB_NAME}" \
        --verbose \
        --clean \
        --if-exists \
        --create \
        --format=custom \
        --compress=9 \
        --file="${BACKUP_DIR}/${BACKUP_FILE}"
    
    if [ $? -eq 0 ]; then
        log "Backup completed successfully: ${BACKUP_FILE}"
        
        # Generate checksum for integrity verification
        sha256sum "${BACKUP_DIR}/${BACKUP_FILE}" > "${BACKUP_DIR}/${BACKUP_FILE}.sha256"
        log "Checksum generated: ${BACKUP_FILE}.sha256"
        
    else
        log "ERROR: Backup failed"
        exit 1
    fi
}

# Cleanup function
cleanup_old_backups() {
    log "Cleaning up backups older than ${RETENTION_DAYS} days"
    
    # Remove old backup files
    find "${BACKUP_DIR}" -name "lumina_overmind_backup_*.sql" -mtime +${RETENTION_DAYS} -delete
    find "${BACKUP_DIR}" -name "lumina_overmind_backup_*.sql.sha256" -mtime +${RETENTION_DAYS} -delete
    
    # Remove old log files (keep 30 days)
    find "${BACKUP_DIR}" -name "backup.log" -mtime +30 -delete
    
    log "Cleanup completed"
}

# Verification function
verify_backup() {
    log "Verifying backup integrity"
    
    if [ -f "${BACKUP_DIR}/${BACKUP_FILE}.sha256" ]; then
        if sha256sum -c "${BACKUP_DIR}/${BACKUP_FILE}.sha256" > /dev/null 2>&1; then
            log "Backup integrity verified successfully"
        else
            log "ERROR: Backup integrity verification failed"
            exit 1
        fi
    else
        log "WARNING: Checksum file not found, skipping integrity verification"
    fi
}

# Main execution
main() {
    log "=== LUMINA OVERMIND BACKUP PROCESS STARTED ==="
    
    health_check
    perform_backup
    verify_backup
    cleanup_old_backups
    
    log "=== BACKUP PROCESS COMPLETED SUCCESSFULLY ==="
    log "Backup location: ${BACKUP_DIR}/${BACKUP_FILE}"
    log "Backup size: $(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)"
}

# Execute main function
main "$@"
