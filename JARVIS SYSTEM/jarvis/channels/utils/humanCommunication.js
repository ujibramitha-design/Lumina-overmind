/**
 * JARVIS Human Communication Utilities
 * ===================================
 * 
 * Utilities for making JARVIS responses feel more human:
 * - Message splitting to avoid wall-of-text
 * - Dynamic typing delays
 * - Natural conversation flow
 * - Thinking placeholders
 */

/**
 * Split a long message into natural chunks
 * Splits by sentences or paragraphs to create natural conversation flow
 * 
 * @param {string} message - The message to split
 * @param {Object} options - Splitting options
 * @returns {Array<string>} Array of message chunks
 */
function splitMessage(message, options = {}) {
  const {
    maxChunkLength = 300,  // Max characters per chunk
    splitBy = 'sentence',  // 'sentence' or 'paragraph'
    preserveFormatting = true,
  } = options;
  
  if (!message || message.length <= maxChunkLength) {
    return [message];
  }
  
  const chunks = [];
  
  if (splitBy === 'sentence') {
    // Split by sentences
    const sentences = message.match(/[^.!?]+[.!?]+["']?|[^.!?]+$/g) || [message];
    
    let currentChunk = '';
    
    for (const sentence of sentences) {
      const trimmedSentence = sentence.trim();
      
      if (!trimmedSentence) continue;
      
      // If adding this sentence would exceed max length
      if (currentChunk.length + trimmedSentence.length > maxChunkLength && currentChunk) {
        chunks.push(currentChunk.trim());
        currentChunk = trimmedSentence;
      } else {
        currentChunk += (currentChunk ? ' ' : '') + trimmedSentence;
      }
    }
    
    if (currentChunk) {
      chunks.push(currentChunk.trim());
    }
  } else if (splitBy === 'paragraph') {
    // Split by paragraphs
    const paragraphs = message.split(/\n\n+/);
    
    for (const paragraph of paragraphs) {
      const trimmedParagraph = paragraph.trim();
      
      if (!trimmedParagraph) continue;
      
      // If paragraph is too long, split it further
      if (trimmedParagraph.length > maxChunkLength) {
        const subChunks = splitMessage(trimmedParagraph, {
          maxChunkLength,
          splitBy: 'sentence',
          preserveFormatting,
        });
        chunks.push(...subChunks);
      } else {
        chunks.push(trimmedParagraph);
      }
    }
  }
  
  return chunks;
}

/**
 * Calculate typing delay based on message length
 * Simulates human typing speed
 * 
 * @param {string} message - The message to calculate delay for
 * @param {Object} options - Delay options
 * @returns {number} Delay in milliseconds
 */
function calculateTypingDelay(message, options = {}) {
  const {
    baseDelay = 500,      // Base delay in ms
    charsPerSecond = 20,  // Typing speed
    variance = 0.3,        // Random variance (30%)
    minDelay = 300,       // Minimum delay
    maxDelay = 3000,      // Maximum delay
  } = options;
  
  const messageLength = message.length;
  const calculatedDelay = (messageLength / charsPerSecond) * 1000 + baseDelay;
  
  // Add random variance
  const randomVariance = calculatedDelay * variance * (Math.random() * 2 - 1);
  const finalDelay = calculatedDelay + randomVariance;
  
  // Clamp to min/max
  return Math.max(minDelay, Math.min(maxDelay, finalDelay));
}

/**
 * Send a message with human-like typing delay
 * 
 * @param {Function} sendFunction - Function to send the message
 * @param {string} message - The message to send
 * @param {Object} options - Options
 */
async function sendWithTypingDelay(sendFunction, message, options = {}) {
  const {
    showTyping = true,
    typingIndicator = 'typing...',
    splitChunks = true,
    chunkDelay = 1000,  // Delay between chunks
  } = options;
  
  try {
    // Show typing indicator if enabled
    if (showTyping) {
      await sendFunction(typingIndicator);
    }
    
    // Calculate typing delay
    const delay = calculateTypingDelay(message);
    await new Promise(resolve => setTimeout(resolve, delay));
    
    // Remove typing indicator (send empty message or delete)
    if (showTyping) {
      // This depends on the platform's implementation
      // For now, we'll just proceed
    }
    
    // Split message into chunks if enabled
    if (splitChunks) {
      const chunks = splitMessage(message);
      
      for (let i = 0; i < chunks.length; i++) {
        const chunk = chunks[i];
        
        // Send chunk
        await sendFunction(chunk);
        
        // Add delay between chunks (except last)
        if (i < chunks.length - 1) {
          const interChunkDelay = calculateTypingDelay(chunk) * 0.5;
          await new Promise(resolve => setTimeout(resolve, interChunkDelay));
        }
      }
    } else {
      // Send full message
      await sendFunction(message);
    }
    
  } catch (error) {
    console.error('Error in sendWithTypingDelay:', error);
    // Fallback: send message immediately
    await sendFunction(message);
  }
}

/**
 * Send a "thinking" placeholder before processing
 * 
 * @param {Function} sendFunction - Function to send the message
 * @param {Object} options - Options
 */
async function sendThinkingPlaceholder(sendFunction, options = {}) {
  const {
    placeholders = [
      'Give me a sec...',
      'Let me think about this...',
      'Hmm, interesting question...',
      'Processing...',
      'One moment...',
      'Analyzing...',
    ],
    duration = 2000,  // How long to show placeholder
  } = options;
  
  try {
    // Select random placeholder
    const placeholder = placeholders[Math.floor(Math.random() * placeholders.length)];
    
    // Send placeholder
    await sendFunction(placeholder);
    
    // Wait for duration
    await new Promise(resolve => setTimeout(resolve, duration));
    
    // Note: The placeholder will be replaced by the actual response
    // This depends on the platform's implementation
    
  } catch (error) {
    console.error('Error in sendThinkingPlaceholder:', error);
  }
}

/**
 * Format message with human-like elements
 * Adds occasional emojis, casual language markers, etc.
 * 
 * @param {string} message - The message to format
 * @param {Object} persona - Persona configuration
 * @returns {string} Formatted message
 */
function formatMessageWithPersona(message, persona = {}) {
  const {
    formality = 'formal',  // 'formal', 'casual', 'friendly'
    useEmojis = true,
    useCasualMarkers = false,
  } = persona;
  
  let formattedMessage = message;
  
  // Add emojis based on formality
  if (useEmojis) {
    if (formality === 'formal') {
      // Minimal emojis for formal
      const formalEmojis = ['✅', '❌', '⚠️', '📊', '🔍'];
      // Only add if message doesn't already have emojis
      if (!/\p{Emoji}/u.test(formattedMessage)) {
        // Add appropriate emoji based on content
        if (formattedMessage.includes('error') || formattedMessage.includes('fail')) {
          formattedMessage = '❌ ' + formattedMessage;
        } else if (formattedMessage.includes('success') || formattedMessage.includes('done')) {
          formattedMessage = '✅ ' + formattedMessage;
        }
      }
    } else if (formality === 'casual') {
      // More emojis for casual
      const casualEmojis = ['👍', '🤔', '😊', '🎉', '💡', '🚀'];
      // Add random emoji occasionally
      if (Math.random() > 0.7) {
        const emoji = casualEmojis[Math.floor(Math.random() * casualEmojis.length)];
        formattedMessage = emoji + ' ' + formattedMessage;
      }
    } else if (formality === 'friendly') {
      // Friendly emojis
      const friendlyEmojis = ['😄', '🤗', '✨', '🌟', '💪', '🙌'];
      if (Math.random() > 0.5) {
        const emoji = friendlyEmojis[Math.floor(Math.random() * friendlyEmojis.length)];
        formattedMessage = emoji + ' ' + formattedMessage;
      }
    }
  }
  
  // Add casual markers for less formal personas
  if (useCasualMarkers && formality !== 'formal') {
    const casualMarkers = ['Btw,', 'Actually,', 'You know,', 'Honestly,'];
    if (Math.random() > 0.8) {
      const marker = casualMarkers[Math.floor(Math.random() * casualMarkers.length)];
      formattedMessage = marker + ' ' + formattedMessage.charAt(0).toLowerCase() + formattedMessage.slice(1);
    }
  }
  
  return formattedMessage;
}

/**
 * Generate a natural conversation opener
 * 
 * @param {Object} context - Conversation context
 * @returns {string} Natural opener
 */
function generateNaturalOpener(context = {}) {
  const {
    timeSinceLastInteraction = 0,  // Hours
    previousTopic = null,
    persona = 'formal',
  } = context;
  
  const openers = {
    formal: [
      'Good to hear from you.',
      'How can I assist you today?',
      'I\'m here to help.',
    ],
    casual: [
      'Hey there!',
      'What\'s on your mind?',
      'What\'s up?',
    ],
    friendly: [
      'Hey! Long time no see!',
      'Good to see you again!',
      'How have you been?',
    ],
  };
  
  const personaOpeners = openers[persona] || openers.formal;
  
  // If it's been a while, use a different opener
  if (timeSinceLastInteraction > 24) {
    return persona === 'friendly' 
      ? 'Hey! It\'s been a while. How\'ve you been?'
      : 'Good to hear from you again.';
  }
  
  return personaOpeners[Math.floor(Math.random() * personaOpeners.length)];
}

/**
 * Add natural conversation filler
 * 
 * @param {string} message - The message
 * @param {Object} options - Options
 * @returns {string} Message with filler
 */
function addNaturalFiller(message, options = {}) {
  const {
    probability = 0.2,  // 20% chance to add filler
    fillers = [
      'Actually,',
      'To be honest,',
      'You know,',
      'I think,',
      'Well,',
    ],
  } = options;
  
  if (Math.random() > probability) {
    return message;
  }
  
  const filler = fillers[Math.floor(Math.random() * fillers.length)];
  return `${filler} ${message.charAt(0).toLowerCase()}${message.slice(1)}`;
}

module.exports = {
  splitMessage,
  calculateTypingDelay,
  sendWithTypingDelay,
  sendThinkingPlaceholder,
  formatMessageWithPersona,
  generateNaturalOpener,
  addNaturalFiller,
};
