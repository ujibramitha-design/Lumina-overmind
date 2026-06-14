# JARVIS AI System Runbook

Runbook operasional untuk JARVIS AI System dengan prosedur dan troubleshooting.

## Overview

Runbook ini berisi prosedur operasional untuk manajemen JARVIS AI System dalam environment production.

## System Status Check

### Check System Health
```bash
# Check PM2 status
pm2 status

# Check JARVIS app logs
pm2 logs jarvis-app

# Check Lumina app logs
pm2 logs lumina-app

# Check system resources
pm2 monit
```

### Check API Endpoints
```bash
# Check health endpoint
curl http://localhost:3001/health

# Check JARVIS status
curl http://localhost:3001/api/status

# Check Lumina status
curl http://localhost:8000/health
```

### Check Database
```bash
# Check SQLite database
sqlite3 data/financial_ledger.db ".tables"

# Check database size
ls -lh data/

# Check database integrity
sqlite3 data/financial_ledger.db "PRAGMA integrity_check;"
```

## Startup Procedures

### Normal Startup
```bash
# Navigate to JARVIS directory
cd "JARVIS SYSTEM/jarvis"

# Start JARVIS with PM2
pm2 start ecosystem.config.js

# Save PM2 process list
pm2 save

# Check status
pm2 status
```

### Startup After Crash
```bash
# Check crash logs
pm2 logs jarvis-app --err

# Restart JARVIS
pm2 restart jarvis-app

# Monitor restart
pm2 logs jarvis-app --lines 100
```

### Startup After Server Reboot
```bash
# PM2 should auto-start if configured
# If not, start manually:
pm2 resurrect

# Verify all processes
pm2 status
```

## Shutdown Procedures

### Normal Shutdown
```bash
# Stop JARVIS gracefully
pm2 stop jarvis-app

# Stop Lumina gracefully
pm2 stop lumina-app

# Verify stopped
pm2 status
```

### Emergency Shutdown
```bash
# Stop all processes immediately
pm2 stop all

# Kill if not responding
pm2 delete all

# Force kill if needed
pkill -f node
```

### Maintenance Shutdown
```bash
# Stop JARVIS only
pm2 stop jarvis-app

# Perform maintenance
# ...

# Restart JARVIS
pm2 start jarvis-app
```

## Monitoring Procedures

### Daily Monitoring
```bash
# Check system uptime
pm2 status

# Check error logs
pm2 logs jarvis-app --err --lines 50

# Check resource usage
pm2 monit

# Check disk space
df -h

# Check memory usage
free -h
```

### Weekly Monitoring
```bash
# Check log file sizes
ls -lh logs/

# Rotate logs if needed
pm2 rotate

# Check database size
ls -lh data/

# Backup database
cp data/financial_ledger.db backups/$(date +%Y%m%d).db

# Check API response times
curl -w "@curl-format.txt" http://localhost:3001/health
```

### Monthly Monitoring
```bash
# Full system audit
pm2 list

# Check all logs
pm2 logs --nostream

# Check database performance
sqlite3 data/financial_ledger.db "EXPLAIN QUERY PLAN SELECT * FROM transactions;"

# Check for security vulnerabilities
npm audit

# Update dependencies
npm update
```

## Backup Procedures

### Database Backup
```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d)

# Backup SQLite database
cp data/financial_ledger.db backups/$(date +%Y%m%d)/

# Backup state files
cp data/*.json backups/$(date +%Y%m%d)/

# Compress backup
tar -czf backups/$(date +%Y%m%d).tar.gz backups/$(date +%Y%m%d)/

# Clean old backups (keep 30 days)
find backups/ -name "*.tar.gz" -mtime +30 -delete
```

### Configuration Backup
```bash
# Backup environment variables
cp .env backups/$(date +%Y%m%d)/.env.backup

# Backup PM2 configuration
cp ecosystem.config.js backups/$(date +%Y%m%d)/

# Backup Terraform configuration
cp -r hydra/terraform backups/$(date +%Y%m%d)/
```

### Full System Backup
```bash
# Backup entire JARVIS directory
tar -czf backups/jarvis-full-$(date +%Y%m%d).tar.gz "JARVIS SYSTEM/jarvis/"

# Upload to cloud storage (optional)
# aws s3 cp backups/jarvis-full-$(date +%Y%m%d).tar.gz s3://backups/
```

## Restore Procedures

### Database Restore
```bash
# Stop JARVIS
pm2 stop jarvis-app

# Restore database
cp backups/20240115/financial_ledger.db data/

# Restore state files
cp backups/20240115/*.json data/

# Start JARVIS
pm2 start jarvis-app

# Verify
pm2 logs jarvis-app --lines 50
```

### Configuration Restore
```bash
# Stop JARVIS
pm2 stop jarvis-app

# Restore environment variables
cp backups/20240115/.env.backup .env

# Restore PM2 configuration
cp backups/20240115/ecosystem.config.js .

# Start JARVIS
pm2 start jarvis-app
```

### Full System Restore
```bash
# Stop all processes
pm2 stop all

# Extract backup
tar -xzf backups/jarvis-full-20240115.tar.gz

# Restore files
cp -r jarvis/* "JARVIS SYSTEM/jarvis/"

# Start JARVIS
pm2 start ecosystem.config.js
```

## Troubleshooting

### JARVIS Not Responding

**Symptoms**: API endpoints timeout, no response

**Steps**:
1. Check PM2 status: `pm2 status`
2. Check logs: `pm2 logs jarvis-app --err`
3. Check port: `netstat -tlnp | grep 3001`
4. Restart JARVIS: `pm2 restart jarvis-app`
5. If still not responding, check system resources: `top`

**Common Causes**:
- Out of memory
- CPU overload
- Database locked
- Network issue

---

### AI Not Responding

**Symptoms**: AI responses timeout or fail

**Steps**:
1. Check Gemini API key in .env
2. Check Ollama status: `ollama list`
3. Check brain service logs
4. Test failover: Trigger timeout to test Ollama
5. Restart AI service if needed

**Common Causes**:
- API key invalid
- Ollama not running
- Network issue
- Timeout too short

---

### WhatsApp Not Working

**Symptoms**: WhatsApp messages not sending/receiving

**Steps**:
1. Check WhatsApp client logs
2. Verify session file exists
3. Check WhatsApp API credentials
4. Re-authenticate if needed
5. Restart WhatsApp client

**Common Causes**:
- Session expired
- Authentication failed
- Network issue
- API limit reached

---

### Telegram Not Working

**Symptoms**: Telegram bot not responding

**Steps**:
1. Check Telegram bot logs
2. Verify bot token in .env
3. Check bot is not blocked by Telegram
4. Test bot with `/start` command
5. Restart Telegram bot

**Common Causes**:
- Bot token invalid
- Bot blocked
- Network issue
- Webhook issue

---

### Database Locked

**Symptoms**: Database operations fail with "database is locked"

**Steps**:
1. Check for long-running transactions
2. Kill any hanging processes
3. Check database file permissions
4. Restart JARVIS to release locks
5. If persistent, restore from backup

**Common Causes**:
- Long-running transaction
- File permission issue
- Concurrent write conflict
- Database corruption

---

### Memory Leak

**Symptoms**: Memory usage increasing over time

**Steps**:
1. Monitor memory: `pm2 monit`
2. Check for memory leaks in code
3. Restart JARVIS periodically
4. Implement memory limits in PM2
5. Profile memory usage

**Common Causes**:
- Unclosed connections
- Memory leak in code
- Large data in memory
- Caching issue

---

### High CPU Usage

**Symptoms**: CPU usage consistently high

**Steps**:
1. Check CPU usage: `top`
2. Identify process using CPU
3. Check for infinite loops
4. Optimize heavy computations
5. Scale horizontally if needed

**Common Causes**:
- Infinite loop
- Heavy computation
- Inefficient algorithm
- DDoS attack

---

### Disk Space Full

**Symptoms**: System out of disk space

**Steps**:
1. Check disk usage: `df -h`
2. Clean log files: `pm2 flush`
3. Clean old backups
4. Clean temp files
5. Expand disk if needed

**Common Causes**:
- Log files too large
- Too many backups
- Database too large
- Temp files not cleaned

---

## Security Procedures

### Security Incident Response

**Steps**:
1. Isolate affected systems
2. Review audit logs
3. Identify breach scope
4. Rotate all credentials
5. Patch vulnerabilities
6. Notify stakeholders
7. Document incident
8. Implement prevention

### Credential Rotation

**Steps**:
1. Generate new credentials
2. Update .env file
3. Update external services
4. Restart affected services
5. Verify functionality
6. Document changes

### Security Audit

**Steps**:
1. Review access logs
2. Check for unauthorized access
3. Review user permissions
4. Scan for vulnerabilities
5. Review code for security issues
6. Update dependencies
7. Document findings

## Performance Tuning

### Database Optimization

**Steps**:
1. Analyze slow queries
2. Add indexes
3. Optimize queries
4. Vacuum database
5. Analyze query plan

### Application Optimization

**Steps**:
1. Profile application
2. Identify bottlenecks
3. Optimize code
4. Implement caching
5. Load balance

### Resource Optimization

**Steps**:
1. Monitor resource usage
2. Adjust PM2 limits
3. Optimize memory usage
4. Optimize CPU usage
5. Scale resources

## Emergency Procedures

### System Down

**Steps**:
1. Check PM2 status
2. Check logs
3. Restart services
4. Check network
5. Check database
6. Notify stakeholders

### Data Loss

**Steps**:
1. Stop all writes
2. Assess damage
3. Restore from backup
4. Verify data integrity
5. Investigate cause
6. Implement prevention

### Security Breach

**Steps**:
1. Isolate systems
2. Review logs
3. Rotate credentials
4. Patch vulnerabilities
5. Notify stakeholders
6. Document incident

## Maintenance Schedule

### Daily
- Check system status
- Review error logs
- Monitor resources
- Verify backups

### Weekly
- Review performance
- Check disk space
- Rotate logs
- Test backups

### Monthly
- Security audit
- Dependency updates
- Performance review
- Capacity planning

### Quarterly
- Full system review
- Architecture review
- Cost optimization
- Strategic planning

## Contact Information

### Primary Contacts
- Creator: [Phone/Email]
- DevOps: [Phone/Email]
- Security: [Phone/Email]

### Emergency Contacts
- 24/7 Support: [Phone]
- On-call: [Phone]
- Management: [Phone]

## Appendix

### Useful Commands

```bash
# PM2 commands
pm2 list                    # List all processes
pm2 status                  # Status of all processes
pm2 logs [app]              # Logs for specific app
pm2 monit                   # Monitor resources
pm2 restart [app]           # Restart app
pm2 stop [app]              # Stop app
pm2 delete [app]            # Delete app
pm2 flush                   # Flush logs

# System commands
top                         # Monitor CPU/memory
df -h                       # Check disk space
free -h                     # Check memory
netstat -tlnp               # Check network ports
ps aux                      # Check processes

# Database commands
sqlite3 [db] ".tables"      # List tables
sqlite3 [db] "PRAGMA integrity_check;"  # Check integrity
sqlite3 [db] "VACUUM;"      # Optimize database
```

### Log Locations

- PM2 logs: `~/.pm2/logs/`
- JARVIS logs: `logs/`
- Error logs: `logs/jarvis-error.log`
- Access logs: `logs/jarvis-access.log`

### Configuration Files

- Environment: `.env`
- PM2: `ecosystem.config.js`
- Docker: `docker-compose.yml`
- Terraform: `hydra/terraform/main.tf`
