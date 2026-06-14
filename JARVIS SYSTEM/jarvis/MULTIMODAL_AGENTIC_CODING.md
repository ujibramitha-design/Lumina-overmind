# JARVIS Multimodal & Agentic Coding Guide

Complete guide for JARVIS's ultimate form with multimodal capabilities and agentic coding powers.

## Overview

JARVIS now has native multimodal capabilities using Gemini 1.5 Pro:
- **Vision**: Analyze screenshots, diagrams, UI elements, and bug reports
- **Audio**: Process voice notes, transcribe audio, and analyze system sounds
- **Agentic Coding**: Auto-fix bugs with user approval flow

## Multimodal Capabilities

### Image Analysis

JARVIS can analyze images sent via WhatsApp or Telegram:
- Screenshot analysis and bug identification
- UI/UX evaluation
- Diagram and flowchart interpretation
- Error message analysis from screenshots
- Code comparison from visual inputs

### Audio Processing

JARVIS can process audio files:
- Voice note transcription
- System sound analysis
- Audio command processing
- Meeting transcription and summarization

## Agentic Coding Flow

### Approval Flow

When JARVIS identifies a bug from an image or code analysis:

1. **Analysis**: JARVIS analyzes the issue
2. **Patch Generation**: Creates fixed code snippet
3. **Approval Request**: Asks user to confirm with "Reply YES to apply this fix"
4. **User Approval**: User replies "YES" to approve
5. **Safe Application**: JARVIS applies patch with backup
6. **Server Restart**: Triggers PM2 restart if needed

### Safety Features

- **Automatic Backup**: Creates timestamped backup before any changes
- **File Validation**: Checks if file exists before modification
- **Approval Required**: No changes without explicit user confirmation
- **Path Resolution**: Uses absolute paths to prevent errors
- **Error Handling**: Graceful fallback on failures

## Usage Examples

### Send Screenshot for Bug Analysis

**WhatsApp:**
```
1. Take screenshot of bug
2. Send to JARVIS WhatsApp
3. JARVIS analyzes and provides:
   - Bug description
   - Root cause analysis
   - Fixed code snippet
   - File path to modify
   - Approval request
```

**Telegram:**
```
1. Take screenshot of bug
2. Send to JARVIS Telegram bot
3. JARVIS analyzes and provides:
   - Bug description
   - Root cause analysis
   - Fixed code snippet
   - File path to modify
   - Approval request
```

### Send Voice Note

**WhatsApp:**
```
1. Record voice note
2. Send to JARVIS WhatsApp
3. JARVIS transcribes and responds
```

**Telegram:**
```
1. Record voice note
2. Send to JARVIS Telegram bot
3. JARVIS transcribes and responds
```

### Approve Code Fix

After JARVIS provides a fix:

```
User: YES
JARVIS: ✅ Patch applied successfully. Backup saved to: /path/to/file.backup_1234567890
```

## API Reference

### generateMultimodalResponse

Generate response with image or audio input.

```javascript
const { getGeminiService } = require('./services/geminiService');

const geminiService = getGeminiService();

// Image analysis
const result = await geminiService.generateMultimodalResponse(
  'user_123',
  'Analyze this screenshot',
  {
    type: 'image',
    buffer: imageBuffer,
    mimeType: 'image/jpeg',
  },
  {
    platform: 'telegram',
    username: 'john_doe',
  }
);

// Audio transcription
const result = await geminiService.generateMultimodalResponse(
  'user_123',
  'Transcribe this voice note',
  {
    type: 'audio',
    buffer: audioBuffer,
    mimeType: 'audio/ogg',
  },
  {
    platform: 'whatsapp',
    phoneNumber: '+1234567890',
  }
);
```

### requestPatchApproval

Request approval for code patch.

```javascript
const patchData = {
  filePath: './src/components/Button.tsx',
  newCode: `// Fixed code here`,
  description: 'Fix button click handler',
  restartServer: true,
};

const result = await geminiService.requestPatchApproval('user_123', patchData);
```

### applyPatch

Apply approved patch.

```javascript
const result = await geminiService.applyPatch('user_123', 'YES');

if (result.success) {
  console.log(result.message);
  console.log('Backup:', result.backupPath);
}
```

### getPendingApproval

Get pending approval for a user.

```javascript
const approval = geminiService.getPendingApproval('user_123');
console.log(approval);
```

### clearPendingApproval

Clear pending approval for a user.

```javascript
geminiService.clearPendingApproval('user_123');
```

## Configuration

### Environment Variables

```bash
# Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here

# PM2 process name for restart
JARVIS_PM2_PROCESS=jarvis-hub
```

### Model Configuration

```javascript
// In geminiService.js
this.models = {
  conversational: 'gemini-1.5-flash',
  codebase: 'gemini-1.5-pro',
  analysis: 'gemini-1.5-pro',
  multimodal: 'gemini-1.5-pro',  // Multimodal model
};
```

## Security Considerations

### File Path Validation

- Only allows modification of files within project directory
- Resolves absolute paths to prevent directory traversal
- Validates file existence before modification

### Approval Flow

- No automatic code changes without approval
- User must explicitly confirm with "YES"
- Pending approvals cleared on denial
- Timestamp tracking for audit trail

### Backup System

- Automatic timestamped backups
- Original file preserved
- Easy rollback if needed
- Backup path returned for reference

### PM2 Restart

- Configurable process name
- Only restarts if explicitly requested
- Graceful shutdown handling
- Error logging

## Troubleshooting

### Image Analysis Fails

**Error:** Failed to process image

**Solutions:**
- Check image format (JPEG, PNG supported)
- Verify image size (< 10MB recommended)
- Ensure Gemini API has multimodal capabilities
- Check network connectivity

### Audio Transcription Fails

**Error:** Failed to process audio

**Solutions:**
- Check audio format (OGG, MP3 supported)
- Verify audio duration (< 5 minutes recommended)
- Ensure Gemini API has audio capabilities
- Check audio quality

### Patch Application Fails

**Error:** Failed to apply patch

**Solutions:**
- Verify file path is correct
- Check file permissions
- Ensure file exists
- Validate patch data format
- Check backup directory permissions

### PM2 Restart Fails

**Error:** Failed to restart server

**Solutions:**
- Verify PM2 is installed
- Check process name is correct
- Ensure PM2 has permissions
- Check PM2 logs for errors

## Best Practices

### For Users

1. **Clear Screenshots**: Ensure screenshots are clear and show relevant code
2. **Voice Notes**: Speak clearly and concisely
3. **Approval**: Only approve patches after reviewing the code
4. **Backups**: Keep manual backups of critical files
5. **Testing**: Test changes after patch application

### For Developers

1. **Validation**: Always validate file paths
2. **Backups**: Never skip backup creation
3. **Error Handling**: Handle all error cases gracefully
4. **Logging**: Log all patch operations
5. **Testing**: Test multimodal features thoroughly

### For Security

1. **Approval**: Never bypass approval flow
2. **Permissions**: Limit file write permissions
3. **Audit**: Keep audit trail of all changes
4. **Validation**: Validate all user inputs
5. **Isolation**: Run JARVIS in isolated environment

## Integration Examples

### Custom Media Handler

```javascript
async handleCustomMedia(userId, mediaUrl, mediaType) {
  const geminiService = getGeminiService();
  
  // Download media
  const response = await fetch(mediaUrl);
  const buffer = await response.buffer();
  
  // Process with Gemini
  const result = await geminiService.generateMultimodalResponse(
    userId,
    'Analyze this media',
    {
      type: mediaType,
      buffer: buffer,
      mimeType: mediaType === 'image' ? 'image/jpeg' : 'audio/mp3',
    }
  );
  
  return result;
}
```

### Custom Patch Flow

```javascript
async customPatchFlow(userId, patchData) {
  const geminiService = getGeminiService();
  
  // Request approval
  const approval = await geminiService.requestPatchApproval(userId, patchData);
  
  // Send approval request to user
  await sendToUser(userId, approval.message);
  
  // Wait for user response (implement your own logic)
  const userResponse = await waitForUserResponse(userId);
  
  // Apply patch if approved
  if (userResponse === 'YES') {
    const result = await geminiService.applyPatch(userId, userResponse);
    return result;
  }
  
  return { success: false, error: 'Approval denied' };
}
```

## Monitoring

### Track Patch Operations

```javascript
const geminiService = getGeminiService();

// Get pending approvals
const approvals = geminiService.pendingApprovals;
console.log('Pending approvals:', approvals.size);

// Get conversation stats
const stats = geminiService.getConversationStats();
console.log('Total users:', stats.totalUsers);
console.log('Total messages:', stats.totalMessages);
```

### Log Patch History

```javascript
// In your application
async function logPatchOperation(userId, patchData, result) {
  const logEntry = {
    userId,
    filePath: patchData.filePath,
    timestamp: new Date().toISOString(),
    success: result.success,
    backupPath: result.backupPath,
  };
  
  // Save to database or file
  await saveToLog(logEntry);
}
```

## Performance Tips

### Image Optimization

- Compress images before sending
- Use appropriate image formats
- Limit image size to < 10MB
- Crop to relevant areas only

### Audio Optimization

- Keep voice notes short (< 2 minutes)
- Use clear audio quality
- Remove background noise
- Use appropriate compression

### Patch Optimization

- Batch multiple small changes
- Use incremental patches
- Test patches in staging first
- Schedule restarts during low traffic

## Advanced Features

### Multi-File Patches

```javascript
async applyMultiFilePatch(userId, patches) {
  const geminiService = getGeminiService();
  const results = [];
  
  for (const patch of patches) {
    const approval = await geminiService.requestPatchApproval(userId, patch);
    const result = await geminiService.applyPatch(userId, 'YES');
    results.push(result);
  }
  
  return results;
}
```

### Rollback Capability

```javascript
async rollbackPatch(backupPath) {
  const fs = require('fs');
  const path = require('path');
  
  // Extract original path from backup
  const originalPath = backupPath.replace(/\.backup_\d+$/, '');
  
  // Restore from backup
  fs.copyFileSync(backupPath, originalPath);
  
  // Restart server
  await geminiService._triggerServerRestart();
  
  return { success: true, message: 'Rollback complete' };
}
```

## Limitations

### Gemini API Limits

- Rate limits apply
- File size limits (images: 10MB, audio: 5MB)
- Context window limits
- Concurrent request limits

### Platform Limitations

- WhatsApp: Limited media formats
- Telegram: File size restrictions
- Network: Latency affects performance
- Storage: Backup files consume space

## Future Enhancements

### Planned Features

- Video analysis support
- Multi-language audio transcription
- Automated testing after patches
- Git integration for version control
- Rollback UI in mobile app
- Patch preview before approval

### Community Contributions

Contributions welcome for:
- Additional media format support
- Enhanced security features
- Better error handling
- Performance optimizations
- Documentation improvements

## Support

For issues or questions:
- Check Gemini API documentation
- Review patch logs
- Verify file permissions
- Test with simple examples first
- Monitor PM2 logs for errors
- Check backup directory

## License

This feature is part of JARVIS AI System.
See main project license for details.
