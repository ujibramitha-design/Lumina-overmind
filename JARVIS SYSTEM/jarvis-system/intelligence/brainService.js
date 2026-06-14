/**
 * JARVIS Brain Service - Unified AI Brain with Bunker Protocol
 * ===========================================================
 * 
 * Unified brain service with fast-failover from Gemini to Ollama
 * for absolute resilience and 100% operational uptime without internet.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const { Ollama } = require('ollama');
require('dotenv').config();

class BrainService {
  constructor(config = {}) {
    this.config = {
      primaryProvider: config.primaryProvider || 'gemini',  // gemini or ollama
      fallbackProvider: config.fallbackProvider || 'ollama',
      geminiApiKey: config.gemamiApiKey || process.env.GEMINI_API_KEY,
      ollamaHost: config.ollamaHost || 'http://localhost:11434',
      ollamaModel: config.ollamaModel || 'llama3',
      geminiModel: config.geminiModel || 'gemini-1.5-pro',
      timeout: config.timeout || 10000,  // 10 seconds
      maxRetries: config.maxRetries || 3,
      ...config,
    };
    
    // Initialize primary provider (Gemini)
    this.genAI = new GoogleGenerativeAI(this.config.geminiApiKey);
    this.geminiModel = this.genAI.getGenerativeModel({
      model: this.config.geminiModel,
    });
    
    // Initialize fallback provider (Ollama)
    this.ollama = new Ollama({ host: this.config.ollamaHost });
    
    // Provider status
    this.providerStatus = {
      gemini: 'available',
      ollama: 'available',
      currentProvider: this.config.primaryProvider,
      lastFailover: null,
      failoverCount: 0,
    };
    
    // Test providers on initialization
    this._testProviders();
  }
  
  /**
   * Test provider availability
   */
  async _testProviders() {
    try {
      // Test Gemini
      await this._testGemini();
      console.log('✅ Gemini provider: AVAILABLE');
    } catch (error) {
      console.warn('⚠️ Gemini provider: UNAVAILABLE', error.message);
      this.providerStatus.gemini = 'unavailable';
    }
    
    try {
      // Test Ollama
      await this._testOllama();
      console.log('✅ Ollama provider: AVAILABLE');
    } catch (error) {
      console.warn('⚠️ Ollama provider: UNAVAILABLE', error.message);
      this.providerStatus.ollama = 'unavailable';
    }
    
    // Set current provider based on availability
    if (this.providerStatus.gemini === 'unavailable') {
      this.providerStatus.currentProvider = 'ollama';
      console.log('🔄 Failover to Ollama: Gemini unavailable');
    }
  }
  
  /**
   * Test Gemini provider
   */
  async _testGemini() {
    const testModel = this.genAI.getGenerativeModel({
      model: this.config.geminiModel,
    });
    
    const result = await Promise.race([
      testModel.generateContent('test'),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
      ),
    ]);
    
    return result;
  }
  
  /**
   * Test Ollama provider
   */
  async _testOllama() {
    const result = await Promise.race([
      this.ollama.chat({
        model: this.config.ollamaModel,
        messages: [{ role: 'user', content: 'test' }],
      }),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), 5000)
      ),
    ]);
    
    return result;
  }
  
  /**
   * Generate response with automatic failover
   */
  async generateResponse(systemPrompt, userPrompt, options = {}) {
    const provider = this.providerStatus.currentProvider;
    
    try {
      if (provider === 'gemini') {
        return await this._generateWithGemini(systemPrompt, userPrompt, options);
      } else {
        return await this._generateWithOllama(systemPrompt, userPrompt, options);
      }
    } catch (error) {
      console.error(`❌ Error with ${provider} provider:`, error.message);
      
      // Attempt failover
      return await this._failover(systemPrompt, userPrompt, options, provider);
    }
  }
  
  /**
   * Generate with Gemini
   */
  async _generateWithGemini(systemPrompt, userPrompt, options = {}) {
    const timeout = options.timeout || this.config.timeout;
    
    const result = await Promise.race([
      this.geminiModel.generateContent([
        { role: 'user', parts: [{ text: systemPrompt }] },
        { role: 'user', parts: [{ text: userPrompt }] },
      ]),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Gemini timeout')), timeout)
      ),
    ]);
    
    return {
      success: true,
      response: result.response.text(),
      provider: 'gemini',
      model: this.config.geminiModel,
    };
  }
  
  /**
   * Generate with Ollama
   */
  async _generateWithOllama(systemPrompt, userPrompt, options = {}) {
    const timeout = options.timeout || this.config.timeout;
    
    const result = await Promise.race([
      this.ollama.chat({
        model: this.config.ollamaModel,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt },
        ],
      }),
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Ollama timeout')), timeout)
      ),
    ]);
    
    return {
      success: true,
      response: result.message.content,
      provider: 'ollama',
      model: this.config.ollamaModel,
    };
  }
  
  /**
   * Failover to alternative provider
   */
  async _failover(systemPrompt, userPrompt, options, failedProvider) {
    console.log(`🔄 Attempting failover from ${failedProvider}...`);
    
    const fallbackProvider = failedProvider === 'gemini' ? 'ollama' : 'gemini';
    
    // Check if fallback is available
    if (this.providerStatus[fallbackProvider] === 'unavailable') {
      throw new Error(`Both providers unavailable. Cannot failover.`);
    }
    
    try {
      this.providerStatus.currentProvider = fallbackProvider;
      this.providerStatus.lastFailover = new Date().toISOString();
      this.providerStatus.failoverCount++;
      
      console.log(`🔄 Failing over to ${fallbackProvider}...`);
      
      if (fallbackProvider === 'gemini') {
        return await this._generateWithGemini(systemPrompt, userPrompt, options);
      } else {
        return await this._generateWithOllama(systemPrompt, userPrompt, options);
      }
    } catch (error) {
      console.error(`❌ Failover to ${fallbackProvider} failed:`, error.message);
      
      // Revert to original provider
      this.providerStatus.currentProvider = failedProvider;
      
      throw new Error(`Failover failed: ${error.message}`);
    }
  }
  
  /**
   * Force switch to specific provider
   */
  async switchProvider(provider) {
    if (provider !== 'gemini' && provider !== 'ollama') {
      throw new Error('Invalid provider. Must be "gemini" or "ollama"');
    }
    
    if (this.providerStatus[provider] === 'unavailable') {
      throw new Error(`${provider} provider is unavailable`);
    }
    
    this.providerStatus.currentProvider = provider;
    console.log(`🔄 Switched to ${provider} provider`);
    
    return {
      success: true,
      currentProvider: provider,
    };
  }
  
  /**
   * Get provider status
   */
  getProviderStatus() {
    return {
      ...this.providerStatus,
      config: {
        primaryProvider: this.config.primaryProvider,
        fallbackProvider: this.config.fallbackProvider,
        geminiModel: this.config.geminiModel,
        ollamaModel: this.config.ollamaModel,
        ollamaHost: this.config.ollamaHost,
      },
    };
  }
  
  /**
   * Health check
   */
  async healthCheck() {
    const status = {
      healthy: false,
      providers: {},
      currentProvider: this.providerStatus.currentProvider,
    };
    
    // Check Gemini
    try {
      await this._testGemini();
      status.providers.gemini = 'healthy';
    } catch (error) {
      status.providers.gemini = 'unhealthy';
    }
    
    // Check Ollama
    try {
      await this._testOllama();
      status.providers.ollama = 'healthy';
    } catch (error) {
      status.providers.ollama = 'unhealthy';
    }
    
    // Overall health
    status.healthy = Object.values(status.providers).some(s => s === 'healthy');
    
    return status;
  }
}

// Singleton instance
let brainService = null;

function getBrainService(config = null) {
  if (!brainService) {
    if (config === null) {
      config = {};
    }
    brainService = new BrainService(config);
  }
  return brainService;
}

module.exports = { BrainService, getBrainService };
