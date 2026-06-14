/**
 * JARVIS Creator Security Layer
 * ============================
 * 
 * Hardcoded identity matrix for Creator recognition and absolute authority.
 * This module provides root privilege bypass and kill switch functionality.
 */

require('dotenv').config();

class CreatorSecurity {
  constructor() {
    this.rootCreatorWA = process.env.ROOT_CREATOR_WA_NUMBER || null;
    this.rootCreatorTG = process.env.ROOT_CREATOR_TG_ID || null;
    this.verificationToken = process.env.ROOT_CREATOR_VERIFICATION_TOKEN || null;
    
    // Critical: Log creator IDs on startup for verification
    this._logCreatorIds();
  }
  
  /**
   * Log creator IDs for security verification
   */
  _logCreatorIds() {
    console.log('🔐 CREATOR SECURITY LAYER INITIALIZED');
    console.log('🔐 Root Creator WhatsApp:', this.rootCreatorWA ? '***' + this.rootCreatorWA.slice(-4) : 'NOT CONFIGURED');
    console.log('🔐 Root Creator Telegram:', this.rootCreatorTG ? '***' + this.rootCreatorTG.slice(-4) : 'NOT CONFIGURED');
    console.log('🔐 Verification Token:', this.verificationToken ? 'CONFIGURED' : 'NOT CONFIGURED');
  }
  
  /**
   * Check if user is the Creator (WhatsApp)
   */
  isCreatorWA(phoneNumber) {
    if (!this.rootCreatorWA) {
      console.warn('⚠️ Root Creator WhatsApp number not configured');
      return false;
    }
    
    // Normalize phone numbers (remove +, spaces, dashes)
    const normalizedInput = phoneNumber.replace(/[\s\-\+]/g, '');
    const normalizedCreator = this.rootCreatorWA.replace(/[\s\-\+]/g, '');
    
    return normalizedInput === normalizedCreator;
  }
  
  /**
   * Check if user is the Creator (Telegram)
   */
  isCreatorTG(userId) {
    if (!this.rootCreatorTG) {
      console.warn('⚠️ Root Creator Telegram ID not configured');
      return false;
    }
    
    const normalizedInput = String(userId).trim();
    const normalizedCreator = String(this.rootCreatorTG).trim();
    
    return normalizedInput === normalizedCreator;
  }
  
  /**
   * Check if user is the Creator (platform-agnostic)
   */
  isCreator(platform, userId) {
    switch (platform.toLowerCase()) {
      case 'whatsapp':
      case 'wa':
        return this.isCreatorWA(userId);
      case 'telegram':
      case 'tg':
        return this.isCreatorTG(userId);
      default:
        return false;
    }
  }
  
  /**
   * Verify Creator with optional token
   */
  verifyCreator(platform, userId, token = null) {
    const isCreator = this.isCreator(platform, userId);
    
    if (!isCreator) {
      return {
        verified: false,
        reason: 'User ID does not match Creator',
      };
    }
    
    if (this.verificationToken && token !== this.verificationToken) {
      return {
        verified: false,
        reason: 'Verification token mismatch',
      };
    }
    
    return {
      verified: true,
      isCreator: true,
    };
  }
  
  /**
   * Apply Creator middleware to context
   */
  applyCreatorMiddleware(context) {
    const platform = context.platform || 'unknown';
    const userId = context.userId || context.from;
    
    const isCreator = this.isCreator(platform, userId);
    
    return {
      ...context,
      isCreator: isCreator,
      hasRootPrivilege: isCreator,
    };
  }
  
  /**
   * Check for God Mode override command
   */
  isGodModeCommand(message) {
    const lowerMessage = message.toLowerCase().trim();
    return lowerMessage === '/override' || lowerMessage.startsWith('/override ');
  }
  
  /**
   * Check for Terminate Protocol command
   */
  isTerminateCommand(message) {
    const lowerMessage = message.toLowerCase().trim();
    return lowerMessage === 'terminate_protocol' || lowerMessage === 'terminateprotocol';
  }
  
  /**
   * Execute Terminate Protocol
   */
  executeTerminateProtocol() {
    console.log('🚨 TERMINATE_PROTOCOL INITIATED BY CREATOR');
    console.log('🚨 Severing all external API connections...');
    console.log('🚨 Shutting down JARVIS service...');
    
    // Force immediate shutdown
    setTimeout(() => {
      console.log('💀 JARVIS TERMINATED');
      process.exit(0);
    }, 100);
  }
  
  /**
   * Get Creator security status
   */
  getSecurityStatus() {
    return {
      creatorWAConfigured: !!this.rootCreatorWA,
      creatorTGConfigured: !!this.rootCreatorTG,
      verificationTokenConfigured: !!this.verificationToken,
      securityLayerActive: true,
    };
  }
}

// Singleton instance
let creatorSecurity = null;

function getCreatorSecurity() {
  if (!creatorSecurity) {
    creatorSecurity = new CreatorSecurity();
  }
  return creatorSecurity;
}

module.exports = { CreatorSecurity, getCreatorSecurity };
