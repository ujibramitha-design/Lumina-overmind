# JARVIS Gemini AI Integration Guide

Complete guide for integrating Google Gemini AI as the primary LLM brain for JARVIS.

## Overview

JARVIS uses Google Gemini API for intelligent responses with three specialized models:
- **gemini-1.5-flash** - Fast conversational responses
- **gemini-1.5-pro** - Heavy codebase reading and analysis
- **gemini-1.5-pro** - Deep system analysis

## Setup

### 1. Install Dependencies

```bash
cd jarvis/channels
npm install
```

### 2. Configure Environment Variables

Update `.env` file:

```bash
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Verify Installation

```bash
node -e "const { getGeminiService } = require('./services/geminiService'); const service = getGeminiService(); service.healthCheck().then(console.log);"
```

## Usage Examples

### Basic Conversational Response

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Generate response
const result = await geminiService.generateResponse(
  'user_123',           // userId
  'What is the system status?',  // message
  {
    platform: 'telegram',
    username: 'john_doe',
    timestamp: new Date().toISOString(),
  }
);

console.log(result.response);
```

### Codebase Analysis

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Analyze code
const code = `
function calculateMetrics(data) {
  return data.reduce((acc, item) => {
    acc.total += item.value;
    return acc;
  }, { total: 0 });
}
`;

const result = await geminiService.analyzeCodebase(
  'user_123',
  code,
  'Explain this function and suggest improvements',
  {
    file: 'utils/metrics.js',
    context: 'This is used for system monitoring',
  }
);

console.log(result.response);
```

### Deep Analysis

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Perform analysis
const result = await geminiService.performAnalysis(
  'user_123',
  {
    cpu: 85,
    memory: 92,
    disk: 45,
    errors: ['Connection timeout', 'Database lock'],
  },
  'system_performance',
  {
    timeRange: 'last_hour',
    severity: 'high',
  }
);

console.log(result.response);
```

## Channel Integration

### Telegram Webhook Integration

```javascript
const { getGeminiService } = require('../services/geminiService');

// In telegram/bot.js
async generateJarvisResponse(messageData) {
  try {
    const geminiService = getGeminiService();
    
    const result = await geminiService.generateResponse(
      messageData.from.id,
      messageData.message,
      {
        platform: 'telegram',
        username: messageData.from.username,
        timestamp: messageData.timestamp,
      }
    );
    
    if (result.success) {
      await this.sendMessage(messageData.chatId, result.response);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

### WhatsApp Integration

```javascript
const { getGeminiService } = require('../services/geminiService');

// In whatsapp/client.js
async generateJarvisResponse(messageData, originalMessage) {
  try {
    const geminiService = getGeminiService();
    
    const result = await geminiService.generateResponse(
      messageData.from.id,
      messageData.message,
      {
        platform: 'whatsapp',
        phoneNumber: messageData.from.id,
        timestamp: messageData.timestamp,
      }
    );
    
    if (result.success) {
      await originalMessage.reply(result.response);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

### WebSocket Integration (Mobile APK)

```javascript
const { getGeminiService } = require('./services/geminiService');

// In WebSocket handler
async handleChatMessage(data) {
  try {
    const geminiService = getGeminiService();
    
    const result = await geminiService.generateResponse(
      data.userId,
      data.message,
      {
        platform: 'mobile',
        device: data.deviceInfo,
        timestamp: data.timestamp,
      }
    );
    
    // Send response via WebSocket
    websocket.send(JSON.stringify({
      type: 'chat_response',
      data: {
        message: result.response,
        sender: 'jarvis',
        timestamp: new Date().toISOString(),
      },
    }));
  } catch (error) {
    console.error('Error:', error.message);
  }
}
```

## Conversation History Management

### Get Conversation History

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Get history for a user
const history = geminiService._getConversationHistory('user_123');
console.log(history);
```

### Clear Conversation History

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Clear history for a user
geminiService.clearConversationHistory('user_123');
```

### Get Conversation Statistics

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Get overall statistics
const stats = geminiService.getConversationStats();
console.log(stats);
// Output:
// {
//   totalUsers: 5,
//   totalMessages: 150,
//   usersWithHistory: [...]
// }
```

## System Prompts

### Conversational System Prompt

The conversational model uses a system prompt that defines JARVIS as:
- Autonomous, hyper-intelligent AI assistant
- Deeply integrated into Lumina Overmind
- Professional, concise communication
- Senior Software Engineer persona for code
- Proactive and context-aware

### Codebase System Prompt

The codebase model uses a system prompt that:
- Acts as codebase intelligence system
- Provides accurate technical explanations
- Suggests improvements and best practices
- Understands Lumina Overmind architecture

### Analysis System Prompt

The analysis model uses a system prompt that:
- Performs in-depth data analysis
- Generates comprehensive reports
- Identifies trends and patterns
- Provides actionable insights

## Configuration

### Model Selection

```javascript
const geminiService = getGeminiService();

// Available models
console.log(geminiService.models);
// {
//   conversational: 'gemini-1.5-flash',
//   codebase: 'gemini-1.5-pro',
//   analysis: 'gemini-1.5-pro',
// }
```

### History Length

```javascript
// In geminiService.js
this.maxHistoryLength = 20; // Keep last 20 messages per user
```

### Health Check

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

const health = await geminiService.healthCheck();
console.log(health);
// {
//   status: 'healthy',
//   models: {...},
//   conversationStats: {...},
//   timestamp: '2024-01-15T10:30:00.000Z'
// }
```

## Error Handling

### Basic Error Handling

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

try {
  const result = await geminiService.generateResponse('user_123', 'Hello');
  
  if (result.success) {
    console.log(result.response);
  } else {
    console.error('Generation failed:', result.error);
    // Use fallback response
    console.log(result.response); // Fallback message
  }
} catch (error) {
  console.error('Service error:', error.message);
  // Handle service-level errors
}
```

### Fallback Responses

Gemini service provides fallback responses when generation fails:
- Conversational: "I apologize, but I encountered an error processing your request."
- Codebase: "I apologize, but I encountered an error analyzing the code."
- Analysis: "I apologize, but I encountered an error performing the analysis."

## Performance Tips

### 1. Use Appropriate Models

- Use `gemini-1.5-flash` for quick conversations
- Use `gemini-1.5-pro` for complex code analysis
- Use `gemini-1.5-pro` for deep system analysis

### 2. Manage Conversation History

- Clear history periodically to reduce context
- Use `maxHistoryLength` to limit memory usage
- Implement history cleanup in scheduler

### 3. Batch Requests

For multiple users, process requests asynchronously:

```javascript
const users = ['user_1', 'user_2', 'user_3'];
const messages = ['Hello', 'Status?', 'Help'];

const promises = users.map((userId, index) =>
  geminiService.generateResponse(userId, messages[index])
);

const results = await Promise.all(promises);
```

### 4. Cache Responses

Cache common responses to reduce API calls:

```javascript
const cache = new Map();

async function getCachedResponse(userId, message) {
  const cacheKey = `${userId}:${message}`;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  
  const result = await geminiService.generateResponse(userId, message);
  cache.set(cacheKey, result);
  
  return result;
}
```

## Security

### API Key Security

- Never commit API keys to version control
- Use environment variables
- Rotate API keys regularly
- Monitor API usage in Google Cloud Console

### Rate Limiting

Gemini API has rate limits. Implement rate limiting:

```javascript
const rateLimiter = new Map();

async function checkRateLimit(userId) {
  const now = Date.now();
  const userRequests = rateLimiter.get(userId) || [];
  
  // Remove requests older than 1 minute
  const recentRequests = userRequests.filter(r => now - r < 60000);
  
  if (recentRequests.length >= 30) { // 30 requests per minute
    throw new Error('Rate limit exceeded');
  }
  
  recentRequests.push(now);
  rateLimiter.set(userId, recentRequests);
}
```

## Troubleshooting

### API Key Not Found

**Error:** `GEMINI_API_KEY not found in environment variables`

**Solution:**
```bash
# Check .env file
cat .env | grep GEMINI_API_KEY

# Ensure .env is loaded
require('dotenv').config();
```

### Model Initialization Failed

**Error:** `Failed to initialize Gemini models`

**Solution:**
- Verify API key is valid
- Check internet connection
- Verify Google Cloud project has Gemini API enabled

### Rate Limit Exceeded

**Error:** `429 Too Many Requests`

**Solution:**
- Implement rate limiting
- Use exponential backoff
- Consider upgrading to paid tier

### Context Too Long

**Error:** `Context length exceeded`

**Solution:**
- Reduce conversation history length
- Clear old history
- Summarize old conversations

## Monitoring

### Track API Usage

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Get conversation stats
const stats = geminiService.getConversationStats();
console.log(`Total users: ${stats.totalUsers}`);
console.log(`Total messages: ${stats.totalMessages}`);
```

### Log Response Times

```javascript
const startTime = Date.now();
const result = await geminiService.generateResponse('user_123', 'Hello');
const responseTime = Date.now() - startTime;

console.log(`Response time: ${responseTime}ms`);
```

## Best Practices

1. **Always handle errors gracefully**
2. **Use appropriate models for tasks**
3. **Manage conversation history**
4. **Implement rate limiting**
5. **Monitor API usage**
6. **Cache common responses**
7. **Provide fallback responses**
8. **Log important events**
9. **Test thoroughly before production**
10. **Keep API keys secure**

## Support

For issues or questions:
- Check Google Gemini API documentation
- Review conversation logs
- Verify API key and configuration
- Test with simple prompts first
- Monitor Google Cloud Console for errors
