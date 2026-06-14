/**
 * JARVIS System - Isolated Entry Point
 * ====================================
 * 
 * Main entry point for the isolated JARVIS system.
 * Runs independently from lumina-overmind for fault tolerance.
 */

const express = require('express');
const { getGeminiService } = require('./channels/services/geminiService');
const { getCreatorSecurity } = require('./security/creatorMiddleware');
require('dotenv').config();

class JarvisSystem {
  constructor() {
    this.app = express();
    this.port = process.env.JARVIS_PORT || 3001;
    this.luminaApiUrl = process.env.LUMINA_API_URL || 'http://localhost:8000';
    this.isConnectedToLumina = false;
    this.connectionBridge = null;
    
    this._initializeMiddleware();
    this._initializeRoutes();
    this._initializeServices();
  }
  
  /**
   * Initialize middleware
   */
  _initializeMiddleware() {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));
    
    // CORS for connection bridge
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
      res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      next();
    });
  }
  
  /**
   * Initialize routes
   */
  _initializeRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        system: 'jarvis',
        connectedToLumina: this.isConnectedToLumina,
        luminaApiUrl: this.luminaApiUrl,
        timestamp: new Date().toISOString(),
      });
    });
    
    // Connection bridge control
    this.app.post('/api/bridge/connect', async (req, res) => {
      try {
        const result = await this.connectToLumina();
        res.json(result);
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message,
        });
      }
    });
    
    this.app.post('/api/bridge/disconnect', async (req, res) => {
      try {
        const result = await this.disconnectFromLumina();
        res.json(result);
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message,
        });
      }
    });
    
    this.app.get('/api/bridge/status', (req, res) => {
      res.json({
        connected: this.isConnectedToLumina,
        luminaApiUrl: this.luminaApiUrl,
        lastConnection: this.lastConnectionTime,
      });
    });
    
    // JARVIS communication endpoint
    this.app.post('/api/jarvis/message', async (req, res) => {
      try {
        const { userId, message, platform, context } = req.body;
        
        const geminiService = getGeminiService();
        const result = await geminiService.generateResponse(userId, message, {
          platform: platform || 'api',
          ...context,
        });
        
        res.json(result);
      } catch (error) {
        res.status(500).json({
          success: false,
          error: error.message,
        });
      }
    });
  }
  
  /**
   * Initialize services
   */
  _initializeServices() {
    // Initialize Creator Security
    const creatorSecurity = getCreatorSecurity();
    console.log('🔐 Creator Security initialized');
    
    // Initialize Gemini Service
    const geminiService = getGeminiService();
    console.log('🧠 Gemini Service initialized');
    
    // Initialize Watcher Protocol
    this._initializeWatcherProtocol();
  }
  
  /**
   * Initialize Watcher Protocol for codebase awareness
   */
  _initializeWatcherProtocol() {
    const { getWatcherProtocol } = require('./intelligence/watcherProtocol');
    this.watcher = getWatcherProtocol({
      luminaPath: '../',  // Path to lumina-overmind root
      watchInterval: 60000,  // Scan every minute
    });
    
    console.log('👁️ Watcher Protocol initialized');
  }
  
  /**
   * Connect to Lumina API
   */
  async connectToLumina() {
    try {
      console.log('🔗 Connecting to Lumina API...');
      
      // Test connection
      const response = await fetch(`${this.luminaApiUrl}/health`);
      
      if (response.ok) {
        this.isConnectedToLumina = true;
        this.lastConnectionTime = new Date().toISOString();
        
        console.log('✅ Connected to Lumina API');
        
        return {
          success: true,
          message: 'Successfully connected to Lumina API',
          luminaApiUrl: this.luminaApiUrl,
          connectedAt: this.lastConnectionTime,
        };
      } else {
        throw new Error('Lumina API health check failed');
      }
      
    } catch (error) {
      console.error('❌ Failed to connect to Lumina:', error.message);
      
      return {
        success: false,
        error: error.message,
        message: 'Failed to connect to Lumina API',
      };
    }
  }
  
  /**
   * Disconnect from Lumina API
   */
  async disconnectFromLumina() {
    try {
      console.log('🔌 Disconnecting from Lumina API...');
      
      this.isConnectedToLumina = false;
      this.lastConnectionTime = null;
      
      console.log('✅ Disconnected from Lumina API');
      
      return {
        success: true,
        message: 'Successfully disconnected from Lumina API',
        disconnectedAt: new Date().toISOString(),
      };
      
    } catch (error) {
      console.error('❌ Error disconnecting from Lumina:', error.message);
      
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  /**
   * Start JARVIS system
   */
  start() {
    this.app.listen(this.port, () => {
      console.log('🚀 JARVIS System started');
      console.log(`📡 Listening on port ${this.port}`);
      console.log(`🔗 Lumina API URL: ${this.luminaApiUrl}`);
      console.log(`🔐 Creator Security: Active`);
      console.log(`👁️ Watcher Protocol: Active`);
      console.log('');
      console.log('JARVIS is running in ISOLATED mode');
      console.log('Lumina crashes will NOT affect JARVIS');
    });
  }
}

// Start JARVIS system if run directly
if (require.main === module) {
  const jarvis = new JarvisSystem();
  jarvis.start();
}

module.exports = JarvisSystem;
