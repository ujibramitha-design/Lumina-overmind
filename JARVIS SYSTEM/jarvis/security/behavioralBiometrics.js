/**
 * JARVIS Behavioral Biometric Security
 * ===================================
 * 
 * Zero-Trust profiling system that analyzes linguistic patterns
 * to verify user identity and prevent unauthorized access.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

class BehavioralBiometrics {
  constructor(config = {}) {
    this.config = {
      baselinePath: config.baselinePath || './jarvis/data/behavioral_baseline.json',
      confidenceThreshold: config.confidenceThreshold || 0.7,
      destructiveCommands: config.destructiveCommands || [
        'drop', 'delete', 'remove', 'truncate', 'format',
        'rm', 'del', 'erase', 'destroy', 'purge',
      ],
      lockdownDuration: config.lockdownDuration || 300000,  // 5 minutes
      maxFailedAttempts: config.maxFailedAttempts || 3,
      ...config,
    };
    
    this.baseline = null;
    this.lockdownMode = false;
    this.lockdownUntil = null;
    this.failedAttempts = 0;
    this.lockdownPassphrase = config.lockdownPassphrase || process.env.JARVIS_LOCKDOWN_PASSPHRASE;
    
    this._loadBaseline();
  }
  
  /**
   * Load behavioral baseline from storage
   */
  _loadBaseline() {
    try {
      if (fs.existsSync(this.config.baselinePath)) {
        this.baseline = JSON.parse(fs.readFileSync(this.config.baselinePath, 'utf8'));
        console.log('✅ Behavioral baseline loaded');
      } else {
        console.log('📝 No baseline found, will create from historical data');
        this.baseline = this._createDefaultBaseline();
      }
    } catch (error) {
      console.error('❌ Error loading baseline:', error.message);
      this.baseline = this._createDefaultBaseline();
    }
  }
  
  /**
   * Create default baseline
   */
  _createDefaultBaseline() {
    return {
      version: '1.0',
      lastUpdated: new Date().toISOString(),
      sampleSize: 0,
      patterns: {
        vocabulary: {
          commonWords: [],
          rareWords: [],
          technicalTerms: [],
        },
        sentenceStructure: {
          avgSentenceLength: 0,
          avgWordLength: 0,
          sentenceComplexity: 0,
        },
        sentiment: {
          avgSentiment: 0,
          sentimentVariance: 0,
        },
        timing: {
          avgTypingSpeed: 0,
          typingVariance: 0,
          messageFrequency: 0,
        },
        style: {
          formality: 0.5,
          emojiUsage: 0.5,
          punctuation: 0.5,
        },
      },
    };
  }
  
  /**
   * Save baseline to storage
   */
  _saveBaseline() {
    try {
      const dir = path.dirname(this.config.baselinePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      this.baseline.lastUpdated = new Date().toISOString();
      fs.writeFileSync(this.config.baselinePath, JSON.stringify(this.baseline, null, 2));
      console.log('💾 Behavioral baseline saved');
    } catch (error) {
      console.error('❌ Error saving baseline:', error.message);
    }
  }
  
  /**
   * Analyze message for behavioral patterns
   */
  async analyzeMessage(message, context = {}) {
    try {
      // Check if in lockdown mode
      if (this._isInLockdown()) {
        return {
          success: false,
          locked: true,
          message: 'System is in lockdown mode. Please provide passphrase to continue.',
        };
      }
      
      // Extract linguistic features
      const features = await this._extractFeatures(message, context);
      
      // Calculate confidence score
      const confidence = this._calculateConfidence(features);
      
      // Check if message contains destructive command
      const isDestructive = this._isDestructiveCommand(message);
      
      // Update baseline with new data
      this._updateBaseline(features);
      
      // Determine if action is allowed
      const actionAllowed = this._isActionAllowed(confidence, isDestructive);
      
      return {
        success: true,
        confidence: confidence,
        isDestructive: isDestructive,
        actionAllowed: actionAllowed,
        features: features,
        locked: false,
      };
    
    } catch (error) {
      console.error('❌ Error analyzing message:', error.message);
      return {
        success: false,
        error: error.message,
        confidence: 0,
        actionAllowed: false,
      };
    }
  }
  
  /**
   * Extract linguistic features from message
   */
  async _extractFeatures(message, context) {
    try {
      const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
      const model = genAI.getGenerativeModel({
        model: 'gemini-1.5-flash',
        systemInstruction: `Extract linguistic features from the message.
Return JSON with:
- vocabulary: { commonWords, rareWords, technicalTerms }
- sentenceStructure: { avgSentenceLength, avgWordLength, sentenceComplexity }
- sentiment: { sentiment, intensity }
- style: { formality, emojiUsage, punctuation }`,
      });
      
      const result = await model.generateContent(message);
      const features = JSON.parse(result.response.text());
      
      return features;
    
    } catch (error) {
      console.error('Error extracting features:', error.message);
      // Fallback to simple extraction
      return this._simpleFeatureExtraction(message);
    }
  }
  
  /**
   * Simple feature extraction (fallback)
   */
  _simpleFeatureExtraction(message) {
    const words = message.toLowerCase().split(/\s+/);
    const sentences = message.split(/[.!?]+/);
    
    return {
      vocabulary: {
        commonWords: words.slice(0, 10),
        rareWords: [],
        technicalTerms: [],
      },
      sentenceStructure: {
        avgSentenceLength: words.length / Math.max(sentences.length, 1),
        avgWordLength: words.join('').length / Math.max(words.length, 1),
        sentenceComplexity: 0.5,
      },
      sentiment: {
        sentiment: 0,
        intensity: 0,
      },
      style: {
        formality: 0.5,
        emojiUsage: (message.match(/[\p{Emoji}]/gu) || []).length / message.length,
        punctuation: (message.match(/[.,!?]/g) || []).length / message.length,
      },
    };
  }
  
  /**
   * Calculate confidence score based on features
   */
  _calculateConfidence(features) {
    if (!this.baseline || this.baseline.sampleSize < 10) {
      // Not enough baseline data, return moderate confidence
      return 0.5;
    }
    
    let confidence = 0;
    let factors = 0;
    
    // Vocabulary similarity
    const vocabSimilarity = this._calculateVocabularySimilarity(features.vocabulary);
    confidence += vocabSimilarity * 0.3;
    factors++;
    
    // Sentence structure similarity
    const structureSimilarity = this._calculateStructureSimilarity(features.sentenceStructure);
    confidence += structureSimilarity * 0.25;
    factors++;
    
    // Style similarity
    const styleSimilarity = this._calculateStyleSimilarity(features.style);
    confidence += styleSimilarity * 0.25;
    factors++;
    
    // Sentiment similarity
    const sentimentSimilarity = this._calculateSentimentSimilarity(features.sentiment);
    confidence += sentimentSimilarity * 0.2;
    factors++;
    
    return confidence / factors;
  }
  
  /**
   * Calculate vocabulary similarity
   */
  _calculateVocabularySimilarity(vocabulary) {
    const baselineVocab = this.baseline.patterns.vocabulary;
    
    // Check common words overlap
    const commonOverlap = vocabulary.commonWords.filter(word =>
      baselineVocab.commonWords.includes(word)
    ).length;
    
    const commonSimilarity = commonOverlap / Math.max(vocabulary.commonWords.length, 1);
    
    return commonSimilarity;
  }
  
  /**
   * Calculate sentence structure similarity
   */
  _calculateStructureSimilarity(structure) {
    const baselineStructure = this.baseline.patterns.sentenceStructure;
    
    const lengthDiff = Math.abs(structure.avgSentenceLength - baselineStructure.avgSentenceLength);
    const lengthSimilarity = 1 - Math.min(lengthDiff / 10, 1);
    
    const wordDiff = Math.abs(structure.avgWordLength - baselineStructure.avgWordLength);
    const wordSimilarity = 1 - Math.min(wordDiff / 2, 1);
    
    return (lengthSimilarity + wordSimilarity) / 2;
  }
  
  /**
   * Calculate style similarity
   */
  _calculateStyleSimilarity(style) {
    const baselineStyle = this.baseline.patterns.style;
    
    const formalityDiff = Math.abs(style.formality - baselineStyle.formality);
    const formalitySimilarity = 1 - formalityDiff;
    
    const emojiDiff = Math.abs(style.emojiUsage - baselineStyle.emojiUsage);
    const emojiSimilarity = 1 - Math.min(emojiDiff * 10, 1);
    
    const punctDiff = Math.abs(style.punctuation - baselineStyle.punctuation);
    const punctSimilarity = 1 - Math.min(punctDiff * 5, 1);
    
    return (formalitySimilarity + emojiSimilarity + punctSimilarity) / 3;
  }
  
  /**
   * Calculate sentiment similarity
   */
  _calculateSentimentSimilarity(sentiment) {
    const baselineSentiment = this.baseline.patterns.sentiment;
    
    const sentimentDiff = Math.abs(sentiment.sentiment - baselineSentiment.avgSentiment);
    return 1 - Math.min(sentimentDiff, 1);
  }
  
  /**
   * Check if message contains destructive command
   */
  _isDestructiveCommand(message) {
    const messageLower = message.toLowerCase();
    return this.config.destructiveCommands.some(cmd =>
      messageLower.includes(cmd)
    );
  }
  
  /**
   * Determine if action is allowed
   */
  _isActionAllowed(confidence, isDestructive) {
    // If not destructive, allow with moderate confidence
    if (!isDestructive) {
      return confidence >= 0.4;
    }
    
    // If destructive, require high confidence
    return confidence >= this.config.confidenceThreshold;
  }
  
  /**
   * Update baseline with new features
   */
  _updateBaseline(features) {
    if (!this.baseline) {
      this.baseline = this._createDefaultBaseline();
    }
    
    // Update vocabulary
    this.baseline.patterns.vocabulary.commonWords.push(...features.vocabulary.commonWords);
    this.baseline.patterns.vocabulary.commonWords = [...new Set(this.baseline.patterns.vocabulary.commonWords)];
    
    // Update sentence structure (moving average)
    const oldSize = this.baseline.sampleSize;
    const newSize = oldSize + 1;
    
    this.baseline.patterns.sentenceStructure.avgSentenceLength =
      (this.baseline.patterns.sentenceStructure.avgSentenceLength * oldSize + features.sentenceStructure.avgSentenceLength) / newSize;
    
    this.baseline.patterns.sentenceStructure.avgWordLength =
      (this.baseline.patterns.sentenceStructure.avgWordLength * oldSize + features.sentenceStructure.avgWordLength) / newSize;
    
    // Update style
    this.baseline.patterns.style.formality =
      (this.baseline.patterns.style.formality * oldSize + features.style.formality) / newSize;
    
    this.baseline.patterns.style.emojiUsage =
      (this.baseline.patterns.style.emojiUsage * oldSize + features.style.emojiUsage) / newSize;
    
    this.baseline.sampleSize = newSize;
    
    // Save periodically
    if (newSize % 10 === 0) {
      this._saveBaseline();
    }
  }
  
  /**
   * Check if system is in lockdown mode
   */
  _isInLockdown() {
    if (!this.lockdownMode) {
      return false;
    }
    
    if (this.lockdownUntil && new Date() > this.lockdownUntil) {
      this.lockdownMode = false;
      this.lockdownUntil = null;
      this.failedAttempts = 0;
      console.log('🔓 Lockdown mode expired');
      return false;
    }
    
    return true;
  }
  
  /**
   * Trigger lockdown mode
   */
  triggerLockdown() {
    this.lockdownMode = true;
    this.lockdownUntil = new Date(Date.now() + this.config.lockdownDuration);
    this.failedAttempts++;
    
    console.log(`🔒 Lockdown mode triggered until ${this.lockdownUntil.toISOString()}`);
    
    return {
      locked: true,
      until: this.lockdownUntil.toISOString(),
      attempts: this.failedAttempts,
    };
  }
  
  /**
   * Verify passphrase to exit lockdown
   */
  verifyPassphrase(passphrase) {
    if (!this.lockdownMode) {
      return { success: true, message: 'Not in lockdown mode' };
    }
    
    if (passphrase === this.lockdownPassphrase) {
      this.lockdownMode = false;
      this.lockdownUntil = null;
      this.failedAttempts = 0;
      console.log('🔓 Lockdown mode lifted by passphrase');
      
      return { success: true, message: 'Lockdown mode lifted' };
    } else {
      this.failedAttempts++;
      console.log(`❌ Incorrect passphrase. Attempts: ${this.failedAttempts}`);
      
      // Fail-safe: if too many failed attempts, reset lockdown
      if (this.failedAttempts >= this.config.maxFailedAttempts * 2) {
        this.lockdownMode = false;
        this.lockdownUntil = null;
        this.failedAttempts = 0;
        console.log('⚠️ Fail-safe: Lockdown reset due to too many failed attempts');
        
        return {
          success: true,
          message: 'Fail-safe: Lockdown reset due to too many failed attempts',
          failSafe: true,
        };
      }
      
      return {
        success: false,
        message: 'Incorrect passphrase',
        attempts: this.failedAttempts,
      };
    }
  }
  
  /**
   * Emergency override (fail-safe)
   */
  emergencyOverride() {
    console.log('🚨 Emergency override triggered');
    this.lockdownMode = false;
    this.lockdownUntil = null;
    this.failedAttempts = 0;
    
    return { success: true, message: 'Emergency override successful' };
  }
  
  /**
   * Get security status
   */
  getSecurityStatus() {
    return {
      lockdownMode: this.lockdownMode,
      lockdownUntil: this.lockdownUntil?.toISOString(),
      failedAttempts: this.failedAttempts,
      baselineSampleSize: this.baseline?.sampleSize || 0,
      confidenceThreshold: this.config.confidenceThreshold,
      maxFailedAttempts: this.config.maxFailedAttempts,
    };
  }
  
  /**
   * Train baseline from historical messages
   */
  async trainFromHistory(messages) {
    try {
      console.log(`🎓 Training baseline from ${messages.length} messages...`);
      
      for (const message of messages) {
        const features = await this._extractFeatures(message.content, message.context);
        this._updateBaseline(features);
      }
      
      this._saveBaseline();
      
      console.log('✅ Baseline training complete');
      
      return {
        success: true,
        sampleSize: this.baseline.sampleSize,
      };
    
    } catch (error) {
      console.error('❌ Error training baseline:', error.message);
      return {
        success: false,
        error: error.message,
      };
    }
  }
}

// Singleton instance
let behavioralBiometrics = null;

function getBehavioralBiometrics(config = null) {
  if (!behavioralBiometrics) {
    if (config === null) {
      config = {};
    }
    behavioralBiometrics = new BehavioralBiometrics(config);
  }
  return behavioralBiometrics;
}

module.exports = { BehavioralBiometrics, getBehavioralBiometrics };
