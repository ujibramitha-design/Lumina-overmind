/**
 * JARVIS Central Communication Hub
 * =================================
 * 
 * Central hub that initializes both WhatsApp and Telegram bots
 * and connects them to the JARVIS Agent logic
 */

const JarvisWhatsAppClient = require('./whatsapp/client');
const JarvisTelegramBot = require('./telegram/bot');
const http = require('http');

class JarvisCommunicationHub {
  constructor(config) {
    this.config = config;
    this.whatsapp = null;
    this.telegram = null;
    this.isRunning = false;
    this.jarvisAgent = null;
    
    // Health check server
    this.healthCheckPort = config.healthCheckPort || 3001;
    this.healthCheckServer = null;
  }

  /**
   * Initialize all communication channels
   */
  async initialize() {
    console.log('🔌 Initializing JARVIS Communication Hub...');
    
    // Initialize WhatsApp
    if (this.config.whatsapp.enabled) {
      console.log('📱 Setting up WhatsApp...');
      this.whatsapp = new JarvisWhatsAppClient({
        sessionPath: this.config.whatsapp.sessionPath
      });
      this.whatsapp.initialize();
      this.whatsapp.onMessage(this.handleIncomingMessage.bind(this));
    }

    // Initialize Telegram
    if (this.config.telegram.enabled) {
      console.log('🤖 Setting up Telegram...');
      this.telegram = new JarvisTelegramBot({
        token: this.config.telegram.token
      });
      this.telegram.initialize();
      this.telegram.onMessage(this.handleIncomingMessage.bind(this));
    }

    console.log('✅ Communication Hub initialized');
  }

  /**
   * Start all communication channels
   */
  async start() {
    console.log('🚀 Starting JARVIS Communication Hub...');
    
    // Start WhatsApp
    if (this.whatsapp) {
      await this.whatsapp.start();
    }

    // Start Telegram
    if (this.telegram) {
      await this.telegram.startPolling();
    }

    // Start health check server
    this.startHealthCheckServer();

    this.isRunning = true;
    console.log('✅ JARVIS Communication Hub is RUNNING');
    console.log('📊 Status:');
    console.log(`   WhatsApp: ${this.whatsapp ? this.whatsapp.getStatus().connected : 'Disabled'}`);
    console.log(`   Telegram: ${this.telegram ? this.telegram.getStatus().connected : 'Disabled'}`);
  }

  /**
   * Handle incoming message from any platform
   */
  async handleIncomingMessage(messageData) {
    try {
      console.log(`📩 [${messageData.platform.toUpperCase()}] Message from ${messageData.from.name}: ${messageData.message}`);
      
      // Route to JARVIS Agent
      if (this.jarvisAgent) {
        const response = await this.jarvisAgent.processMessage(messageData);
        
        // Send response back to the same platform
        await this.sendResponse(messageData.platform, messageData.from.id, response);
      } else {
        console.warn('⚠️ JARVIS Agent not connected. Message not processed.');
        await this.sendResponse(
          messageData.platform,
          messageData.from.id,
          'JARVIS Agent is currently initializing. Please try again in a moment.'
        );
      }
    } catch (error) {
      console.error('❌ Error handling message:', error.message);
    }
  }

  /**
   * Send response to specific platform
   */
  async sendResponse(platform, to, message) {
    try {
      switch (platform) {
        case 'whatsapp':
          if (this.whatsapp) {
            await this.whatsapp.sendMessage(to, message);
          }
          break;
        case 'telegram':
          if (this.telegram) {
            await this.telegram.sendMessage(to, message);
          }
          break;
        default:
          console.error(`❌ Unknown platform: ${platform}`);
      }
    } catch (error) {
      console.error(`❌ Error sending response to ${platform}:`, error.message);
    }
  }

  /**
   * Send proactive message to specific platform
   */
  async sendProactiveMessage(platform, to, message) {
    console.log(`📤 [PROACTIVE] Sending to ${platform} (${to}): ${message}`);
    await this.sendResponse(platform, to, message);
  }

  /**
   * Broadcast message to all platforms
   */
  async broadcast(message) {
    console.log('📡 Broadcasting message to all platforms...');
    
    // Send to Telegram (if configured with broadcast list)
    if (this.telegram && this.config.telegram.broadcastChatId) {
      await this.telegram.sendMessage(this.config.telegram.broadcastChatId, message);
    }
    
    // WhatsApp broadcast would require a group or broadcast list
    // This can be extended as needed
  }

  /**
   * Connect JARVIS Agent
   */
  connectAgent(agent) {
    this.jarvisAgent = agent;
    console.log('🤖 JARVIS Agent connected to Communication Hub');
  }

  /**
   * Start health check server
   */
  startHealthCheckServer() {
    this.healthCheckServer = http.createServer((req, res) => {
      if (req.url === '/health') {
        const status = {
          status: 'ok',
          timestamp: new Date().toISOString(),
          channels: {
            whatsapp: this.whatsapp ? this.whatsapp.getStatus() : { connected: false, disabled: true },
            telegram: this.telegram ? this.telegram.getStatus() : { connected: false, disabled: true }
          },
          agent: this.jarvisAgent ? { connected: true } : { connected: false }
        };
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(status, null, 2));
      } else {
        res.writeHead(404);
        res.end('Not Found');
      }
    });

    this.healthCheckServer.listen(this.healthCheckPort, () => {
      console.log(`🏥 Health check server running on port ${this.healthCheckPort}`);
    });
  }

  /**
   * Get overall status
   */
  getStatus() {
    return {
      running: this.isRunning,
      whatsapp: this.whatsapp ? this.whatsapp.getStatus() : { disabled: true },
      telegram: this.telegram ? this.telegram.getStatus() : { disabled: true },
      agent: this.jarvisAgent ? { connected: true } : { connected: false }
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('🛑 Shutting down JARVIS Communication Hub...');
    
    if (this.whatsapp) {
      await this.whatsapp.shutdown();
    }

    if (this.telegram) {
      await this.telegram.shutdown();
    }

    if (this.healthCheckServer) {
      this.healthCheckServer.close();
    }

    this.isRunning = false;
    console.log('✅ Communication Hub shutdown complete');
  }
}

// Export for use as module
module.exports = JarvisCommunicationHub;

// If run directly, start the hub
if (require.main === module) {
  const config = {
    whatsapp: {
      enabled: process.env.JARVIS_WHATSAPP_ENABLED === 'true',
      sessionPath: process.env.JARVIS_WHATSAPP_SESSION_PATH || './data/jarvis_sessions/whatsapp'
    },
    telegram: {
      enabled: process.env.JARVIS_TELEGRAM_ENABLED === 'true',
      token: process.env.JARVIS_TELEGRAM_BOT_TOKEN,
      broadcastChatId: process.env.JARVIS_TELEGRAM_BROADCAST_CHAT_ID
    },
    healthCheckPort: parseInt(process.env.JARVIS_HEALTH_CHECK_PORT || '3001')
  };

  const hub = new JarvisCommunicationHub(config);

  // Handle graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\n🛑 Received SIGINT, shutting down gracefully...');
    await hub.shutdown();
    process.exit(0);
  });

  process.on('SIGTERM', async () => {
    console.log('\n🛑 Received SIGTERM, shutting down gracefully...');
    await hub.shutdown();
    process.exit(0);
  });

  // Initialize and start
  (async () => {
    await hub.initialize();
    await hub.start();
  })();
}
