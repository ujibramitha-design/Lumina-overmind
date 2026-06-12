# 🤖 DOOM SENTINEL - Digital Overwatch & Operations Machine
## Military-grade AI Assistant with Proactive Monitoring

---

## 🎯 **OVERVIEW**

DOOM SENTINEL adalah asisten AI sekaligus sistem monitoring militer yang beroperasi di dua jalur komando: WhatsApp API dan Telegram Bot API.

**Nama Sandi:** DOOM (Digital Overwatch & Operations Machine)

---

## 🚀 **QUICK SETUP**

### **1. Install Dependencies**
```bash
# Install DOOM Sentinel specific requirements
pip install -r requirements_doom.txt

# Install main project requirements (if not already installed)
pip install -r requirements.txt
```

### **2. Configure Environment Variables**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

### **3. Required Environment Variables**
```bash
# 🤖 DOOM SENTINEL Configuration
ADMIN_WA_NUMBER=+6281234567890,+6281234567891
ADMIN_TELE_ID=123456789,987654321

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Twilio WhatsApp Gateway
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886

# Database (already configured in main .env)
DATABASE_URL=postgresql://lumina_user:password@localhost:5432/lumina_os
```

### **4. Start DOOM Sentinel**
```bash
# Run DOOM Sentinel
python core_modules/doom_sentinel/main.py
```

---

## 🛡️ **SECURITY FEATURES**

### **Multi-Layer Security**
- **Admin ID Validation**: Hanya nomor Jenderal yang diizinkan
- **Role-Based Access Control (RBAC)**: Akses berdasarkan peran
- **Session Management**: Tracking aktivitas pengguna
- **Command Permission**: Verifikasi perintah sebelum eksekusi

### **Access Levels**
- **ADMIN**: Jenderal/Lead System Architect (Akses penuh)
- **GUEST**: Customer Service mode (Akses terbatas)
- **BLOCKED**: Akses ditolak

---

## 🤖 **DUAL PERSONALITY SYSTEM**

### **Admin Mode (Jenderal)**
```
🎖️ DOOM COMMAND SYSTEM ONLINE

Commands:
• /status - System health report
• /deploy_scout <location> - Deploy AI Hunter
• /approve_ads <campaign_id> - Approve ad campaign
• /system_control - Advanced system controls
• Natural language commands supported
```

### **Guest Mode (Customer Service)**
```
👋 Virtual Assistant

Capabilities:
• Property information
• Pricing inquiries
• Location details
• General customer service
• No system commands access
```

---

## 🚨 **PROACTIVE MONITORING**

### **Automatic Alerts**
DOOM otomatis mengirim alert jika:
- Server down/database crash
- Traffic spike (>50 leads/hour)
- API usage approaching limits
- High CPU/Memory/Disk usage
- System errors detected

### **Alert Channels**
- **Telegram**: Real-time alerts to admin
- **WhatsApp**: Backup alert channel
- **Cooldown**: 5 minutes between same alerts

---

## 📊 **MONITORING METRICS**

### **System Health**
```python
{
    'server_health': '🟢 HEALTHY',
    'database_status': '🟢 ONLINE',
    'leads_today': 127,
    'budget_remaining': 'Rp 45.000.000',
    'active_agents': 28,
    'total_agents': 34,
    'uptime': '2d 14h 32m'
}
```

### **Alert Thresholds**
- CPU Usage: >80%
- Memory Usage: >85%
- Disk Usage: >90%
- Leads per hour: >50
- API Usage: >80%

---

## 🔧 **COMMAND REFERENCE**

### **Admin Commands**
```bash
# System Status
/status

# Deploy AI Hunter
/deploy_scout Serang
/deploy_scout "Jakarta Selatan"

# Approve Ads
/approve_ads campaign_123

# System Control
/system_control

# Natural Language
"Berikan saya statistik sistem"
"Deploy hunter agent ke Tangerang"
"Cek kesehatan server"
```

### **Guest Commands**
```bash
# Customer Service
"Apakah ada properti di Serang?"
"Berapa harga rumah subsidi?"
"Bisa bantu info KPR?"
" Lokasi proyek mana saja?"
```

---

## 🏗️ **ARCHITECTURE**

### **Core Components**
```
core_modules/doom_sentinel/
├── __init__.py              # Package initialization
├── main.py                  # Main application entry point
├── security_middleware.py   # Authentication & authorization
├── telegram_gateway.py      # Telegram bot integration
├── whatsapp_gateway.py     # WhatsApp API integration
├── rbac_manager.py         # Role-based access control
└── alert_system.py          # Proactive monitoring
```

### **Data Flow**
```
User Message → Security Middleware → RBAC Manager → Response
                ↓
        Alert System (monitoring)
                ↓
        Telegram/WhatsApp Gateway → User
```

---

## 🔌 **API INTEGRATION**

### **WhatsApp Webhook**
```python
POST /webhook/whatsapp
Content-Type: application/json

{
    "From": "whatsapp:+6281234567890",
    "Body": "/status",
    "MessageSid": "msg_123456"
}
```

### **Telegram Bot Commands**
```python
# Command handlers registered
/start          # Welcome message
/help           # Help information
/status         # System status
/deploy_scout   # Deploy hunter
/approve_ads    # Approve campaigns
/system_control # Control panel
```

---

## 🛠️ **TROUBLESHOOTING**

### **Common Issues**

#### **1. Telegram Bot Not Responding**
```bash
# Check bot token
echo $TELEGRAM_BOT_TOKEN

# Verify bot is running
python -c "import telegram; print(telegram.Bot(token='YOUR_TOKEN').get_me())"
```

#### **2. WhatsApp Messages Not Sending**
```bash
# Check Twilio credentials
echo $TWILIO_ACCOUNT_SID
echo $TWILIO_AUTH_TOKEN

# Test WhatsApp connection
python -c "from twilio.rest import Client; print('Connected')"
```

#### **3. Admin Access Not Working**
```bash
# Check admin IDs
echo $ADMIN_WA_NUMBER
echo $ADMIN_TELE_ID

# Verify format (comma-separated, no spaces)
```

#### **4. Database Connection Issues**
```bash
# Test database connection
python -c "from core_modules.db_manager_postgres import postgres_db_manager; print(postgres_db_manager.health_check())"
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with debug output
python core_modules/doom_sentinel/main.py
```

---

## 📈 **PERFORMANCE OPTIMIZATION**

### **Message Queue**
- **Bulk Messages**: Rate-limited to 1 msg/second
- **Queue Management**: Async processing
- **Error Handling**: Retry mechanism

### **Memory Management**
- **Session Cleanup**: Automatic expired session removal
- **Alert History**: 24-hour retention
- **Monitoring**: 60-second intervals

### **Rate Limiting**
- **Commands**: 100 commands/hour per user
- **Alerts**: 5-minute cooldown
- **API Calls**: Respect platform limits

---

## 🔐 **SECURITY BEST PRACTICES**

### **Environment Variables**
```bash
# Never commit .env to version control
echo ".env" >> .gitignore

# Use different keys for dev/prod
# Rotate API keys regularly
# Monitor usage and costs
```

### **Access Control**
```bash
# Limit admin numbers to trusted personnel
# Use secure communication channels
# Monitor session activity
# Implement IP restrictions if needed
```

### **Data Protection**
```bash
# Encrypt sensitive data
# Use HTTPS for webhooks
# Validate all inputs
# Log all security events
```

---

## 🚀 **DEPLOYMENT**

### **Development**
```bash
# Run locally
python core_modules/doom_sentinel/main.py

# With auto-reload
uvicorn core_modules.doom_sentinel.main:app --reload
```

### **Production**
```bash
# Using Docker
docker-compose up doom-sentinel

# Using systemd
sudo systemctl start doom-sentinel
sudo systemctl enable doom-sentinel
```

### **Monitoring**
```bash
# Check status
curl http://localhost:8000/health

# View logs
tail -f logs/doom_sentinel.log

# Monitor resources
htop
```

---

## 📞 **SUPPORT**

### **Documentation**
- **API Docs**: http://localhost:8000/docs
- **System Health**: http://localhost:8000/health
- **Alert History**: Available in system

### **Emergency Contacts**
- **System Admin**: Lead System Architect
- **Technical Support**: DevOps Team
- **Security Issues**: Security Team

---

## 🎯 **MISSION STATUS**

DOOM SENTINEL is designed to be the ultimate AI assistant and monitoring system for your real estate business. With military-grade security, proactive monitoring, and dual-channel communication, DOOM ensures your system remains operational and secure 24/7.

**Status:** ✅ PRODUCTION READY  
**Security:** 🛡️ MILITARY GRADE  
**Monitoring:** 🚨 PROACTIVE  
**Support:** 🤖 24/7 AI ASSISTANT

---

*DOOM SENTINEL - Your Digital Overwatch & Operations Machine* 🤖
