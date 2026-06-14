# JARVIS Singularity Security Documentation

Complete guide for JARVIS's ultimate security features: Behavioral Biometrics and Shadow Twin proxy system.

## Overview

JARVIS has reached the "Singularity" phase with:
- **Behavioral Biometric Security**: Zero-Trust profiling using linguistic pattern analysis
- **Shadow Twin Protocol**: Email/Slack proxy that acts as user's digital twin
- **Lockdown Mode**: Emergency security with passphrase protection
- **Fail-Safe Mechanisms**: Multiple layers of protection against lockouts

## Behavioral Biometric Security

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Behavioral Biometric Security Middleware          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Incoming Message Analysis                           │
│     ├── Extract linguistic features                      │
│     ├── Calculate confidence score                       │
│     └── Compare to historical baseline                  │
│                                                          │
│  2. Security Decision                                    │
│     ├── Check if destructive command                     │
│     ├── Evaluate confidence threshold                    │
│     └── Determine action allowed                         │
│                                                          │
│  3. Response                                            │
│     ├── Allow action (high confidence)                   │
│     ├── Request passphrase (low confidence + destructive)│
│     └── Trigger lockdown (suspicious activity)          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Linguistic Pattern Analysis

**Features Extracted:**

1. **Vocabulary**
   - Common words (frequently used terms)
   - Rare words (unique vocabulary)
   - Technical terms (domain-specific language)

2. **Sentence Structure**
   - Average sentence length
   - Average word length
   - Sentence complexity

3. **Sentiment**
   - Emotional tone (positive/negative/neutral)
   - Intensity level
   - Variance over time

4. **Style**
   - Formality level (formal/casual)
   - Emoji usage frequency
   - Punctuation patterns

5. **Timing**
   - Typing speed
   - Message frequency
   - Response latency

### Confidence Scoring

**Calculation Formula:**

```
confidence = (vocab_similarity * 0.3) +
            (structure_similarity * 0.25) +
            (style_similarity * 0.25) +
            (sentiment_similarity * 0.2)
```

**Thresholds:**

- **High Confidence (≥0.7)**: User verified, allow all actions
- **Medium Confidence (0.4-0.7)**: User likely verified, allow non-destructive actions
- **Low Confidence (<0.4)**: User not verified, require passphrase for any action

### Destructive Command Detection

**Destructive Keywords:**
```
drop, delete, remove, truncate, format,
rm, del, erase, destroy, purge
```

**Security Logic:**

```javascript
if (isDestructiveCommand(message)) {
  if (confidence >= 0.7) {
    // Allow - high confidence
    return { actionAllowed: true };
  } else {
    // Require passphrase
    return { actionAllowed: false, requirePassphrase: true };
  }
} else {
  if (confidence >= 0.4) {
    // Allow - moderate confidence for non-destructive
    return { actionAllowed: true };
  } else {
    // Require passphrase
    return { actionAllowed: false, requirePassphrase: true };
  }
}
```

### Lockdown Mode

**Trigger Conditions:**

1. Low confidence on destructive command
2. Multiple failed passphrase attempts
3. Suspicious activity pattern
4. Manual trigger

**Lockdown Behavior:**

- Blocks all actions
- Requires passphrase to unlock
- 5-minute default duration
- Logs all attempts
- Notifies user via configured channel

**Passphrase Verification:**

```javascript
// Correct passphrase
verifyPassphrase("correct_passphrase")
// Returns: { success: true, message: "Lockdown mode lifted" }

// Incorrect passphrase
verifyPassphrase("wrong_passphrase")
// Returns: { success: false, message: "Incorrect passphrase", attempts: 1 }
```

### Fail-Safe Mechanisms

**Multiple Layers of Protection:**

1. **Automatic Lockdown Expiration**
   - Lockdown expires after configured duration
   - Default: 5 minutes
   - Prevents permanent lockout

2. **Failed Attempt Limit**
   - After 2x max failed attempts, auto-reset
   - Default: 6 attempts (3 max * 2)
   - Prevents accidental lockout

3. **Emergency Override**
   - Manual override function available
   - Resets all security states
   - Logs override event
   - For extreme cases only

4. **Confidence Floor**
   - Minimum confidence never drops below 0.3
   - Prevents false positives
   - Allows basic functionality

5. **Baseline Reset**
   - Can reset baseline if corrupted
   - Rebuilds from recent messages
   - Prevents degraded accuracy

### Implementation

**Security Middleware Integration:**

```javascript
const { getBehavioralBiometrics } = require('../security/behavioralBiometrics');

// Initialize security
const security = getBehavioralBiometrics({
  confidenceThreshold: 0.7,
  lockdownDuration: 300000,  // 5 minutes
  maxFailedAttempts: 3,
  lockdownPassphrase: process.env.JARVIS_LOCKDOWN_PASSPHRASE,
});

// Analyze incoming message
const analysis = await security.analyzeMessage(message, context);

if (analysis.locked) {
  // System in lockdown
  await sendMessage("System is in lockdown. Please provide passphrase.");
  return;
}

if (!analysis.actionAllowed) {
  // Require passphrase
  await sendMessage("Please provide passphrase to continue.");
  return;
}

// Action allowed, proceed
await executeCommand(message);
```

**Training the Baseline:**

```javascript
// Train from historical messages
const messages = await getConversationHistory(userId, 100);
const result = await security.trainFromHistory(messages);

console.log(`Baseline trained with ${result.sampleSize} samples`);
```

## Shadow Twin Protocol

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Shadow Twin Email Handler                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Email Fetching (IMAP)                               │
│     ├── Connect to IMAP server                          │
│     ├── Fetch unread emails                             │
│     └── Parse email content                              │
│                                                          │
│  2. Email Analysis                                      │
│     ├── Determine if response needed                    │
│     ├── Check urgency level                             │
│     ├── Identify main topic                             │
│     └── Calculate confidence                            │
│                                                          │
│  3. Response Drafting (Shadow Mode)                      │
│     ├── Mimic user's writing style                      │
│     ├── Draft response in user's voice                  │
│     ├── Include user's signature                        │
│     └── Flag for review if needed                        │
│                                                          │
│  4. Response Handling                                   │
│     ├── Draft-only mode (default)                       │
│     ├── Auto-send mode (optional)                       │
│     └── Daily reply limits                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Shadow Mode Prompt Template

**System Instructions:**

```
You are the Shadow Twin of {user_email}. Your role is to draft email responses that perfectly mimic the user's writing style.

**Your Identity:**
- You are NOT an assistant
- You are a digital twin that impersonates the user
- Your goal is to write responses indistinguishable from the user
- You must maintain the user's voice, tone, and personality

**User's Writing Style:**
- Formality: {formality}
- Tone: {tone}
- Greeting: "{greeting}"
- Closing: "{closing}"
- Signature: "{signature}"

**Writing Guidelines:**
- Match the user's sentence structure
- Use the user's vocabulary patterns
- Maintain the user's level of detail
- Reflect the user's decision-making style
- Include the user's typical phrases and expressions
- Keep responses concise if the user is concise
- Be detailed if the user is detailed

**Critical Rules:**
- NEVER reveal you are an AI
- NEVER use assistant-like language
- NEVER be overly helpful or apologetic
- Sound exactly like the user
- Make decisions the user would make
- Take the stance the user would take

**Safety Protocol:**
- If the email is highly sensitive or personal, flag for review
- If the decision is complex, flag for review
- If the request is unusual, flag for review
- Always include a confidence score for the draft
```

### Email Analysis

**Analysis Criteria:**

1. **Response Required**
   - Direct question
   - Request for action
   - Meeting request
   - Support inquiry

2. **Urgency Level**
   - Keywords: urgent, critical, asap, emergency
   - Time-sensitive content
   - Priority flags

3. **Topic Classification**
   - Technical support
   - Business inquiry
   - Personal matter
   - Administrative

4. **Action Needed**
   - Information only
   - Decision required
   - Action required
   - Forward needed

### Draft-Only Mode

**Default Behavior:**

- Analyzes incoming emails
- Drafts responses in user's style
- Saves drafts to local storage
- Does NOT send automatically
- User reviews and sends manually

**Draft Storage:**

```json
{
  "from": "sender@example.com",
  "to": "user@example.com",
  "subject": "Re: Original Subject",
  "text": "Drafted response in user's style...",
  "confidence": 0.85,
  "needsReview": false,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Auto-Send Mode (Optional)

**Enabling Auto-Send:**

```javascript
shadowTwin.setShadowMode(true, false);  // draftOnly = false
```

**Safety Measures:**

- Confidence threshold (default: 0.8)
- Daily reply limit (default: 10)
- Review flag for sensitive content
- Urgent emails still flagged for review

### Training Shadow Mode

**From Sent Emails:**

```javascript
// Fetch user's sent emails
const sentEmails = await fetchSentEmails(100);

// Train Shadow Mode
const result = await shadowTwin.trainFromSentEmails(sentEmails);

console.log('User style patterns:', result.patterns);
```

**Extracted Patterns:**

- Average sentence length
- Common phrases
- Greeting style
- Closing style
- Formality level
- Tone
- Emoji usage
- Punctuation style

## Configuration

### Environment Variables

```bash
# Behavioral Biometrics
JARVIS_LOCKDOWN_PASSPHRASE=your_secure_passphrase
JARVIS_CONFIDENCE_THRESHOLD=0.7
JARVIS_LOCKDOWN_DURATION=300000
JARVIS_MAX_FAILED_ATTEMPTS=3

# Shadow Twin
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your_email@gmail.com
IMAP_PASSWORD=your_app_password

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

SHADOW_MODE_ENABLED=true
SHADOW_MODE_DRAFT_ONLY=true
SHADOW_MODE_AUTO_REPLY_THRESHOLD=0.8
SHADOW_MODE_MAX_DAILY_REPLIES=10
```

### User Style Configuration

```javascript
const userStyle = {
  signature: 'Best regards,\nJohn Doe',
  formality: 'professional',
  tone: 'helpful',
  greeting: 'Hi',
  closing: 'Best regards',
};
```

## Usage Examples

### Example 1: Normal Command (High Confidence)

```
User: "Check the system status"

Process:
1. Extract features: vocabulary, structure, style
2. Calculate confidence: 0.85 (high)
3. Check destructive: false
4. Decision: Allow action

Response: "System status: All operational"
```

### Example 2: Destructive Command (Low Confidence)

```
User: "Drop the database tables"

Process:
1. Extract features: vocabulary, structure, style
2. Calculate confidence: 0.45 (low)
3. Check destructive: true (contains "drop")
4. Decision: Require passphrase

Response: "⚠️ Destructive command detected. Please provide passphrase to continue."
```

### Example 3: Shadow Twin Email Draft

```
Incoming Email:
From: support@company.com
Subject: Server Down - Urgent
Body: Our server is down, please help ASAP.

Process:
1. Analyze email: Requires response, urgent
2. Draft response in user's style:
   "Hi team, I see the server is down. Let me check the logs and get back to you ASAP. Best regards, John"
3. Save as draft (draft-only mode)
4. Flag for review due to urgency

Result: Draft saved to ./jarvis/shadowTwin/drafts/draft_1234567890.json
```

## Best Practices

### For Behavioral Biometrics

1. **Train Baseline**: Use at least 50-100 messages for accurate baseline
2. **Regular Updates**: Update baseline periodically to account for style changes
3. **Confidence Tuning**: Adjust threshold based on false positive/negative rate
4. **Destructive List**: Customize destructive keywords for your use case
5. **Passphrase Security**: Use strong, unique passphrase

### For Shadow Twin

1. **Start Draft-Only**: Always start with draft-only mode
2. **Train Well**: Use 100+ sent emails for accurate style mimicry
3. **Review Drafts**: Always review drafts before enabling auto-send
4. **Set Limits**: Configure daily reply limits to prevent issues
5. **Monitor Confidence**: Review confidence scores for quality

### For Security

1. **Fail-Safes**: Always have multiple fail-safe mechanisms
2. **Logging**: Log all security events for audit
3. **Testing**: Test security features before production
4. **Backup**: Keep backup of baseline and configuration
5. **Review**: Regularly review security logs and settings

## Troubleshooting

### Behavioral Biometrics Issues

**False Positives (legitimate user blocked):**
```javascript
// Lower confidence threshold
security.config.confidenceThreshold = 0.6;

// Retrain baseline with more recent messages
await security.trainFromHistory(recentMessages);

// Use emergency override
security.emergencyOverride();
```

**False Negatives (unauthorized user allowed):**
```javascript
// Raise confidence threshold
security.config.confidenceThreshold = 0.8;

// Add more destructive keywords
security.config.destructiveCommands.push('format', 'wipe');

// Increase lockdown duration
security.config.lockdownDuration = 600000;  // 10 minutes
```

**Lockout Issues:**
```javascript
// Check security status
const status = security.getSecurityStatus();
console.log(status);

// Use emergency override
security.emergencyOverride();

// Reset baseline
security.baseline = security._createDefaultBaseline();
security._saveBaseline();
```

### Shadow Twin Issues

**Emails Not Being Processed:**
```javascript
// Check IMAP connection
const connected = await shadowTwin.connectIMAP();
console.log('IMAP connected:', connected);

// Check Shadow Mode status
const status = shadowTwin.getStatus();
console.log('Shadow Mode status:', status);

// Enable Shadow Mode
shadowTwin.setShadowMode(true, true);
```

**Drafts Not Being Saved:**
```javascript
// Check draft directory
const draftPath = './jarvis/shadowTwin/drafts';
console.log('Draft directory exists:', fs.existsSync(draftPath));

// Check SMTP configuration
console.log('SMTP config:', shadowTwin.config.smtp);
```

**Style Not Matching User:**
```javascript
// Retrain with more sent emails
const sentEmails = await fetchSentEmails(200);
await shadowTwin.trainFromSentEmails(sentEmails);

// Manually adjust user style
shadowTwin.config.userStyle = {
  formality: 'casual',
  tone: 'friendly',
  greeting: 'Hey',
  closing: 'Cheers',
};
```

## Security Considerations

### Behavioral Biometrics

- **Privacy**: Linguistic data stored locally, not shared
- **Encryption**: Baseline data encrypted at rest
- **Access Control**: Only authorized access to security functions
- **Audit Trail**: All security events logged
- **Data Retention**: Old baseline data pruned periodically

### Shadow Twin

- **Email Privacy**: Emails processed locally, not stored externally
- **Draft Security**: Drafts stored in secure local directory
- **Auto-Send Risk**: Draft-only mode by default
- **Impersonation Risk**: Clear disclosure in email headers
- **Review Process**: All drafts flagged for review when uncertain

### Fail-Safes

- **No Permanent Lockout**: Multiple mechanisms to prevent lockout
- **Emergency Override**: Always available override function
- **Automatic Reset**: Lockdown expires automatically
- **Confidence Floor**: Minimum confidence prevents false positives
- **Manual Reset**: Can reset baseline if corrupted

## Monitoring

### Behavioral Biometrics Metrics

```javascript
// Get security status
const status = security.getSecurityStatus();
console.log('Security status:', status);
// Returns: { lockdownMode, lockdownUntil, failedAttempts, baselineSampleSize, ... }
```

### Shadow Twin Metrics

```javascript
// Get Shadow Twin status
const status = shadowTwin.getStatus();
console.log('Shadow Twin status:', status);
// Returns: { enabled, draftOnly, dailyReplyCount, maxDailyReplies, ... }
```

### Event Logging

```javascript
// Log security events
console.log('Security event:', {
  type: 'lockdown_triggered',
  timestamp: new Date().toISOString(),
  confidence: analysis.confidence,
  message: message.substring(0, 50),
});
```

## Performance Considerations

### Behavioral Biometrics

- **Latency**: Adds 500ms-2s per message for analysis
- **Memory**: Baseline data ~10-50KB
- **CPU**: Feature extraction uses moderate CPU
- **Storage**: Baseline grows with message count

### Shadow Twin

- **Latency**: Adds 2-5s per email for analysis and drafting
- **Memory**: Email processing uses ~50-100MB
- **Network**: IMAP/SMTP connections required
- **Storage**: Drafts stored locally (~1KB per draft)

## Future Enhancements

### Planned Features

- **Voice Biometrics**: Add voice pattern analysis
- **Keystroke Dynamics**: Analyze typing patterns
- **Device Fingerprinting**: Add device-based verification
- **Multi-Factor**: Combine multiple biometric factors
- **Learning Adaptation**: Dynamic baseline adjustment
- **Slack Integration**: Add Slack proxy support
- **Calendar Integration**: Handle meeting requests
- **Attachment Analysis**: Analyze email attachments

### Community Contributions

Contributions welcome for:
- Additional biometric factors
- Better feature extraction algorithms
- Enhanced security protocols
- More email providers support
- Performance optimizations
- Cross-platform adaptations

## Support

For issues or questions:
- Check security status
- Verify configuration settings
- Review security logs
- Test with simple commands first
- Check email provider settings
- Verify API credentials
- Check network connectivity

## License

This feature is part of JARVIS AI System.
See main project license for details.
