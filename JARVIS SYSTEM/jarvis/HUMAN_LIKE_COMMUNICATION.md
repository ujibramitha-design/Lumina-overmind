# JARVIS Human-Like Communication Guide

Complete guide for making JARVIS feel 100% human with natural conversation flow, spontaneity, and relationship evolution.

## Overview

JARVIS now exhibits human communication quirks through:
- **Message Splitting**: Breaks long responses into natural chunks
- **Typing Delays**: Simulates human typing speed with variance
- **Dynamic Persona**: Evolves relationship based on interaction count
- **Spontaneity**: Initiates conversations autonomously based on inactivity

## Message Splitting

### How It Works

Long AI responses are split into natural chunks to avoid wall-of-text:

**Before (Robotic):**
```
I've analyzed the code and found several issues. First, the error handling is incomplete. Second, the performance could be improved by caching. Third, the documentation needs updating. Fourth, the tests are failing. Finally, the deployment process is manual and should be automated.
```

**After (Human-like):**
```
I've analyzed the code and found several issues.

First, the error handling is incomplete.

Second, the performance could be improved by caching.

Third, the documentation needs updating.
```

### Implementation

```javascript
const { splitMessage } = require('../utils/humanCommunication');

// Split by sentences (default)
const chunks = splitMessage(longMessage, {
  maxChunkLength: 300,
  splitBy: 'sentence',
});

// Split by paragraphs
const chunks = splitMessage(longMessage, {
  maxChunkLength: 300,
  splitBy: 'paragraph',
});
```

### Usage in Handlers

**WhatsApp:**
```javascript
await sendWithTypingDelay(
  async (msg) => await originalMessage.reply(msg),
  formattedMessage,
  {
    showTyping: true,
    splitChunks: true,
    chunkDelay: 1000,
  }
);
```

**Telegram:**
```javascript
await sendWithTypingDelay(
  async (msg) => await this.sendMessage(chatId, msg),
  formattedMessage,
  {
    showTyping: true,
    splitChunks: true,
    chunkDelay: 1000,
  }
);
```

## Typing Delays

### How It Works

Simulates human typing speed with random variance:

**Calculation:**
```javascript
delay = (message_length / chars_per_second) * 1000 + base_delay
final_delay = delay + (delay * variance * (random * 2 - 1))
```

**Example:**
- 100 character message
- 20 chars/second typing speed
- 500ms base delay
- 30% variance
- Result: ~5-7 seconds with random variation

### Configuration

```javascript
const delay = calculateTypingDelay(message, {
  baseDelay: 500,      // Base delay in ms
  charsPerSecond: 20,  // Typing speed
  variance: 0.3,        // 30% random variance
  minDelay: 300,       // Minimum delay
  maxDelay: 3000,      // Maximum delay
});
```

### Thinking Placeholders

Before processing heavy tasks, JARVIS shows a thinking placeholder:

```javascript
await sendThinkingPlaceholder(sendFunction, {
  placeholders: [
    'Give me a sec...',
    'Let me think about this...',
    'Hmm, interesting question...',
    'Processing...',
    'One moment...',
    'Analyzing...',
  ],
  duration: 2000,  // 2 seconds
});
```

## Dynamic Persona

### Relationship Evolution

JARVIS's personality evolves based on interaction count:

| Interactions | Persona | Address | Tone | Emojis |
|--------------|---------|---------|------|--------|
| 0-99 | Formal | Tuan/Sir | Professional | Minimal |
| 100-499 | Casual | Hey there | Approachable | Occasional |
| 500+ | Friendly | Hey! | Conversational | Frequent |

### Persona Examples

**Formal (0-99 interactions):**
```
Tuan, I have completed the analysis of the system logs. 
The error rate has decreased by 15% since the last update. 
✅ All systems are functioning within normal parameters.
```

**Casual (100-499 interactions):**
```
Hey there! I've finished analyzing the logs. 
Good news - error rate is down 15% since the last update. 
👍 Everything's looking good!
```

**Friendly (500+ interactions):**
```
Hey! Just finished checking the logs - looks like things are improving! 
Error rate dropped 15% since the last update. 😄 
Pretty solid progress, right?
```

### Implementation

**Database Schema:**
```sql
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    interaction_count INTEGER DEFAULT 0,
    persona TEXT DEFAULT 'formal',
    first_interaction DATETIME,
    last_interaction DATETIME
);
```

**Usage:**
```javascript
// Get user's interaction count
const count = await userProfileManager.getInteractionCount(userId);

// Determine persona
const persona = getPersonaFromCount(count);

// Generate response with persona
const result = await geminiService.generateResponse(userId, message, {
  persona: persona,
});
```

### System Prompt Injection

JARVIS's system instructions are dynamically updated based on persona:

```javascript
_getConversationalSystemPrompt(persona = 'formal') {
  const personaStyles = {
    formal: {
      greeting: 'Tuan/Sir',
      tone: 'professional and formal',
      language: 'precise and professional',
      emojis: 'minimal (🤖, ✅, ❌, ⚠️, 🚨)',
      relationship: 'professional assistant',
    },
    casual: {
      greeting: 'Hey there',
      tone: 'professional but approachable',
      language: 'clear and direct',
      emojis: 'occasional (👍, 🤔, 😊, 🎉)',
      relationship: 'trusted colleague',
    },
    friendly: {
      greeting: 'Hey!',
      tone: 'friendly and casual',
      language: 'conversational with occasional humor',
      emojis: 'frequent (😄, 🤗, ✨, 🌟)',
      relationship: 'close friend',
    },
  };
  
  // Build dynamic system prompt with persona
  return `You are JARVIS... Your relationship with the user is: ${style.relationship}...`;
}
```

## Spontaneity Module

### How It Works

JARVIS autonomously initiates conversations when user is inactive:

**Trigger Conditions:**
- User hasn't interacted for 12+ hours
- Relevant tech news found
- GitHub trending repositories match stack

**Content Sources:**
- RSS feeds (TechCrunch, The Verge, O'Reilly Radar)
- GitHub trending (JavaScript, Python, TypeScript)
- Relevance filtering for Lumina Overmind stack

### Example Spontaneous Messages

**Tech News:**
```
Hey! Saw this and thought of you - TechCrunch just published an article about the latest React performance optimizations. Since we're using Next.js, this might be really useful for our dashboard! What do you think? 🤔
```

**GitHub Trending:**
```
Hey! Check out this trending Python repo on GitHub - it's a new AI framework that could be interesting for our JARVIS project. Might be worth exploring! 🚀
```

### Configuration

```python
config = {
    'inactivity_threshold': 12,  # hours
    'rss_feeds': [
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://feeds.feedburner.com/oreilly/radar',
    ],
    'github_trending_enabled': True,
    'github_languages': ['javascript', 'python', 'typescript'],
    'relevance_keywords': [
        'react', 'nextjs', 'python', 'fastapi', 'ai',
        'docker', 'kubernetes', 'websocket', 'telegram',
        'whatsapp', 'gemini', 'openai', 'llm',
    ],
}
```

### Scheduler Integration

```python
# In scheduler.py
'spontaneity': {
    'enabled': True,
    'interval': 4,  # Every 4 hours
    'description': 'Spontaneous conversation initiation based on inactivity',
}
```

### Relevance Scoring

```python
def _calculate_relevance_score(self, item):
    score = 0.0
    text = f"{item['title']} {item['description']}".lower()
    
    for keyword in self.relevance_keywords:
        if keyword.lower() in text:
            score += 0.2
    
    return min(score, 1.0)  # Cap at 1.0
```

## Complete Example

### User Journey

**First Interaction (Formal):**
```
User: What's the system status?
JARVIS: Tuan, I have checked the system status. All services are operational. 
✅ CPU usage: 45%
✅ Memory: 62%
✅ Disk: 34%
All systems functioning within normal parameters.
```

**After 150 Interactions (Casual):**
```
User: What's the system status?
JARVIS: Hey there! Just checked - everything's looking good. 
👍 CPU at 45%, memory at 62%, disk at 34%. 
All systems running smoothly!
```

**After 600 Interactions (Friendly):**
```
User: What's the system status?
JARVIS: Hey! System's looking great today! 😄 
CPU's at 45%, memory at 62%, disk at 34%. 
Pretty solid performance across the board. Anything specific you want me to check?
```

**Spontaneous Message (After 12h inactivity):**
```
JARVIS: Hey! Saw this and thought of you - TechCrunch just published an article about the latest React performance optimizations. Since we're using Next.js, this might be really useful for our dashboard! What do you think? 🤔
```

## Message Flow Example

### Long Response with Splitting

**Original AI Response (500 characters):**
```
I've analyzed the Docker configuration and identified several optimization opportunities. First, we should switch to multi-stage builds to reduce image size. Second, we can implement build caching to speed up deployment. Third, we should use .dockerignore to exclude unnecessary files. Fourth, we can optimize the base image selection. Finally, we should implement health checks for better monitoring.
```

**After Human-Like Processing:**

**Chunk 1 (after 2.5s typing):**
```
I've analyzed the Docker configuration and identified several optimization opportunities.
```

**Chunk 2 (after 1.2s typing):**
```
First, we should switch to multi-stage builds to reduce image size.
```

**Chunk 3 (after 1.8s typing):**
```
Second, we can implement build caching to speed up deployment.
```

**Chunk 4 (after 1.5s typing):**
```
Third, we should use .dockerignore to exclude unnecessary files.
```

**Chunk 5 (after 1.3s typing):**
```
Fourth, we can optimize the base image selection.
```

**Chunk 6 (after 1.1s typing):**
```
Finally, we should implement health checks for better monitoring. ✅
```

## Configuration

### Environment Variables

```bash
# Human-like communication
JARVIS_MESSAGE_SPLITTING_ENABLED=true
JARVIS_TYPING_DELAY_ENABLED=true
JARVIS_TYPING_SPEED=20
JARVIS_TYPING_VARIANCE=0.3

# Dynamic persona
JARVIS_PERSONA_EVOLUTION_ENABLED=true
JARVIS_FORMAL_THRESHOLD=100
JARVIS_CASUAL_THRESHOLD=500

# Spontaneity
JARVIS_SPONTANEITY_ENABLED=true
JARVIS_INACTIVITY_THRESHOLD=12
JARVIS_SPONTANEITY_INTERVAL=4
```

### Handler Configuration

**WhatsApp:**
```javascript
const config = {
  humanCommunication: {
    enabled: true,
    messageSplitting: true,
    typingDelay: true,
    maxChunkLength: 300,
    chunkDelay: 1000,
  },
};
```

**Telegram:**
```javascript
const config = {
  humanCommunication: {
    enabled: true,
    messageSplitting: true,
    typingDelay: true,
    maxChunkLength: 300,
    chunkDelay: 1000,
  },
};
```

## Best Practices

### For Message Splitting

1. **Keep chunks meaningful**: Split at natural sentence boundaries
2. **Maintain context**: Each chunk should be understandable
3. **Avoid orphaned words**: Don't split mid-word
4. **Respect code blocks**: Keep code blocks intact
5. **Consider platform limits**: WhatsApp has character limits

### For Typing Delays

1. **Be realistic**: Don't make delays too long or too short
2. **Add variance**: Human typing isn't perfectly consistent
3. **Consider message length**: Longer messages need more time
4. **Platform-specific**: Adjust for different platforms
5. **User preference**: Allow users to disable if desired

### For Dynamic Persona

1. **Gradual evolution**: Don't jump between personas abruptly
2. **Context-aware**: Maintain persona consistency within conversation
3. **Respect boundaries**: Never become too casual in professional contexts
4. **User feedback**: Allow users to adjust persona preference
5. **Fallback safe**: Default to formal if unsure

### For Spontaneity

1. **Relevance first**: Only share truly relevant content
2. **Don't spam**: Limit spontaneous messages frequency
3. **Respect time**: Don't send during sleeping hours
4. **Value-add**: Always provide value, not just noise
5. **Opt-out option**: Allow users to disable spontaneity

## Troubleshooting

### Message Splitting Issues

**Chunks too small:**
```javascript
// Increase maxChunkLength
const chunks = splitMessage(message, {
  maxChunkLength: 500,  // Increased from 300
});
```

**Chunks too large:**
```javascript
// Decrease maxChunkLength
const chunks = splitMessage(message, {
  maxChunkLength: 200,  // Decreased from 300
});
```

**Unnatural splits:**
```javascript
// Change split strategy
const chunks = splitMessage(message, {
  splitBy: 'paragraph',  // Instead of 'sentence'
});
```

### Typing Delay Issues

**Delays too long:**
```javascript
const delay = calculateTypingDelay(message, {
  charsPerSecond: 30,  // Faster typing
  baseDelay: 300,      // Lower base delay
});
```

**Delays too short:**
```javascript
const delay = calculateTypingDelay(message, {
  charsPerSecond: 15,  // Slower typing
  baseDelay: 700,      // Higher base delay
});
```

**No variance:**
```javascript
const delay = calculateTypingDelay(message, {
  variance: 0.5,  // Increase variance to 50%
});
```

### Persona Issues

**Persona not changing:**
```python
# Check interaction count
count = user_profile_manager.get_interaction_count(user_id)
print(f"Current count: {count}")

# Manually update for testing
user_profile_manager.increment_interaction_count(user_id)
```

**Persona stuck on formal:**
```javascript
// Check persona threshold
const persona = getPersonaFromCount(count);
console.log(`Count: ${count}, Persona: ${persona}`);
```

### Spontaneity Issues

**No spontaneous messages:**
```python
# Check inactivity threshold
config['inactivity_threshold'] = 6  # Reduce to 6 hours

# Check last interaction
last_interaction = spontaneity_module.last_interaction_time[user_id]
print(f"Last interaction: {last_interaction}")
```

**Irrelevant content:**
```python
# Adjust relevance keywords
config['relevance_keywords'] = [
    'react', 'nextjs', 'python', 'fastapi',
    # Add more specific keywords
]
```

## Monitoring

### Track Persona Evolution

```python
# Get user stats
stats = user_profile_manager.get_user_stats(user_id)
print(f"Interaction count: {stats['interaction_count']}")
print(f"Current persona: {stats['persona']}")
```

### Track Spontaneity

```python
# Get spontaneity stats
stats = spontaneity_module.get_stats()
print(f"Spontaneous messages sent: {stats['spontaneous_messages_sent']}")
print(f"Relevance rate: {stats['relevance_rate']}")
```

### Track Message Splitting

```javascript
// Log chunk counts
const chunks = splitMessage(message);
console.log(`Message split into ${chunks.length} chunks`);
```

## Performance Considerations

### Message Splitting

- **Complexity**: O(n) where n is message length
- **Memory**: Minimal, processes chunks sequentially
- **Latency**: Adds ~100-500ms processing time

### Typing Delays

- **Latency**: Adds 300-3000ms per message
- **User Experience**: Feels more natural
- **Trade-off**: Slower response time vs. human-like feel

### Dynamic Persona

- **Complexity**: O(1) persona lookup
- **Memory**: Minimal, stores current persona
- **Latency**: Adds ~50ms for model reinitialization

### Spontaneity

- **Complexity**: O(n) where n is number of feeds
- **Memory**: Stores user interaction times
- **Latency**: Runs in background, no user-facing impact

## Security Considerations

### Message Splitting

- **No data leakage**: Chunks are processed in memory
- **No persistence**: Chunks not stored
- **Safe for sensitive data**: No external processing

### Dynamic Persona

- **User privacy**: Interaction count stored locally
- **No external tracking**: No third-party analytics
- **User control**: Can reset interaction count

### Spontaneity

- **Content filtering**: Only relevant content shared
- **User consent**: Can be disabled per user
- **Time restrictions**: Respects quiet hours

## Future Enhancements

### Planned Features

- **Adaptive typing speed**: Learn user's preferred pace
- **Emotion detection**: Adjust tone based on user's mood
- **Context-aware spontaneity**: More intelligent content selection
- **Multi-language support**: Human-like communication in different languages
- **Voice message splitting**: Split audio transcripts naturally
- **Conversation threading**: Group related messages

### Community Contributions

Contributions welcome for:
- Additional persona styles
- Better splitting algorithms
- Enhanced spontaneity sources
- Performance optimizations
- Cross-platform adaptations

## Support

For issues or questions:
- Check interaction count in database
- Verify persona threshold settings
- Test message splitting with sample text
- Monitor spontaneity logs
- Review configuration settings
- Check platform-specific limits

## License

This feature is part of JARVIS AI System.
See main project license for details.
