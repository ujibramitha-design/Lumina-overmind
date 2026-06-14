/**
 * JARVIS Language Detector
 * ========================
 * 
 * Auto-detects the language of incoming messages
 * using Gemini AI for accurate language identification.
 */

const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

class LanguageDetector {
  constructor() {
    this.genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    this.detectionModel = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      systemInstruction: `You are a language detection expert. Identify the language of the given text and return the ISO 639-1 language code.

Supported languages:
- English (en)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)
- Spanish (es)
- French (fr)
- German (de)
- Russian (ru)
- Arabic (ar)
- Portuguese (pt)
- Italian (it)
- Dutch (nl)
- Polish (pl)
- Turkish (tr)
- Vietnamese (vi)
- Thai (th)
- Indonesian (id)
- Hindi (hi)
- Bengali (bn)
- Swedish (sv)
- Norwegian (no)
- Danish (da)
- Finnish (fi)

Return only the language code (e.g., "en", "ja", "ko").`,
    });
  }
  
  /**
   * Detect language of text
   */
  async detectLanguage(text) {
    try {
      // Quick check for common patterns
      const quickDetection = this._quickDetect(text);
      if (quickDetection) {
        return quickDetection;
      }
      
      // Use Gemini for accurate detection
      const result = await this.detectionModel.generateContent(text);
      const detectedLanguage = result.response.text().trim().toLowerCase();
      
      // Validate language code
      const validLanguages = [
        'en', 'ja', 'ko', 'zh', 'es', 'fr', 'de', 'ru', 'ar',
        'pt', 'it', 'nl', 'pl', 'tr', 'vi', 'th', 'id', 'hi',
        'bn', 'sv', 'no', 'da', 'fi',
      ];
      
      if (validLanguages.includes(detectedLanguage)) {
        return detectedLanguage;
      }
      
      // Default to English if invalid
      return 'en';
      
    } catch (error) {
      console.error('Error detecting language:', error.message);
      return 'en';  // Default to English
    }
  }
  
  /**
   * Quick detection for common patterns
   */
  _quickDetect(text) {
    // Check for Japanese characters
    if (/[\u3040-\u309F\u30A0-\u30FF]/.test(text)) {
      return 'ja';
    }
    
    // Check for Korean characters
    if (/[\uAC00-\uD7AF\u1100-\u11FF]/.test(text)) {
      return 'ko';
    }
    
    // Check for Chinese characters
    if (/[\u4E00-\u9FFF]/.test(text)) {
      return 'zh';
    }
    
    // Check for Arabic characters
    if (/[\u0600-\u06FF]/.test(text)) {
      return 'ar';
    }
    
    // Check for Thai characters
    if (/[\u0E00-\u0E7F]/.test(text)) {
      return 'th';
    }
    
    // Check for Vietnamese
    if (/[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỉĩ]/.test(text)) {
      return 'vi';
    }
    
    // Check for Cyrillic (Russian)
    if (/[\u0400-\u04FF]/.test(text)) {
      return 'ru';
    }
    
    // Check for Devanagari (Hindi)
    if (/[\u0900-\u097F]/.test(text)) {
      return 'hi';
    }
    
    // Check for Bengali
    if (/[\u0980-\u09FF]/.test(text)) {
      return 'bn';
    }
    
    return null;  // Cannot detect quickly, use Gemini
  }
  
  /**
   * Detect language with confidence
   */
  async detectLanguageWithConfidence(text) {
    try {
      const language = await this.detectLanguage(text);
      
      // Calculate confidence based on character patterns
      const confidence = this._calculateConfidence(text, language);
      
      return {
        language: language,
        confidence: confidence,
      };
      
    } catch (error) {
      console.error('Error detecting language with confidence:', error.message);
      return {
        language: 'en',
        confidence: 0.5,
      };
    }
  }
  
  /**
   * Calculate confidence score
   */
  _calculateConfidence(text, language) {
    // High confidence for languages with unique scripts
    const uniqueScriptLanguages = ['ja', 'ko', 'zh', 'ar', 'th', 'hi', 'bn'];
    
    if (uniqueScriptLanguages.includes(language)) {
      return 0.95;
    }
    
    // Medium confidence for Latin-script languages
    const latinScriptLanguages = ['es', 'fr', 'de', 'pt', 'it', 'nl', 'pl', 'sv', 'no', 'da', 'fi'];
    
    if (latinScriptLanguages.includes(language)) {
      return 0.75;
    }
    
    // Lower confidence for English (default)
    return 0.6;
  }
}

// Singleton instance
let languageDetector = null;

function getLanguageDetector() {
  if (!languageDetector) {
    languageDetector = new LanguageDetector();
  }
  return languageDetector;
}

module.exports = { LanguageDetector, getLanguageDetector };
