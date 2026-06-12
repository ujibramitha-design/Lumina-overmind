# 🚀 LUMINA OS - PRODUCTION DEPLOYMENT GUIDE

## 📋 PREREQUISITES

### Server Requirements
- **VPS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: Minimum 4GB (recommended 8GB+)
- **Storage**: Minimum 50GB SSD
- **CPU**: Minimum 2 cores (recommended 4+ cores)
- **Network**: Stable internet connection

### Software Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- Domain name (optional but recommended)

---

## 🔧 DEPLOYMENT STEPS

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone Repository
```bash
# Clone the repository
git clone <your-repository-url> lumina-os
cd lumina-os

# Create necessary directories
mkdir -p logs data reports static output nginx/ssl backups
```

### 3. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Critical Environment Variables:**
```env
# Production URLs
PUBLIC_URL=https://your-domain.com
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
WS_URL=wss://your-domain.com

# Security (use strong passwords)
POSTGRES_PASSWORD=your_strong_postgres_password
REDIS_PASSWORD=your_strong_redis_password
SECRET_KEY=your_super_secret_key_minimum_32_characters

# API Keys
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Monitoring
GRAFANA_PASSWORD=your_grafana_admin_password
```

### 4. SSL Certificate (Optional but Recommended)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to nginx folder
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

### 5. Deploy Application
```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up -d --build

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 6. Database Migration
```bash
# Access FastAPI container
docker exec -it lumina_fastapi bash

# Generate Prisma client
npx prisma generate

# Run database migrations
npx prisma migrate deploy

# Exit container
exit
```

---

## 🔒 SECURITY CONFIGURATIONS

### Firewall Setup
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### SSL Configuration
Uncomment and configure HTTPS in `nginx/nginx.conf`:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... other SSL configurations
}
```

---

## 📊 MONITORING

### Application Monitoring
- **Grafana**: http://your-domain.com:3001 (admin / your GRAFANA_PASSWORD)
- **Prometheus**: http://your-domain.com:9090
- **Application Logs**: `docker-compose logs -f fastapi`

### Health Checks
```bash
# Check all services health
curl http://your-domain.com/health

# Check individual services
docker-compose -f docker-compose.prod.yml exec fastapi curl http://localhost:8000/health
docker-compose -f docker-compose.prod.yml exec nextjs curl http://localhost:3000/api/health
```

---

## 🔄 MAINTENANCE

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose -f docker-compose.prod.yml up -d --build

# Clean up old images
docker image prune -f
```

### Backups
```bash
# Database backup
docker exec lumina_postgres pg_dump -U lumina_user lumina_os > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker exec -i lumina_postgres psql -U lumina_user lumina_os < backups/backup_file.sql
```

### Logs Management
```bash
# Rotate logs
sudo logrotate -f /etc/logrotate.conf

# Clear old logs (keep last 7 days)
find logs/ -name "*.log" -mtime +7 -delete
```

---

## 🚨 TROUBLESHOOTING

### Common Issues

#### 1. Services Not Starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs service_name

# Check resource usage
docker stats

# Restart service
docker-compose -f docker-compose.prod.yml restart service_name
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL status
docker exec lumina_postgres pg_isready -U lumina_user -d lumina_os

# Check Redis status
docker exec lumina_redis redis-cli ping
```

#### 3. SSL Certificate Issues
```bash
# Check certificate expiration
sudo certbot certificates

# Renew certificate
sudo certbot renew
```

---

## 📈 PERFORMANCE OPTIMIZATION

### Resource Limits
Adjust resource limits in `docker-compose.prod.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
```

### Database Optimization
```sql
-- Optimize PostgreSQL
CREATE INDEX CONCURRENTLY idx_leads_created_at ON leads(created_at);
ANALYZE;
```

---

## 🌐 DOMAIN CONFIGURATION

### DNS Records
```
A Record: your-domain.com -> YOUR_SERVER_IP
AAAA Record: your-domain.com -> YOUR_IPV6_ADDRESS (optional)
CNAME Record: www -> your-domain.com
```

### Subdomains (Optional)
```
api.your-domain.com -> FastAPI (via Nginx)
grafana.your-domain.com -> Grafana
prometheus.your-domain.com -> Prometheus
```

---

## 📞 SUPPORT

### Emergency Commands
```bash
# Stop all services
docker-compose -f docker-compose.prod.yml down

# Force stop (if stuck)
docker-compose -f docker-compose.prod.yml kill

# Remove all containers and volumes
docker-compose -f docker-compose.prod.yml down -v
```

### Contact Support
- Check logs first: `docker-compose logs -f`
- Monitor resource usage: `docker stats`
- Check health endpoints: `curl http://your-domain.com/health`

---

## ✅ DEPLOYMENT CHECKLIST

- [ ] Server requirements met
- [ ] Docker and Docker Compose installed
- [ ] Environment variables configured
- [ ] SSL certificates obtained (if using HTTPS)
- [ ] Firewall configured
- [ ] Application deployed successfully
- [ ] Database migrations completed
- [ ] Health checks passing
- [ ] Monitoring dashboards accessible
- [ ] Backup strategy implemented
- [ ] Log rotation configured
- [ ] Performance optimized

---

**Deployment Complete! 🎉**

Your LUMINA OS instance is now running in production mode.
Access your application at: https://your-domain.com

Monitor your system at: https://your-domain.com:3001 (Grafana)
