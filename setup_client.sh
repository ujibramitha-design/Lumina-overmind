#!/bin/bash

# =============================================================================
# LUMINA OS - MAGIC CLIENT INSTALLER
# White-Label Setup Script for New Clients
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
 ___ ____  ____ ____ ____    _  _ _ _     _   _    _    _   _    
|_ _|_  _|_  _|_  _|_  _|  | \/ | (_) |   | | |  | |  | | |   
 | |  | |  | |  | |  | | |\/| | | | |   | | |  | |  | | |   
 | |  | |  | | |  | |  |_| |  |_| |   | | |  | |  | | | |   
|___|_| |_|_|_|_|_|_|_|_|  |_|_|_|_|_|_|_|_|  |_|_|_  |_|_|_|
                                                                
    WHITE-LABEL CLIENT SETUP WIZARD
    AI-Powered Real Estate Intelligence Platform
EOF
echo -e "${NC}"

# Check if running as root (not recommended)
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}⚠️  WARNING: Running as root is not recommended!${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check system requirements
echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+ first.${NC}"
    echo "Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [[ $NODE_VERSION -lt 18 ]]; then
    echo -e "${RED}❌ Node.js version $NODE_VERSION is too old. Please install Node.js 18+${NC}"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ System requirements met!${NC}"

# Create installation directory
INSTALL_DIR="$PWD/lumina-os-client"
echo -e "${BLUE}📁 Creating installation directory: $INSTALL_DIR${NC}"
mkdir -p "$INSTALL_DIR"

# Function to validate Supabase URL
validate_supabase_url() {
    local url="$1"
    if [[ ! $url =~ ^postgresql://postgres:[^@]+@db\.[^:]+\.supabase\.co:[0-9]+/postgres$ ]]; then
        return 1
    fi
    return 0
}

# Function to validate email
validate_email() {
    local email="$1"
    if [[ ! $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        return 1
    fi
    return 0
}

# Function to validate password
validate_password() {
    local password="$1"
    if [[ ${#password} -lt 8 ]]; then
        return 1
    fi
    return 0
}

# Function to generate encryption key
generate_encryption_key() {
    python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
}

# Interactive Setup
echo -e "${PURPLE}🎯 Starting Interactive Setup...${NC}"
echo

# Step 1: Supabase Configuration
echo -e "${YELLOW}📊 STEP 1: Supabase Database Configuration${NC}"
echo "Please provide your Supabase database credentials:"
echo

# DATABASE_URL
while true; do
    read -p "🔗 DATABASE_URL (Connection Pooling): " DATABASE_URL
    if validate_supabase_url "$DATABASE_URL"; then
        break
    else
        echo -e "${RED}❌ Invalid Supabase URL format. Please use: postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres${NC}"
    fi
done

# DIRECT_URL
while true; do
    read -p "🔗 DIRECT_URL (Direct Connection): " DIRECT_URL
    if validate_supabase_url "$DIRECT_URL"; then
        break
    else
        echo -e "${RED}❌ Invalid Supabase URL format. Please use: postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres${NC}"
    fi
done

echo
echo -e "${YELLOW}👤 STEP 2: Super Admin Account Creation${NC}"
echo "Create your first administrator account:"
echo

# Admin Email
while true; do
    read -p "📧 Admin Email: " ADMIN_EMAIL
    if validate_email "$ADMIN_EMAIL"; then
        break
    else
        echo -e "${RED}❌ Invalid email format${NC}"
    fi
done

# Admin Password
while true; do
    read -s -p "🔐 Admin Password (min 8 chars): " ADMIN_PASSWORD
    echo
    if validate_password "$ADMIN_PASSWORD"; then
        break
    else
        echo -e "${RED}❌ Password must be at least 8 characters${NC}"
    fi
done

# Confirm Password
while true; do
    read -s -p "🔐 Confirm Admin Password: " ADMIN_PASSWORD_CONFIRM
    echo
    if [[ "$ADMIN_PASSWORD" == "$ADMIN_PASSWORD_CONFIRM" ]]; then
        break
    else
        echo -e "${RED}❌ Passwords do not match${NC}"
    fi
done

echo
echo -e "${YELLOW}🏷️  STEP 3: White-Label Branding Configuration${NC}"
echo "Customize your brand identity (press Enter to use defaults):"
echo

# App Name
read -p "📱 Application Name [LUMINA OS]: " APP_NAME
APP_NAME=${APP_NAME:-LUMINA OS}

# Company Name
read -p "🏢 Company Name [Your Company]: " COMPANY_NAME
COMPANY_NAME=${COMPANY_NAME:-Your Company}

# Primary Color
read -p "🎨 Primary Color [#ef4444]: " PRIMARY_COLOR
PRIMARY_COLOR=${PRIMARY_COLOR:-#ef4444}

# Secondary Color
read -p "🎨 Secondary Color [#1f2937]: " SECONDARY_COLOR
SECONDARY_COLOR=${SECONDARY_COLOR:-#1f2937}

# Accent Color
read -p "🎨 Accent Color [#10b981]: " ACCENT_COLOR
ACCENT_COLOR=${ACCENT_COLOR:-#10b981}

echo
echo -e "${YELLOW}🔐 STEP 4: Security Configuration${NC}"

# Generate Encryption Key
echo -e "${BLUE}🔑 Generating encryption key...${NC}"
ENCRYPTION_KEY=$(generate_encryption_key)
echo -e "${GREEN}✅ Encryption key generated successfully${NC}"

# License Key
read -p "🔓 License Key [DEMO-LICENSE]: " LICENSE_KEY
LICENSE_KEY=${LICENSE_KEY:-DEMO-LICENSE}

echo
echo -e "${YELLOW}📋 STEP 5: Configuration Summary${NC}"
echo "Please review your configuration:"
echo
echo -e "${CYAN}Database Configuration:${NC}"
echo "  DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "  DIRECT_URL: ${DIRECT_URL:0:30}..."
echo
echo -e "${CYAN}Admin Account:${NC}"
echo "  Email: $ADMIN_EMAIL"
echo "  Password: $(echo "$ADMIN_PASSWORD" | sed 's/./*/*****/')"
echo
echo -e "${CYAN}Branding:${NC}"
echo "  App Name: $APP_NAME"
echo "  Company: $COMPANY_NAME"
echo "  Primary Color: $PRIMARY_COLOR"
echo "  Secondary Color: $SECONDARY_COLOR"
echo "  Accent Color: $ACCENT_COLOR"
echo
echo -e "${CYAN}Security:${NC}"
echo "  Encryption Key: ${ENCRYPTION_KEY:0:20}..."
echo "  License Key: $LICENSE_KEY"
echo

read -p "Continue with installation? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Installation cancelled.${NC}"
    exit 1
fi

# Create .env file
echo -e "${BLUE}📝 Creating .env file...${NC}"
cat > "$INSTALL_DIR/.env" << EOF
# =============================================================================
# LUMINA OS - CLIENT CONFIGURATION
# Generated by Magic Installer on $(date)
# =============================================================================

# 🌐 Environment Configuration
ENVIRONMENT=production
DEBUG=false

# 🚀 Application URLs
FRONTEND_URL=https://your-domain.com
API_URL=https://your-domain.com/api
BACKEND_URL=https://your-domain.com/api
WEBHOOK_URL=https://your-domain.com/api/webhooks

# 🗄️ Database Configuration (Supabase)
DATABASE_URL=$DATABASE_URL
DIRECT_URL=$DIRECT_URL

# 🔐 Security Configuration
ENCRYPTION_KEY=$ENCRYPTION_KEY
LUMINA_LICENSE_KEY=$LICENSE_KEY

# 👤 Admin Account (Initial Setup)
ADMIN_EMAIL=$ADMIN_EMAIL
ADMIN_PASSWORD=$ADMIN_PASSWORD

# 🏷️ White-Label Branding
NEXT_PUBLIC_APP_NAME="$APP_NAME"
NEXT_PUBLIC_COMPANY_NAME="$COMPANY_NAME"
NEXT_PUBLIC_PRIMARY_COLOR="$PRIMARY_COLOR"
NEXT_PUBLIC_SECONDARY_COLOR="$SECONDARY_COLOR"
NEXT_PUBLIC_ACCENT_COLOR="$ACCENT_COLOR"
NEXT_PUBLIC_APP_TITLE="$APP_NAME - AI Real Estate Intelligence"
NEXT_PUBLIC_APP_DESCRIPTION="AI-powered real estate lead generation and intelligence platform"
NEXT_PUBLIC_APP_AUTHOR="$COMPANY_NAME"
NEXT_PUBLIC_SUPPORT_EMAIL="support@$(echo "$COMPANY_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g').com"
NEXT_PUBLIC_ENABLE_WHITE_LABEL=true
NEXT_PUBLIC_SHOW_BRANDING=true
NEXT_PUBLIC_ALLOW_CUSTOM_LOGO=true

# 🤖 AI Services (Configure as needed)
GEMINI_API_KEY=
EXA_API_KEY=
FIRECRAWL_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# 📱 Communication
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=

# 💰 Budget Controls
AI_DAILY_BUDGET_USD=50.0
AI_MONTHLY_BUDGET_USD=1500.0
WHATSAPP_DAILY_BUDGET_USD=20.0
WHATSAPP_MONTHLY_BUDGET_USD=600.0

# 🌐 CORS Configuration
CORS_ORIGINS=["https://your-domain.com"]
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS=["*"]

# 📊 Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot_log.txt
EOF

echo -e "${GREEN}✅ .env file created successfully${NC}"

# Create installation script
echo -e "${BLUE}📜 Creating installation scripts...${NC}"

# Install script
cat > "$INSTALL_DIR/install.sh" << 'EOF'
#!/bin/bash

# LUMINA OS - Installation Script
set -e

echo "🚀 Installing LUMINA OS..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "🐳 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

echo "🗄️ Running database migrations..."
docker-compose exec backend npx prisma migrate deploy
docker-compose exec backend npx prisma db push

echo "👤 Creating admin user..."
docker-compose exec backend python -c "
import asyncio
import sys
sys.path.append('/app')
from prisma import Client

async def create_admin():
    db = Client()
    try:
        # Check if admin already exists
        existing = db.user.find_first(where={'email': os.getenv('ADMIN_EMAIL')})
        if existing:
            print('Admin user already exists')
            return
        
        # Create admin user
        admin = db.user.create({
            'email': os.getenv('ADMIN_EMAIL'),
            'username': os.getenv('ADMIN_EMAIL').split('@')[0],
            'password': os.getenv('ADMIN_PASSWORD'),  # Will be hashed by the app
            'firstName': 'Super',
            'lastName': 'Admin',
            'role': 'SUPER_ADMIN',
            'isActive': True,
            'permissions': ['ALL']
        })
        print(f'✅ Admin user created: {admin.email}')
    except Exception as e:
        print(f'❌ Failed to create admin: {e}')
    finally:
        await db.disconnect()

asyncio.run(create_admin())
"

echo "🎉 Installation completed!"
echo ""
echo "🌐 Access your LUMINA OS instance:"
echo "   Frontend: http://localhost:3000"
echo "   API: http://localhost:8000"
echo "   Admin Email: $ADMIN_EMAIL"
echo ""
echo "📚 Next steps:"
echo "   1. Configure your AI service API keys"
echo "   2. Set up your domain and SSL certificates"
echo "   3. Configure backup and monitoring"
echo ""
echo "🔐 For support, contact: support@lumina.tech"
EOF

chmod +x "$INSTALL_DIR/install.sh"

# Update script
cat > "$INSTALL_DIR/update.sh" << 'EOF'
#!/bin/bash

# LUMINA OS - Update Script
set -e

echo "🔄 Updating LUMINA OS..."

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Rebuild and restart services
echo "🐳 Rebuilding Docker images..."
docker-compose build

echo "🔄 Restarting services..."
docker-compose up -d --force-recreate

echo "🗄️ Running database migrations..."
docker-compose exec backend npx prisma migrate deploy

echo "✅ Update completed!"
EOF

chmod +x "$INSTALL_DIR/update.sh"

# Backup script
cat > "$INSTALL_DIR/backup.sh" << 'EOF'
#!/bin/bash

# LUMINA OS - Backup Script
set -e

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup: $BACKUP_DIR"

# Database backup
echo "🗄️ Backing up database..."
docker-compose exec -T postgres pg_dump -U postgres postgres > "$BACKUP_DIR/database.sql"

# Configuration backup
echo "📝 Backing up configuration..."
cp .env "$BACKUP_DIR/.env.backup"

# Files backup
echo "📁 Backing up important files..."
cp -r logs "$BACKUP_DIR/"
cp -r data "$BACKUP_DIR/" 2>/dev/null || true

echo "✅ Backup completed: $BACKUP_DIR"
EOF

chmod +x "$INSTALL_DIR/backup.sh"

# Docker Compose file
echo -e "${BLUE}🐳 Creating docker-compose.yml...${NC}"
cat > "$INSTALL_DIR/docker-compose.yml" << EOF
version: '3.8'

services:
  # PostgreSQL Database (Using Supabase - this is for local development only)
  postgres:
    image: postgres:15-alpine
    container_name: lumina_postgres
    environment:
      POSTGRES_DB: lumina_production
      POSTGRES_USER: lumina_user
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD:-lumina_password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - lumina_network
    restart: unless-stopped
    profiles:
      - local

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: lumina_redis
    command: redis-server --appendonly yes --requirepass \${REDIS_PASSWORD:-lumina_redis}
    volumes:
      - redis_data:/data
    networks:
      - lumina_network
    restart: unless-stopped

  # Backend API
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: lumina_backend
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - DIRECT_URL=\${DIRECT_URL}
      - ENCRYPTION_KEY=\${ENCRYPTION_KEY}
      - REDIS_URL=redis://:\${REDIS_PASSWORD:-lumina_redis}@redis:6379/0
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./backups:/app/backups
    ports:
      - "8000:8000"
    networks:
      - lumina_network
    depends_on:
      - redis
    restart: unless-stopped

  # Frontend
  frontend:
    build:
      context: ./dashboard
      dockerfile: ../Dockerfile.frontend
    container_name: lumina_frontend
    environment:
      - NEXT_PUBLIC_APP_NAME=\${NEXT_PUBLIC_APP_NAME}
      - NEXT_PUBLIC_COMPANY_NAME=\${NEXT_PUBLIC_COMPANY_NAME}
      - NEXT_PUBLIC_PRIMARY_COLOR=\${NEXT_PUBLIC_PRIMARY_COLOR}
      - NEXT_PUBLIC_SECONDARY_COLOR=\${NEXT_PUBLIC_SECONDARY_COLOR}
      - NEXT_PUBLIC_ACCENT_COLOR=\${NEXT_PUBLIC_ACCENT_COLOR}
    ports:
      - "3000:3000"
    networks:
      - lumina_network
    depends_on:
      - backend
    restart: unless-stopped

  # Celery Worker
  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: lumina_celery_worker
    command: celery -A tasks.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - DIRECT_URL=\${DIRECT_URL}
      - ENCRYPTION_KEY=\${ENCRYPTION_KEY}
      - REDIS_URL=redis://:\${REDIS_PASSWORD:-lumina_redis}@redis:6379/0
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - lumina_network
    depends_on:
      - redis
      - backend
    restart: unless-stopped

  # Celery Beat (Scheduler)
  celery_beat:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: lumina_celery_beat
    command: celery -A tasks.celery_app beat --loglevel=info
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - DIRECT_URL=\${DIRECT_URL}
      - ENCRYPTION_KEY=\${ENCRYPTION_KEY}
      - REDIS_URL=redis://:\${REDIS_PASSWORD:-lumina_redis}@redis:6379/0
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    networks:
      - lumina_network
    depends_on:
      - redis
      - backend
    restart: unless-stopped

networks:
  lumina_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
EOF

# README file
echo -e "${BLUE}📖 Creating README.md...${NC}"
cat > "$INSTALL_DIR/README.md" << EOF
# $APP_NAME

$APP_NAME - AI-Powered Real Estate Intelligence Platform

## 🚀 Quick Start

1. **Run the installer:**
   \`\`\`bash
   ./install.sh
   \`\`\`

2. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Admin Email: $ADMIN_EMAIL

## 📚 Documentation

- [Configuration Guide](./docs/configuration.md)
- [API Documentation](./docs/api.md)
- [Deployment Guide](./docs/deployment.md)

## 🔧 Management Scripts

- \`./install.sh\` - Initial installation
- \`./update.sh\` - Update to latest version
- \`./backup.sh\` - Create backup

## 🆘 Support

For support, contact: support@$(echo "$COMPANY_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g').com

## 📄 License

License Key: $LICENSE_KEY
EOF

echo -e "${GREEN}✅ Installation files created successfully!${NC}"

# Create docs directory
mkdir -p "$INSTALL_DIR/docs"

echo -e "${BLUE}📚 Creating documentation...${NC}"

# Configuration guide
cat > "$INSTALL_DIR/docs/configuration.md" << 'EOF'
# Configuration Guide

## Environment Variables

### Database Configuration
- `DATABASE_URL`: Supabase connection pooling URL
- `DIRECT_URL`: Supabase direct connection URL

### Branding Configuration
- `NEXT_PUBLIC_APP_NAME`: Application name
- `NEXT_PUBLIC_COMPANY_NAME`: Company name
- `NEXT_PUBLIC_PRIMARY_COLOR`: Primary brand color
- `NEXT_PUBLIC_SECONDARY_COLOR`: Secondary brand color
- `NEXT_PUBLIC_ACCENT_COLOR`: Accent color

### Security Configuration
- `ENCRYPTION_KEY`: Data encryption key
- `LUMINA_LICENSE_KEY`: License validation key

### AI Services
- `GEMINI_API_KEY`: Google Gemini API key
- `EXA_API_KEY`: Exa search API key
- `FIRECRAWL_API_KEY`: Firecrawl API key

## White-Label Customization

### Logo Customization
1. Upload your logo to \`public/logo.png\`
2. Set \`NEXT_PUBLIC_ALLOW_CUSTOM_LOGO=true\`
3. Update branding in the admin panel

### Color Customization
Update the color variables in your environment:
- Primary: Main brand color
- Secondary: Secondary brand color  
- Accent: Highlight color

### Domain Configuration
1. Update \`FRONTEND_URL\` and \`API_URL\`
2. Configure SSL certificates
3. Update CORS origins
EOF

# API documentation
cat > "$INSTALL_DIR/docs/api.md" << 'EOF'
# API Documentation

## Authentication

All API endpoints require authentication using JWT tokens.

### Login
\`\`\`bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "password"
}
\`\`\`

## Classified Vault

### Create API Key
\`\`\`bash
POST /api/config-vault/keys
Authorization: Bearer <token>
Content-Type: application/json

{
  "key_name": "OPENAI_API_KEY",
  "key_value": "your-api-key",
  "description": "OpenAI API key for AI processing",
  "category": "API_KEYS"
}
\`\`\`

### Get API Keys
\`\`\`bash
GET /api/config-vault/keys
Authorization: Bearer <token>
\`\`\`

## Lead Management

### Create Lead
\`\`\`bash
POST /api/leads
Authorization: Bearer <token>
Content-Type: application/json

{
  "business_name": "Example Corp",
  "contact": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "project_id": "project-uuid"
}
\`\`\`

### Get Leads
\`\`\`bash
GET /api/leads
Authorization: Bearer <token>
\`\`\`
EOF

# Deployment guide
cat > "$INSTALL_DIR/docs/deployment.md" << 'EOF'
# Deployment Guide

## Production Deployment

### Prerequisites
- Docker and Docker Compose
- Supabase database
- SSL certificate
- Domain name

### Steps

1. **Prepare Environment**
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

2. **Deploy Services**
   \`\`\`bash
   docker-compose -f docker-compose.production.yml up -d
   \`\`\`

3. **Configure Nginx**
   \`\`\`bash
   # Copy nginx configuration
   sudo cp nginx/lumina.conf /etc/nginx/sites-available/
   sudo ln -s /etc/nginx/sites-available/lumina.conf /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   \`\`\`

4. **Setup SSL**
   \`\`\`bash
   sudo certbot --nginx -d yourdomain.com
   \`\`\`

## Monitoring

### Health Checks
- Frontend: http://localhost:3000/health
- API: http://localhost:8000/health
- Database: Check connection logs

### Logs
\`\`\`bash
docker-compose logs -f backend
docker-compose logs -f frontend
\`\`\`

## Backup Strategy

### Automated Backups
\`\`\`bash
# Add to crontab
0 2 * * * /path/to/lumina-os/backup.sh
\`\`\`

### Manual Backup
\`\`\`bash
./backup.sh
\`\`\`
EOF

echo -e "${GREEN}✅ Documentation created successfully!${NC}"

echo
echo -e "${PURPLE}🎉 INSTALLATION COMPLETED!${NC}"
echo
echo -e "${CYAN}Your LUMINA OS client has been configured and is ready for deployment!${NC}"
echo
echo -e "${YELLOW}📁 Installation Directory:${NC} $INSTALL_DIR"
echo -e "${YELLOW}📝 Configuration File:${NC} $INSTALL_DIR/.env"
echo -e "${YELLOW}🔧 Installation Script:${NC} $INSTALL_DIR/install.sh"
echo -e "${YELLOW}📚 Documentation:${NC} $INSTALL_DIR/docs/"
echo
echo -e "${BLUE}🚀 Next Steps:${NC}"
echo "1. cd $INSTALL_DIR"
echo "2. ./install.sh"
echo "3. Access your application at http://localhost:3000"
echo "4. Login with: $ADMIN_EMAIL"
echo
echo -e "${GREEN}💰 Ready for commercial deployment at \$50,000 per client!${NC}"
echo
echo -e "${CYAN}For support, contact: support@lumina.tech${NC}"
