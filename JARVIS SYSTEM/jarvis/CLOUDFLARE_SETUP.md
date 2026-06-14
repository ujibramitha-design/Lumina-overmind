# Cloudflare Tunnels Setup for JARVIS

Complete guide to set up Cloudflare Tunnels for exposing JARVIS services securely without port forwarding or public IP.

## Prerequisites

- Cloudflare account (free tier works)
- Domain name configured in Cloudflare
- Local JARVIS services running

## Step 1: Install cloudflared

### Linux (Ubuntu/Debian)
```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared --version
```

### Linux (CentOS/RHEL)
```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm

# Install
sudo rpm -i cloudflared-linux-x86_64.rpm

# Verify installation
cloudflared --version
```

### Windows
```powershell
# Download from GitHub releases
# https://github.com/cloudflare/cloudflared/releases/latest

# Extract and add to PATH
# Or use winget
winget install --id Cloudflare.cloudflared
```

### macOS
```bash
# Using Homebrew
brew install cloudflared

# Verify installation
cloudflared --version
```

## Step 2: Authenticate with Cloudflare

```bash
# Login to Cloudflare
cloudflared tunnel login

# This will open a browser window
# Select your account and authorize
```

## Step 3: Create Tunnel

```bash
# Create a new tunnel
cloudflared tunnel create jarvis-tunnel

# This will output:
# - Tunnel ID (save this!)
# - Tunnel name
```

**Example Output:**
```
Tunnel ID: <TUNNEL_ID>
Tunnel Name: jarvis-tunnel
```

## Step 4: Configure Tunnel

### Option A: Use provided config.yml

Copy `jarvis/cloudflared-config.yml` and replace `<TUNNEL_ID>` with your actual tunnel ID:

```yaml
tunnel: <YOUR_TUNNEL_ID>
credentials-file: /root/.cloudflared/<YOUR_TUNNEL_ID>.json

ingress:
  - hostname: jarvis.yourdomain.com
    service: http://localhost:3000/telegram-webhook
    originRequest:
      noTLSVerify: true
  
  # ... other ingress rules
```

### Option B: Create config manually

```bash
# Create config directory
mkdir -p ~/.cloudflared

# Create config file
nano ~/.cloudflared/config.yml
```

Add the configuration from `jarvis/cloudflared-config.yml`.

## Step 5: Configure DNS Records

```bash
# Add DNS record for your domain
cloudflared tunnel route dns jarvis-tunnel jarvis.yourdomain.com

# Verify DNS record
cloudflared tunnel route dns jarvis-tunnel
```

## Step 6: Start the Tunnel

### Development Mode (Foreground)
```bash
# Start tunnel in foreground
cloudflared tunnel run --config ~/.cloudflared/config.yml jarvis-tunnel
```

### Production Mode (Background)
```bash
# Install as systemd service
sudo cloudflared service install

# Start service
sudo systemctl start cloudflared

# Enable auto-start on boot
sudo systemctl enable cloudflared

# Check status
sudo systemctl status cloudflared
```

### Using PM2
```bash
# Start with PM2
pm2 start cloudflared -- tunnel --config ~/.cloudflared/config.yml jarvis-tunnel

# Save PM2 configuration
pm2 save

# Setup PM2 startup
pm2 startup
```

### Using Docker
```bash
# Run cloudflared in Docker
docker run -d \
  --name cloudflared \
  -v ~/.cloudflared:/home/cloudflared/.cloudflared \
  cloudflare/cloudflared:latest \
  tunnel run --config /home/cloudflared/.cloudflared/config.yml jarvis-tunnel
```

## Step 7: Update Environment Variables

Update your `.env` file with the new Cloudflare domain:

```bash
# JARVIS Channels Configuration
JARVIS_TELEGRAM_WEBHOOK_URL=https://jarvis.yourdomain.com
JARVIS_TELEGRAM_WEBHOOK_PATH=/telegram-webhook
JARVIS_TELEGRAM_WEBHOOK_SECRET=your_secret_here

# Mobile App Configuration
API_BASE_URL=https://jarvis.yourdomain.com
```

## Step 8: Update Telegram Webhook

Update the Telegram bot configuration in `jarvis/channels/hub.js`:

```javascript
const config = {
  telegram: {
    enabled: true,
    token: process.env.JARVIS_TELEGRAM_BOT_TOKEN,
    webhookUrl: process.env.JARVIS_TELEGRAM_WEBHOOK_URL,
    webhookPath: process.env.JARVIS_TELEGRAM_WEBHOOK_PATH,
    webhookSecret: process.env.JARVIS_TELEGRAM_WEBHOOK_SECRET,
    webhookPort: 3000,
  }
};
```

## Step 9: Update Mobile App

Update `jarvis-mobile/services/auth.js`:

```javascript
const API_BASE_URL = 'https://jarvis.yourdomain.com';
```

## Step 10: Test the Setup

### Test Webhook
```bash
# Test webhook endpoint
curl -X POST https://jarvis.yourdomain.com/telegram-webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret_here" \
  -d '{"test": true}'
```

### Test API
```bash
# Test health check
curl https://jarvis.yourdomain.com/health

# Test mobile API
curl https://jarvis.yourdomain.com/api/jarvis-mobile/health \
  -H "X-Jarvis-Service-Token: your_token"
```

### Test WebSocket
```bash
# Test WebSocket connection
wscat -c https://jarvis.yourdomain.com/api/jarvis-mobile/ws
```

## Security Configuration

### Enable Cloudflare Access (Optional)

Add Cloudflare Access rules for additional security:

1. Go to Cloudflare Dashboard → Zero Trust → Access → Applications
2. Add new application
3. Configure authentication (Email, Google, etc.)
4. Add IP restrictions if needed

### Configure Firewall Rules

Add Cloudflare Firewall rules:

1. Go to Cloudflare Dashboard → Security → WAF
2. Create custom rules:
   - Block suspicious IPs
   - Rate limit webhook endpoints
   - Enable Bot Fight Mode

### Enable SSL/TLS

1. Go to Cloudflare Dashboard → SSL/TLS
2. Set mode to "Full" or "Full (strict)"
3. Configure minimum TLS version (1.2 or higher)

## Troubleshooting

### Tunnel Not Starting
```bash
# Check tunnel status
cloudflared tunnel info jarvis-tunnel

# Check logs
journalctl -u cloudflared -f

# Test configuration
cloudflared tunnel --config ~/.cloudflared/config.yml run --url http://localhost:3000
```

### Webhook Not Receiving Updates
```bash
# Check Telegram webhook info
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo

# Set webhook manually
curl -X POST https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook \
  -d "url=https://jarvis.yourdomain.com/telegram-webhook" \
  -d "secret_token=your_secret_here"
```

### DNS Not Propagating
```bash
# Check DNS propagation
dig jarvis.yourdomain.com

# Check Cloudflare DNS status
# Go to Cloudflare Dashboard → DNS
```

### Connection Refused
```bash
# Check if local service is running
curl http://localhost:3000/health

# Check firewall rules
sudo ufw status
sudo iptables -L
```

## Benefits of Cloudflare Tunnels

**Security:**
- No exposed ports on your machine
- Cloudflare DDoS protection
- SSL/TLS encryption
- IP whitelisting support

**Reliability:**
- Automatic failover
- Global edge network
- No port forwarding needed
- Works behind NAT/firewall

**Performance:**
- Global CDN
- HTTP/3 support
- Smart routing
- Compression

**Cost:**
- Free tier available
- No VPS needed
- No static IP required
- Low bandwidth costs

## Monitoring

### Cloudflare Dashboard
- Monitor tunnel status
- View analytics
- Check error rates
- Track bandwidth usage

### Local Monitoring
```bash
# Check cloudflared logs
tail -f /var/log/cloudflared.log

# Monitor with PM2
pm2 logs cloudflared

# Monitor with systemd
journalctl -u cloudflared -f
```

## Maintenance

### Update cloudflared
```bash
# Check for updates
cloudflared update

# Manual update
# Download latest version and replace binary
```

### Rotate Tunnel Credentials
```bash
# Delete old tunnel
cloudflared tunnel delete jarvis-tunnel

# Create new tunnel
cloudflared tunnel create jarvis-tunnel

# Update config.yml with new tunnel ID
# Update DNS records
```

## Production Checklist

- [ ] Cloudflare account configured
- [ ] Domain added to Cloudflare
- [ ] cloudflared installed
- [ ] Tunnel created and authenticated
- [ ] DNS records configured
- [ ] config.yml updated with tunnel ID
- [ ] Tunnel running in background
- [ ] Telegram webhook configured
- [ ] Mobile app API URL updated
- [ ] Security middleware enabled
- [ ] SSL/TLS configured
- [ ] Firewall rules configured
- [ ] Monitoring setup
- [ ] Backup configuration saved
- [ ] Documentation updated

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│              Cloudflare Edge Network                    │
│  (DDoS Protection, SSL, CDN, Global Routing)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS (443)
                     │
┌────────────────────▼────────────────────────────────────┐
│              Cloudflare Tunnel                          │
│  (Secure tunnel to local machine)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ cloudflared
                     │
┌────────────────────▼────────────────────────────────────┐
│              Local Machine                              │
│  ┌──────────────────────────────────────────────┐     │
│  │  JARVIS Services                              │     │
│  │  ├── Telegram Webhook (port 3000)           │     │
│  │  ├── Health Check (port 3001)               │     │
│  │  ├── Mobile API (port 8000)                 │     │
│  │  └── WebSocket (port 8000)                  │     │
│  └──────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Additional Resources

- [Cloudflare Tunnels Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [cloudflared GitHub](https://github.com/cloudflare/cloudflared)
- [Telegram Webhook Documentation](https://core.telegram.org/bots/api#setwebhook)
- [Cloudflare Zero Trust](https://developers.cloudflare.com/cloudflare-one/)

## Support

For issues or questions:
1. Check Cloudflare dashboard for tunnel status
2. Review cloudflared logs
3. Verify DNS configuration
4. Check local service status
5. Test with curl/wscat
