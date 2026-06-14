/**
 * JARVIS Telegram Connection Manager (Webhook Mode)
 * ====================================================
 * 
 * Persistent Telegram bot integration using Webhook mode
 * for better performance and Cloudflare Tunnel compatibility
 */

const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');
const express = require('express');
const { getGeminiService } = require('../services/geminiService');
const { sendWithTypingDelay, formatMessageWithPersona } = require('../utils/humanCommunication');

class JarvisTelegramBot {
  constructor(config) {
    this.config = config;
    this.bot = null;
    this.isConnected = false;
    this.webhookActive = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 5000; // 5 seconds
    this.messageHandlers = [];
    
    // Webhook configuration
    this.webhookUrl = config.webhookUrl;
    this.webhookPath = config.webhookPath || '/telegram-webhook';
    this.webhookSecret = config.webhookSecret || 'jarvis_telegram_secret';
    
    // Express app for webhook
    this.app = express();
    this.server = null;
    this.port = config.webhookPort || 3000;
    
    // Session storage path
    this.sessionPath = path.join(__dirname, '../../data/sessions/telegram');
    
    // Ensure session directory exists
    if (!fs.existsSync(this.sessionPath)) {
      fs.mkdirSync(this.sessionPath, { recursive: true });
    }
  }

  /**
   * Initialize Telegram bot
   */
  initialize() {
    console.log('🤖 Initializing JARVIS Telegram Bot (Webhook Mode)...');
    
    this.bot = new TelegramBot(this.config.token, {
      polling: false, // Webhook mode - no polling
      request: {
        agentOptions: {
          keepAlive: true,
          keepAliveMsecs: 10000
        }
      }
    });

    this.setupEventListeners();
    this.setupWebhookServer();
    return this.bot;
  }

  /**
   * Setup event listeners for Telegram bot
   */
  setupEventListeners() {
    // Message received (via webhook)
    this.bot.on('message', async (msg) => {
      await this.handleIncomingMessage(msg);
    });

    // Callback query (inline buttons)
    this.bot.on('callback_query', async (query) => {
      await this.handleCallbackQuery(query);
    });

    // Webhook error
    this.bot.on('webhook_error', (error) => {
      console.error('❌ Telegram Webhook Error:', error.message);
    });
  }

  /**
   * Setup Express server for webhook
   */
  setupWebhookServer() {
    // Middleware to verify webhook secret
    this.app.use((req, res, next) => {
      const secret = req.headers['x-telegram-bot-api-secret-token'];
      
      if (secret !== this.webhookSecret) {
        console.warn('⚠️ Unauthorized webhook request (invalid secret)');
        return res.status(403).json({ error: 'Unauthorized' });
      }
      
      next();
    });

    // Webhook endpoint
    this.app.post(this.webhookPath, (req, res) => {
      this.bot.processUpdate(req.body);
      res.sendStatus(200);
    });

    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'ok',
        webhook: this.webhookActive,
        connected: this.isConnected,
      });
    });
  }

  /**
   * Start webhook server
   */
  async startWebhook() {
    if (this.webhookActive) {
      console.log('⚠️ Webhook already active');
      return;
    }

    try {
      console.log('🚀 Starting JARVIS Telegram Bot Webhook...');
      
      // Set webhook
      await this.bot.setWebHook(`${this.webhookUrl}${this.webhookPath}`, {
        secret_token: this.webhookSecret,
      });
      
      console.log(`✅ Webhook set to: ${this.webhookUrl}${this.webhookPath}`);
      
      // Start Express server
      this.server = this.app.listen(this.port, () => {
        console.log(`🌐 Webhook server listening on port ${this.port}`);
      });
      
      this.webhookActive = true;
      this.isConnected = true;
      this.reconnectAttempts = 0;
      
      console.log('✅ JARVIS Telegram Bot is WEBHOOK MODE');
      
      // Get bot info
      const botInfo = await this.bot.getMe();
      console.log(`🤖 Connected as: @${botInfo.username}`);
      console.log(`🤖 Bot ID: ${botInfo.id}`);
      
    } catch (error) {
      console.error('❌ Failed to start webhook:', error.message);
      this.webhookActive = false;
      this.isConnected = false;
      this.scheduleReconnect();
    }
  }

  /**
   * Stop webhook server
   */
  async stopWebhook() {
    if (!this.webhookActive) {
      return;
    }

    try {
      console.log('🛑 Stopping Telegram Bot Webhook...');
      
      // Delete webhook
      await this.bot.deleteWebHook();
      
      // Close Express server
      if (this.server) {
        this.server.close();
      }
      
      this.webhookActive = false;
      this.isConnected = false;
      console.log('✅ Webhook stopped');
    } catch (error) {
      console.error('❌ Error stopping webhook:', error.message);
    }
  }

  /**
   * Restart webhook (for error recovery)
   */
  async restartWebhook() {
    await this.stopWebhook();
    
    // Wait a bit before restarting
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    await this.startWebhook();
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
        await this.startWebhook();
      } catch (error) {
        console.error('❌ Reconnection failed:', error.message);
        this.scheduleReconnect();
      }
    }, delay);
  }

  /**
   * Handle incoming Telegram message
   */
  async handleIncomingMessage(msg) {
    try {
      const chat = msg.chat;
      const user = msg.from;
      
      const messageData = {
        platform: 'telegram',
        from: {
          id: user.id.toString(),
          name: user.first_name + (user.last_name ? ' ' + user.last_name : ''),
          username: user.username || null,
          isGroup: chat.type !== 'private'
        },
        message: msg.text || '',
        timestamp: new Date(msg.date * 1000).toISOString(),
        messageId: msg.message_id.toString(),
        chatId: chat.id.toString()
      };

      console.log(`📩 Telegram message from ${user.username || user.first_name} (${user.id}): ${msg.text || '[non-text message]'}`);

      // Route to message handlers
      for (const handler of this.messageHandlers) {
        await handler(messageData);
      }
      
      // Handle different message types
      if (chat.type === 'private') {
        // Text message
        if (msg.text) {
          await this.generateJarvisResponse(messageData);
        }
        // Photo/image
        else if (msg.photo) {
          await this.handleImageMessage(msg, messageData);
        }
        // Voice/audio
        else if (msg.voice) {
          await this.handleVoiceMessage(msg, messageData);
        }
        // Check for approval response (YES/NO)
        else if (msg.text && msg.text.toLowerCase() === 'yes') {
          await this.handleApprovalResponse(messageData);
        }
      }
    } catch (error) {
      console.error('❌ Error handling Telegram message:', error.message);
    }
  }
  
  /**
   * Handle image/photo message
   */
  async handleImageMessage(msg, messageData) {
    try {
      const geminiService = getGeminiService();
      
      // Get the largest photo
      const photo = msg.photo[msg.photo.length - 1];
      const fileId = photo.file_id;
      
      // Get file info
      const fileInfo = await this.bot.getFile(fileId);
      const fileUrl = `https://api.telegram.org/file/bot${this.config.token}/${fileInfo.file_path}`;
      
      // Download image buffer
      const https = require('https');
      const imageBuffer = await new Promise((resolve, reject) => {
        https.get(fileUrl, (response) => {
          const chunks = [];
          response.on('data', (chunk) => chunks.push(chunk));
          response.on('end', () => resolve(Buffer.concat(chunks)));
          response.on('error', reject);
        });
      });
      
      // Generate multimodal response
      const result = await geminiService.generateMultimodalResponse(
        messageData.from.id,
        messageData.message || 'Analyze this image',
        {
          type: 'image',
          buffer: imageBuffer,
          mimeType: 'image/jpeg',
        },
        {
          platform: 'telegram',
          username: messageData.from.username,
          timestamp: messageData.timestamp,
        }
      );
      
      if (result.success) {
        await this.sendMessage(messageData.chatId, result.response);
        console.log(`🖼️ JARVIS image analysis sent to ${messageData.from.username || messageData.from.name}`);
      } else {
        console.error('❌ Failed to analyze image:', result.error);
      }
    } catch (error) {
      console.error('❌ Error handling image message:', error.message);
      await this.sendMessage(messageData.chatId, 'I apologize, but I encountered an error processing the image.');
    }
  }
  
  /**
   * Handle voice/audio message
   */
  async handleVoiceMessage(msg, messageData) {
    try {
      const geminiService = getGeminiService();
      
      const voice = msg.voice;
      const fileId = voice.file_id;
      
      // Get file info
      const fileInfo = await this.bot.getFile(fileId);
      const fileUrl = `https://api.telegram.org/file/bot${this.config.token}/${fileInfo.file_path}`;
      
      // Download audio buffer
      const https = require('https');
      const audioBuffer = await new Promise((resolve, reject) => {
        https.get(fileUrl, (response) => {
          const chunks = [];
          response.on('data', (chunk) => chunks.push(chunk));
          response.on('end', () => resolve(Buffer.concat(chunks)));
          response.on('error', reject);
        });
      });
      
      // Generate multimodal response
      const result = await geminiService.generateMultimodalResponse(
        messageData.from.id,
        messageData.message || 'Transcribe this voice note',
        {
          type: 'audio',
          buffer: audioBuffer,
          mimeType: 'audio/ogg',
        },
        {
          platform: 'telegram',
          username: messageData.from.username,
          timestamp: messageData.timestamp,
        }
      );
      
      if (result.success) {
        await this.sendMessage(messageData.chatId, result.response);
        console.log(`🎤 JARVIS voice analysis sent to ${messageData.from.username || messageData.from.name}`);
      } else {
        console.error('❌ Failed to process voice:', result.error);
      }
    } catch (error) {
      console.error('❌ Error handling voice message:', error.message);
      await this.sendMessage(messageData.chatId, 'I apologize, but I encountered an error processing the voice note.');
    }
  }
  
  /**
   * Handle approval response (YES/NO)
   */
  async handleApprovalResponse(messageData) {
    try {
      const geminiService = getGeminiService();
      
      // Apply patch
      const result = await geminiService.applyPatch(
        messageData.from.id,
        messageData.message
      );
      
      if (result.success) {
        await this.sendMessage(messageData.chatId, `✅ ${result.message}`);
      } else {
        await this.sendMessage(messageData.chatId, `❌ ${result.error}`);
      }
    } catch (error) {
      console.error('❌ Error handling approval response:', error.message);
    }
  }
  
  /**
   * Generate JARVIS response using Gemini AI
   */
  async generateJarvisResponse(messageData) {
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
          platform: 'telegram',
          username: messageData.from.username,
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
          async (msg) => await this.sendMessage(messageData.chatId, msg),
          formattedMessage,
          {
            showTyping: true,
            splitChunks: true,
            chunkDelay: 1000,
          }
        );
        
        // Increment interaction count
        await this._incrementInteractionCount(messageData.from.id);
        
        console.log(`🤖 JARVIS response sent to ${messageData.from.username || messageData.from.name} (persona: ${persona})`);
      } else {
        console.error('❌ Failed to generate JARVIS response:', result.error);
      }
    } catch (error) {
      console.error('❌ Error generating JARVIS response:', error.message);
      // Send fallback message
      await this.sendMessage(
        messageData.chatId,
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
   * Handle callback query (inline buttons)
   */
  async handleCallbackQuery(query) {
    try {
      const data = query.data;
      const user = query.from;
      
      console.log(`🔘 Callback query from ${user.username || user.first_name}: ${data}`);
      
      // Acknowledge callback
      await this.bot.answerCallbackQuery(query.id);
      
      // Route to handlers if needed
      // (Can be extended for interactive features)
      
    } catch (error) {
      console.error('❌ Error handling callback query:', error.message);
    }
  }

  /**
   * Send message via Telegram
   */
  async sendMessage(chatId, message, options = {}) {
    if (!this.isConnected) {
      console.error('❌ Telegram bot not connected');
      return false;
    }

    try {
      await this.bot.sendMessage(chatId, message, {
        parse_mode: 'Markdown',
        ...options
      });
      console.log(`📤 Telegram message sent to ${chatId}`);
      return true;
    } catch (error) {
      console.error('❌ Failed to send Telegram message:', error.message);
      return false;
    }
  }

  /**
   * Send message with inline keyboard
   */
  async sendMessageWithKeyboard(chatId, message, keyboard) {
    if (!this.isConnected) {
      console.error('❌ Telegram bot not connected');
      return false;
    }

    try {
      await this.bot.sendMessage(chatId, message, {
        parse_mode: 'Markdown',
        reply_markup: {
          inline_keyboard: keyboard
        }
      });
      console.log(`📤 Telegram message with keyboard sent to ${chatId}`);
      return true;
    } catch (error) {
      console.error('❌ Failed to send Telegram message with keyboard:', error.message);
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
      webhook: this.webhookActive,
      reconnectAttempts: this.reconnectAttempts,
      sessionPath: this.sessionPath,
      webhookUrl: this.webhookUrl,
    };
  }

  /**
   * Graceful shutdown
   */
  async shutdown() {
    console.log('🛑 Shutting down JARVIS Telegram Bot...');
    await this.stopWebhook();
    this.isConnected = false;
    console.log('✅ Telegram Bot shutdown complete');
  }
}

module.exports = JarvisTelegramBot;
