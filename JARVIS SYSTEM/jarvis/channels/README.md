# JARVIS Communication Channels

Persistent WhatsApp and Telegram integration for JARVIS AI Assistant with auto-reconnect and session persistence.

## 📁 Structure

```
jarvis_channels/
├── whatsapp/
│   └── client.js              # WhatsApp connection manager
├── telegram/
│   └── bot.js                 # Telegram connection manager
├── hub.js                     # Central communication hub
├── ecosystem.config.js        # PM2 configuration
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd jarvis_channels
npm init -y
npm install whatsapp-web.js qrcode-terminal node-telegram-bot-api dotenv
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your tokens
```

**Required Environment Variables:**

```bash
# Telegram Bot Token (get from @BotFather)
JARVIS_TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# WhatsApp (will generate QR code on first run)
JARVIS_WHATSAPP_ENABLED=true
```

### 3. Start with PM2 (Recommended for Production)

```bash
# Install PM2 globally
npm install -g pm2

# Start JARVIS hub
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on system boot
pm2 startup
```

### 4. Start Manually (Development)

```bash
node hub.js
```

## 📱 WhatsApp Setup

### First-Time Authentication

1. Start the hub with WhatsApp enabled
2. QR code will appear in terminal/logs
3. Scan QR code with JARVIS's dedicated WhatsApp number
4. Session is automatically saved to `./data/jarvis_sessions/whatsapp`

### Session Persistence

**How it works:**
- WhatsApp uses `LocalAuth` strategy from `whatsapp-web.js`
- Session data is saved to: `./data/jarvis_sessions/whatsapp/`
- Includes: authentication tokens, device info, session state
- On restart, hub automatically loads saved session
- No need to re-scan QR code after initial setup

**Session Files:**
```
data/jarvis_sessions/whatsapp/
├── jarvis-whatsapp/
│   ├── session.json          # Main session data
│   ├── session-xxx.data      # Session state
│   └── ...
```

**Auto-Reconnect Logic:**
- Exponential backoff: 5s, 10s, 20s, 40s, 80s...
- Max 10 reconnection attempts
- Automatic retry on disconnection
- Graceful handling of network issues

## 🤖 Telegram Setup

### Bot Creation

1. Open Telegram and search for @BotFather
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Add to `.env`: `JARVIS_TELEGRAM_BOT_TOKEN=your_token_here`

### Robust Error Handling

**Features:**
- Automatic polling restart on errors
- Catching polling errors and network issues
- Exponential backoff for reconnection
- Graceful shutdown handling

**Error Recovery:**
- Polling errors trigger automatic restart
- Network issues trigger reconnection
- Max 10 reconnection attempts
- Logs all errors for debugging

## 🔌 Central Hub

The `hub.js` file coordinates both channels:

**Features:**
- Unified message handling
- Platform-agnostic routing
- Health check server (port 3001)
- Graceful shutdown
- Agent connection interface

**Health Check Endpoint:**
```
GET http://localhost:3001/health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00Z",
  "channels": {
    "whatsapp": {
      "connected": true,
      "reconnectAttempts": 0,
      "sessionPath": "./data/jarvis_sessions/whatsapp"
    },
    "telegram": {
      "connected": true,
      "polling": true,
      "reconnectAttempts": 0
    }
  },
  "agent": {
    "connected": true
  }
}
```

## 🛠️ PM2 Process Management

### Commands

```bash
# Start
pm2 start ecosystem.config.js

# Status
pm2 status

# Logs
pm2 logs jarvis-hub

# Restart
pm2 restart jarvis-hub

# Stop
pm2 stop jarvis-hub

# Delete
pm2 delete jarvis-hub

# Monitor
pm2 monit
```

### Auto-Start on Boot

```bash
# Generate startup script
pm2 startup

# Save current processes
pm2 save
```

### Configuration

The `ecosystem.config.js` includes:
- Auto-restart on crash
- Memory limit (1GB)
- Log rotation
- Graceful shutdown
- Environment-specific configs

## 🔒 Security

### Service Token Authentication

JARVIS uses a dedicated service token for internal API access:

```bash
# Generate secure token
JARVIS_SERVICE_TOKEN=your_secure_token_here
```

**Security Features:**
- HMAC-SHA256 signature verification
- Constant-time token comparison
- Audit logging for all API calls
- IP whitelist support (optional)

## 📊 Monitoring

### Log Files

```
logs/
├── jarvis-hub-error.log      # Error logs
├── jarvis-hub-out.log        # Standard output
└── jarvis-hub-combined.log   # Combined logs
```

### Health Checks

```bash
# Check health
curl http://localhost:3001/health

# Monitor with PM2
pm2 monit
```

## 🔧 Troubleshooting

### WhatsApp Not Connecting

1. Check session directory exists: `./data/jarvis_sessions/whatsapp`
2. Delete session folder and re-scan QR code
3. Check network connectivity
4. Verify Puppeteer installation

### Telegram Not Polling

1. Verify bot token is correct
2. Check bot is not blocked by Telegram
3. Verify internet connection
4. Check logs for specific error messages

### Session Lost

**WhatsApp:**
```bash
# Delete session folder
rm -rf ./data/jarvis_sessions/whatsapp
# Restart hub to generate new QR code
pm2 restart jarvis-hub
```

**Telegram:**
- Telegram sessions are token-based
- No session persistence needed
- Just restart the hub

## 📝 Integration with JARVIS Agent

The hub connects to the JARVIS Agent through the `connectAgent()` method:

```javascript
const hub = new JarvisCommunicationHub(config);
const jarvisAgent = new JarvisAgent(config);

hub.connectAgent(jarvisAgent);
```

The agent must implement:
```javascript
{
  processMessage: async (messageData) => {
    // Process message and return response
    return response;
  }
}
```

## 🚀 Production Deployment

### Docker (Optional)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
CMD ["node", "hub.js"]
```

### Systemd Service (Alternative to PM2)

```ini
[Unit]
Description=JARVIS Communication Hub
After=network.target

[Service]
Type=simple
User=jarvis
WorkingDirectory=/path/to/jarvis_channels
ExecStart=/usr/bin/node hub.js
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📞 Support

For issues or questions:
1. Check logs: `pm2 logs jarvis-hub`
2. Verify environment variables
3. Check health endpoint: `curl http://localhost:3001/health`
4. Review session storage directory

## 🔄 Updates

To update the communication channels:

```bash
# Pull latest code
git pull

# Install new dependencies
npm install

# Restart PM2
pm2 restart jarvis-hub
```

## 📄 License

Part of Lumina Overmind Enterprise
