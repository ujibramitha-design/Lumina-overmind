# LUMINA OS Enterprise - Operational Runbooks

## Table of Contents
1. [Application Startup](#application-startup)
2. [Database Operations](#database-operations)
3. [API Server Management](#api-server-management)
4. [Celery Worker Management](#celery-worker-management)
5. [Backup and Recovery](#backup-and-recovery)
6. [Monitoring and Alerting](#monitoring-and-alerting)
7. [Troubleshooting](#troubleshooting)
8. [Deployment](#deployment)

---

## Application Startup

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- PostgreSQL database running
- Redis server running
- Environment variables configured

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Configure required variables
# DATABASE_URL, SUPABASE_URL, SUPABASE_ANON_KEY, etc.
```

### Start PostgreSQL
```bash
# Using Docker
docker-compose up -d postgres

# Or local installation
sudo systemctl start postgresql
```

### Start Redis
```bash
# Using Docker
docker-compose up -d redis

# Or local installation
sudo systemctl start redis
```

### Start API Server
```bash
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Dashboard
```bash
cd dashboard
npm install
npm run dev
```

### Start Celery Workers
```bash
cd api
celery -A tasks.celery_app worker --loglevel=info
```

### Start Celery Beat (Scheduler)
```bash
cd api
celery -A tasks.celery_app beat --loglevel=info
```

---

## Database Operations

### Database Migrations
```bash
cd api
npx prisma migrate dev
npx prisma migrate deploy
```

### Database Seeding
```bash
cd api
python scripts/create_sample_leads.py
```

### Database Backup
```bash
# Automated backup
python scripts/enhanced_backup_system.py

# Manual backup
pg_dump -U postgres lumina_db > backup_$(date +%Y%m%d).sql
```

### Database Restore
```bash
# From SQL file
psql -U postgres lumina_db < backup_20240101.sql

# From enhanced backup system
python scripts/restore_backup.py --backup-id <backup_id>
```

### Database Optimization
```bash
# Run optimization utilities
python scripts/postgres_optimization.py

# Reindex tables
REINDEX TABLE leads;
REINDEX TABLE projects;
```

---

## API Server Management

### Check API Health
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/health
```

### View API Documentation
```bash
# Swagger UI (requires auth)
http://localhost:8000/docs

# ReDoc (requires auth)
http://localhost:8000/redoc

# OpenAPI JSON
http://localhost:8000/openapi.json
```

### Restart API Server
```bash
# Development
# Ctrl+C in terminal, then restart

# Production
sudo systemctl restart lumina-api
```

### View API Logs
```bash
# Development
# Check terminal output

# Production
sudo journalctl -u lumina-api -f
tail -f /var/log/lumina/api.log
```

### Rate Limiting Check
```bash
# Check rate limit status
curl -I http://localhost:8000/api/leads
```

---

## Celery Worker Management

### Check Worker Status
```bash
cd api
celery -A tasks.celery_app inspect active
celery -A tasks.celery_app inspect stats
```

### Restart Workers
```bash
# Find worker process
ps aux | grep celery

# Kill worker
pkill -f celery

# Restart worker
celery -A tasks.celery_app worker --loglevel=info
```

### Monitor Task Queue
```bash
celery -A tasks.celery_app inspect registered
celery -A tasks.celery_app inspect scheduled
celery -A tasks.celery_app inspect reserved
```

### Clear Task Queue
```bash
celery -A tasks.celery_app purge
```

---

## Backup and Recovery

### Automated Backup System
```bash
# Run enhanced backup system
python scripts/enhanced_backup_system.py

# Configure backup schedule in crontab
0 2 * * * cd /path/to/lumina-overmind && python scripts/enhanced_backup_system.py
```

### Backup Locations
- Local: `backups/local/`
- S3: Configured in environment variables
- Google Drive: Configured in environment variables

### Restore from Backup
```bash
# List available backups
python scripts/enhanced_backup_system.py --list

# Restore specific backup
python scripts/enhanced_backup_system.py --restore <backup_id>
```

### Disaster Recovery
1. Stop all services
2. Restore database from latest backup
3. Restore application files from backup
4. Restart services in order: PostgreSQL → Redis → API → Dashboard → Celery
5. Verify system health

---

## Monitoring and Alerting

### Application Monitoring
```bash
# Check system resources
python scripts/monitor_system.py

# Check integration status
python scripts/integration_checker.py
```

### Log Monitoring
```bash
# API logs
tail -f logs/api.log

# Celery logs
tail -f logs/celery.log

# Error logs
tail -f logs/error.log
```

### Performance Monitoring
```bash
# Check PostgreSQL performance
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_database;

# Check Redis performance
redis-cli INFO
```

### Alerting Setup
- Configure Sentry for error tracking
- Configure Prometheus for metrics
- Set up Grafana dashboards
- Configure email/SMS alerts for critical failures

---

## Troubleshooting

### API Not Starting
**Symptoms:** API server fails to start
**Solutions:**
1. Check environment variables are set
2. Verify PostgreSQL is running
3. Verify Redis is running
4. Check port 8000 is not in use
5. Review logs for specific errors

### Database Connection Errors
**Symptoms:** Cannot connect to database
**Solutions:**
1. Verify DATABASE_URL is correct
2. Check PostgreSQL is running
3. Verify database credentials
4. Check network connectivity
5. Test connection: `psql $DATABASE_URL`

### Celery Workers Not Processing Tasks
**Symptoms:** Tasks stuck in queue
**Solutions:**
1. Check Celery workers are running
2. Verify Redis is running
3. Check worker logs for errors
4. Restart Celery workers
5. Clear stuck tasks

### High Memory Usage
**Symptoms:** System running out of memory
**Solutions:**
1. Check for memory leaks in long-running processes
2. Restart services
3. Increase system memory
4. Optimize database queries
5. Implement caching

### Slow API Response Times
**Symptoms:** API endpoints responding slowly
**Solutions:**
1. Check database query performance
2. Implement database indexing
3. Enable caching
4. Check network latency
5. Scale horizontally

---

## Deployment

### Production Deployment
```bash
# Build dashboard
cd dashboard
npm run build

# Start production API server
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Start production dashboard
cd dashboard
npm start
```

### Docker Deployment
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment-Specific Configuration
- Development: Use `.env.development`
- Staging: Use `.env.staging`
- Production: Use `.env.production`

### Rollback Procedure
1. Stop current deployment
2. Restore previous version from git
3. Restore database from backup
4. Restart services
5. Verify functionality

---

## Security

### Update Dependencies
```bash
# Python dependencies
pip list --outdated
pip install --upgrade <package>

# Node dependencies
npm outdated
npm update
```

### Security Audit
```bash
# Python security audit
pip-audit

# Node security audit
npm audit
npm audit fix
```

### Access Control
- Review Casbin policies regularly
- Update user roles as needed
- Rotate API keys periodically
- Enable two-factor authentication

---

## Maintenance

### Regular Maintenance Tasks
- Weekly: Review logs and metrics
- Monthly: Update dependencies
- Quarterly: Security audit
- Annually: Disaster recovery drill

### Log Rotation
```bash
# Configure logrotate
sudo nano /etc/logrotate.d/lumina

# Test logrotate
sudo logrotate -d /etc/logrotate.d/lumina
```

### Database Maintenance
```bash
# Vacuum database
VACUUM ANALYZE;

# Reindex
REINDEX DATABASE lumina_db;

# Update statistics
ANALYZE;
```

---

## Support

### Contact Information
- Support Email: support@lumina.os
- Documentation: https://docs.lumina-os.com
- Issue Tracker: https://github.com/lumina-os/issues

### Emergency Contacts
- On-call Engineer: +62-XXX-XXXX-XXXX
- System Administrator: +62-XXX-XXXX-XXXX
