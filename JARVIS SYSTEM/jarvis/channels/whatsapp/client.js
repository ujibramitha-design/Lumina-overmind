/**
 * JARVIS WhatsApp Connection Manager
 * =================================
 * 
 * Persistent WhatsApp integration with session persistence
 * and auto-reconnect logic using whatsapp-web.js
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const path = require('path');
const fs = require('fs');
const { getGeminiService } = require('../services/geminiService');
const { sendWithTypingDelay, formatMessageWithPersona } = require('../utils/humanCommunication');

class JarvisWhatsAppClient {
  constructor(config) {
    this.config = config;
    this.client = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 5000; // 5 seconds
    this.messageHandlers = [];
    
    // Session storage path
    this.sessionPath = path.join(__dirname, '../../data/sessions/whatsapp');
    
    // Ensure session directory exists
    if (!fs.existsSync(this.sessionPath)) {
      fs.mkdirSync(this.sessionPath, { recursive: true });
    }
  }

  /**
   * Initialize WhatsApp client with LocalAuth for session persistence
   */
  initialize() {
    console.log('🤖 Initializing JARVIS WhatsApp Client...');
    
    this.client = new Client({
      authStrategy: new LocalAuth({
        dataPath: this.sessionPath,
        clientId: 'jarvis-whatsapp'
      }),
      puppeteer: {
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--no-zygote',
          '--single-process',
          '--disable-gpu'
        ]
      },
      qrMaxRetries: 5,
      takeoverTimeout: 60000,
      takeoverOnConflict: true
    });

    this.setupEventListeners();
    return this.client;
  }

  /**
   * Setup event listeners for WhatsApp client
   */
  setupEventListeners() {
    // QR Code generation for initial authentication
    this.client.on('qr', (qr) => {
      console.log('\n' + '='.repeat(50));
      console.log('📱 SCAN QR CODE TO CONNECT JARVIS WHATSAPP');
      console.log('='.repeat(50));
      qrcode.generate(qr, { small: true });
      console.log('='.repeat(50) + '\n');
      console.log('Scan this QR code with JARVIS\'s dedicated WhatsApp number');
      console.log('Session will be saved automatically after successful scan\n');
    });

    // Ready event - client is authenticated and ready
    this.client.on('ready', () => {
      console.log('✅ JARVIS WhatsApp Client is READY');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      
      // Get device info
      this.client.getInfo().then((info) => {
        console.log(`📱 Connected as: ${info.pushname} (${info.wid.user})`);
        console.log(`📱 Platform: ${info.platform}`);
      });
    });

    // Authentication success
    this.client.on('authenticated', (session) => {
      console.log('✅ JARVIS WhatsApp Session AUTHENTICATED');
      console.log('📁 Session saved to:', this.sessionPath);
    });

    // Authentication failure
    this.client.on('auth_failure', (msg) => {
      console.error('❌ WhatsApp Authentication Failed:', msg);
      console.log('🔄 Will attempt to reconnect...');
      this.scheduleReconnect();
    });

    // Disconnection event
    this.client.on('disconnected', (reason) => {
      console.log('⚠️ WhatsApp Client Disconnected:', reason);
      this.isConnected = false;
      console.log('🔄 Attempting to reconnect...');
      this.scheduleReconnect();
    });

    // Message received
    this.client.on('message', async (message) => {
      await this.handleIncomingMessage(message);
    });

    // Error handling
    this.client.on('error', (error) => {
      console.error('❌ WhatsApp Client Error:', error.message);
      if (!this.isConnected) {
        this.scheduleReconnect();
      }
    });
  }

  /**
   * Start the WhatsApp client
   */
  async start() {
    try {
      await this.client.initialize();
      console.log('🚀 Starting JARVIS WhatsApp Client...');
      await this.client.connect();
    } catch (error) {
      console.error('❌ Failed to start WhatsApp client:', error.message);
      this.scheduleReconnect();
    }
  }

  /**
   * Schedule reconnection attempt with exponential backoff
   */
  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max reconnection attempts reached. Giving up.');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`🔄 Reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay/1000}s...`);
    
    setTimeout(async () => {
      try {
        await this.start();
      } catch (error) {
        console.error('❌ Reconnection failed:', error.message);
        this.scheduleReconnect();
      }
    }, delay);
  }

  /**
   * Handle incoming WhatsApp message
   */
  async handleIncomingMessage(message) {
    try {
      const contact = await message.getContact();
      const chat = await message.getChat();
      
      const messageData = {
        platform: 'whatsapp',
        from: {
          id: contact.number,
          name: contact.pushname,
          isGroup: chat.isGroup
        },
        message: message.body,
        timestamp: new Date().toISOString(),
        messageId: message.id._serialized
      };

      console.log(`📩 WhatsApp message from ${contact.pushname} (${contact.number}): ${message.body}`);

      // Route to message handlers
      for (const handler of this.messageHandlers) {
        await handler(messageData);
      }
      
      // Handle different message types (only for private chats)
      if (!chat.isGroup) {
        // Text message
        if (message.body) {
          await this.generateJarvisResponse(messageData, message);
        }
        // Image message
        else if (message.hasMedia && message.type === 'image') {
          await this.handleImageMessage(message, messageData);
        }
        // Voice/audio message
        else if (message.hasMedia && message.type === 'audio') {
          await this.handleVoiceMessage(message, messageData);
        }
        // Check for approval response (YES/NO)
        else if (message.body && message.body.toLowerCase() === 'yes') {
          await this.handleApprovalResponse(messageData, message);
        }
      }
    } catch (error) {
      console.error('❌ Error handling WhatsApp message:', error.message);
    }
  }
  
  /**
   * Handle image message
   */
  async handleImageMessage(message, messageData) {
    try {
      const geminiService = getGeminiService();
      
      // Download media
      const media = await message.downloadMedia();
      
      if (!media) {
        throw new Error('Failed to download media');
      }
      
      // Convert base64 to buffer
      const imageBuffer = Buffer.from(media.data, 'base64');
      
      // Generate multimodal response
      const result = await geminiService.generateMultimodalResponse(
        messageData.from.id,
        messageData.message || 'Analyze this image',
        {
          type: 'image',
          buffer: imageBuffer,
          mimeType: media.mimetype || 'image/jpeg',
        },
        {
          platform: 'whatsapp',
          phoneNumber: messageData.from.id,
          timestamp: messageData.timestamp,
        }
      );
      
      if (result.success) {
        await message.reply(result.response);
        console.log(`🖼️ JARVIS image analysis sent to ${messageData.from.name}`);
      } else {
        console.error('❌ Failed to analyze image:', result.error);
      }
    } catch (error) {
      console.error('❌ Error handling image message:', error.message);
      await message.reply('I apologize, but I encountered an error processing the image.');
    }
  }
  
  /**
   * Handle voice/audio message
   */
  async handleVoiceMessage(message, messageData) {
    try {
      const geminiService = getGeminiService();
      
      // Download media
      const media = await message.downloadMedia();
      
      if (!media) {
        throw new Error('Failed to download media');
      }
      
      // Convert base64 to buffer
      const audioBuffer = Buffer.from(media.data, 'base64');
      
      // Generate multimodal response
      const result = await geminiService.generateMultimodalResponse(
        messageData.from.id,
        messageData.message || 'Transcribe this voice note',
        {
          type: 'audio',
          buffer: audioBuffer,
          mimeType: media.mimetype || 'audio/ogg',
        },
        {
          platform: 'whatsapp',
          phoneNumber: messageData.from.id,
          timestamp: messageData.timestamp,
        }
      );
      
      if (result.success) {
        await message.reply(result.response);
        console.log(`🎤 JARVIS voice analysis sent to ${messageData.from.name}`);
      } else {
        console.error('❌ Failed to process voice:', result.error);
      }
    } catch (error) {
      console.error('❌ Error handling voice message:', error.message);
      await message.reply('I apologize, but I encountered an error processing the voice note.');
    }
  }
  
  /**
   * Handle approval response (YES/NO)
   */
  async handleApprovalResponse(messageData, originalMessage) {
    try {
      const geminiService = getGeminiService();
      
      // Apply patch
      const result = await geminiService.applyPatch(
        messageData.from.id,
        messageData.message
      );
      
      if (result.success) {
        await originalMessage.reply(`✅ ${result.message}`);
      } else {
        await originalMessage.reply(`❌ ${result.error}`);
      }
    } catch (error) {
      console.error('❌ Error handling approval response:', error.message);
    }
  }
  
  /**
   * Generate JARVIS response using Gemini AI
   */
  async generateJarvisResponse(messageData, originalMessage) {
    try {
      const geminiService = getGeminiService();
      
      // Get user's interaction count for persona
      const interactionCount = await this._getUserInteractionCount(messageData.from.id);
      const persona = this._getPersonaFromCount(interactionCount);
      
      // Generate response with context
      const result = await geminiService.generateResponse(
        messageData.from.id,
        messageData.message,
        {
          platform: 'whatsapp',
          phoneNumber: messageData.from.id,
          timestamp: messageData.timestamp,
          interactionCount: interactionCount,
          persona: persona,
        }
      );
      
      if (result.success) {
        // Format message with persona
        const formattedMessage = formatMessageWithPersona(result.response, {
          formality: persona,
          useEmojis: true,
          useCasualMarkers: persona !== 'formal',
        });
        
        // Send with human-like typing delay and message splitting
        await sendWithTypingDelay(
          async (msg) => await originalMessage.reply(msg),
          formattedMessage,
          {
            showTyping: true,
            splitChunks: true,
            chunkDelay: 1000,
          }
        );
        
        // Increment interaction count
        await this._incrementInteractionCount(messageData.from.id);
        
        console.log(`🤖 JARVIS response sent to ${messageData.from.name} (persona: ${persona})`);
      } else {
        console.error('❌ Failed to generate JARVIS response:', result.error);
      }
    } catch (error) {
      console.error('❌ Error generating JARVIS response:', error.message);
      // Send fallback message
      await originalMessage.reply(
        'I apologize, but I encountered an error processing your request. Please try again.'
      );
    }
  }
  
  /**
   * Get user's interaction count from database
   */
  async _getUserInteractionCount(userId) {
    try {
      // This would query the database for interaction count
      // For now, return a default value
      // TODO: Implement database query
      return 0;
    } catch (error) {
      console.error('Error getting interaction count:', error);
      return 0;
    }
  }
  
  /**
   * Increment user's interaction count
   */
  async _incrementInteractionCount(userId) {
    try {
      // This would update the database
      // TODO: Implement database update
      console.log(`Incrementing interaction count for ${userId}`);
    } catch (error) {
      console.error('Error incrementing interaction count:', error);
    }
  }
  
  /**
   * Get persona based on interaction count
   */
  _getPersonaFromCount(count) {
    if (count < 100) {
      return 'formal';  // Strictly formal
    } else if (count < 500) {
      return 'casual';  // More casual
    } else {
      return 'friendly';  // Close, trusted colleague
    }
  }

  /**
   * Send message via WhatsApp
   */
  async sendMessage(to, message) {
    if (!this.isConnected) {
      console.error('❌ WhatsApp client not connected');
      return false;
    }

    try {
      await this.client.sendMessage(to, message);
      console.log(`📤 WhatsApp message sent to ${to}`);
      return true;
    } catch (error) {
      console.error('❌ Failed to send WhatsApp message:', error.message);
      return false;
    }
  }

  /**
   * Register message handler
   */
  onMessage(handler) {
    this.messageHandlers.push(handler);
  }

  /**
   * Get connection status
   */
  getStatus() {
    return {
      connected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      sessionPath: this.sessionPath
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('🛑 Shutting down JARVIS WhatsApp Client...');
    if (this.client) {
      await this.client.destroy();
    }
    this.isConnected = false;
    console.log('✅ WhatsApp Client shutdown complete');
  }
}

module.exports = JarvisWhatsAppClient;
