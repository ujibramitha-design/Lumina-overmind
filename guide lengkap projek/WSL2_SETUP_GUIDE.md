# WSL2 Setup Guide for Lumina Overmind

## Why WSL2?

WSL2 (Windows Subsystem for Linux 2) provides:
- Native Linux environment on Windows
- No Windows file locking issues
- Better database performance
- Closer to production environment (Linux)
- Ability to run all services (PostgreSQL, Redis, etc.) without issues

## Prerequisites

- Windows 10 version 2004 or higher (Build 19041 or higher)
- Windows 11 (any version)
- Administrator privileges

## Installation Steps

### Step 1: Enable WSL2

Open PowerShell as Administrator and run:

```powershell
# Enable WSL
wsl --install

# Or enable specific features manually
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### Step 2: Restart Computer

Restart your computer to apply changes.

### Step 3: Install Linux Distribution

After restart, run:

```powershell
# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu (recommended)
wsl --install -d Ubuntu-22.04

# Or list available distributions
wsl --list --online
```

### Step 4: Complete Ubuntu Setup

After installation, Ubuntu will open automatically. Complete the setup:
1. Create username and password
2. Update system:

```bash
sudo apt update && sudo apt upgrade -y
```

## Installing Dependencies for Lumina Overmind

### Step 5: Install Python 3.10+

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip git -y
```

### Step 6: Install Node.js 18+

```bash
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node --version
npm --version
```

### Step 7: Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL service
sudo service postgresql start

# Set up PostgreSQL user
sudo -u postgres createuser --interactive
# Enter your WSL2 username when prompted

sudo -u postgres psql
# In psql:
ALTER USER your_username WITH PASSWORD 'your_password';
\q
```

### Step 8: Install Optional Services

```bash
# Redis (if needed for Celery)
sudo apt install redis-server -y
sudo service redis-server start

# Docker (optional, for containerized services)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

## Clone Lumina Overmind in WSL2

### Step 9: Navigate to WSL2 Home

```bash
cd ~
```

### Step 10: Clone Repository

```bash
# Option 1: Clone from GitHub
git clone https://github.com/ujibramitha-design/Lumina-overmind.git

# Option 2: Clone from GitLab
git clone https://gitlab.com/uji.bramitha/lumina-overmind.git

# Enter directory
cd Lumina-overmind
```

### Step 11: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Generate Prisma client
prisma generate
```

### Step 12: Setup Frontend Environment

```bash
cd dashboard

# Install Node.js dependencies
npm install

# Return to root
cd ..
```

### Step 13: Configure Environment

```bash
# Copy environment example
cp .env.example .env

# Edit .env with your settings
nano .env
```

Update database connection in `.env`:
```
DATABASE_URL="postgresql://your_username:your_password@localhost:5432/lumina_db"
```

### Step 14: Run Database Migrations

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
prisma migrate dev

# Or push schema
prisma db push
```

## Running Lumina Overmind in WSL2

### Start Backend

```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend

```bash
# In new terminal
cd ~/Lumina-overmind/dashboard
npm run dev
```

## Accessing from Windows

### Access WSL2 from Windows

WSL2 files are accessible from Windows at:
```
\\wsl$\Ubuntu-22.04\home\your_username\Lumina-overmind
```

### Access Windows from WSL2

Windows files are accessible from WSL2 at:
```bash
cd /mnt/c/Program\ Project\ APK\ WEB\ CRM/Belajar_Android/lumina-overmind
```

### Network Access

Services running in WSL2 are accessible from Windows at:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Troubleshooting

### WSL2 Not Starting

```powershell
# Restart WSL
wsl --shutdown
wsl
```

### Database Connection Issues

```bash
# Check PostgreSQL status
sudo service postgresql status

# Start PostgreSQL
sudo service postgresql start

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER ~/Lumina-overmind
```

## Performance Optimization

### Increase WSL2 Memory

Create `%USERPROFILE%\.wslconfig` on Windows:

```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

### Enable Systemd (Ubuntu 22.04+)

```bash
# Edit WSL config
sudo nano /etc/wsl.conf

# Add:
[boot]
systemd=true

# Restart WSL
wsl --shutdown
```

## Backup and Migration

### Backup WSL2

```powershell
# Export WSL distribution
wsl --export Ubuntu-22.04 C:\backup\ubuntu-backup.tar
```

### Restore WSL2

```powershell
# Import WSL distribution
wsl --import Ubuntu-22.04 C:\WSL\Ubuntu C:\backup\ubuntu-backup.tar
```

## VS Code Integration

### Install VS Code Server in WSL2

```bash
# Install VS Code
code .

# Or install VS Code server
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
sudo mv code /usr/local/bin/
```

### Recommended VS Code Extensions

- Remote - WSL
- Python
- Pylance
- ESLint
- Prettier
- Prisma
- Docker

## Summary

**Time Required**: 30-45 minutes
**Difficulty**: Medium
**Benefits**:
- No Windows file locking issues
- Better database performance
- Linux development environment
- Closer to production

**Next Steps After Setup**:
1. Test database connection
2. Run backend server
3. Run frontend server
4. Verify all services work correctly
5. Update development workflow to use WSL2
