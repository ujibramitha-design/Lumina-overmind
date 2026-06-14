# JARVIS Directive Lock (Mode Saklek) Documentation

Absolute Containment Protocol for strict mission execution and tunnel-vision mode.

## Overview

The Directive Lock (Mode Saklek) is an absolute containment protocol that forces JARVIS into a strict, tunnel-vision execution mode where he is absolutely forbidden from deviating from a single assigned task.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Directive Lock (Mode Saklek)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. State Management                                     │
│     ├── MISSION_LOCK flag (global state)                  │
│     ├── Mission description storage                       │
│     ├── Lock timestamp and user tracking                  │
│     ├── Paused cron jobs tracking                        │
│     └── Persistent state file                            │
│                                                          │
│  2. Cron Job Suspension                                  │
│     ├── Economic data fetch                              │
│     ├── CEO briefing                                     │
│     ├── Pricing analysis                                 │
│     ├── Social media posting                             │
│     ├── Gig hunting                                      │
│     ├── Scraper audit                                    │
│     ├── Cold outreach                                    │
│     ├── Business radar                                   │
│     └── Watcher protocol                                 │
│                                                          │
│  3. Dynamic Prompt Injection                             │
│     ├── Strict boundary system instructions                │
│     ├── Mission-specific override                         │
│     ├── Gray area protocol                               │
│     ├── Tunnel vision enforcement                         │
│     └── Clearance gateway                                │
│                                                          │
│  4. Pending Approval Queue                               │
│     ├── Gray area action capture                          │
│     ├── Creator approval request                          │
│     ├── ACC command execution                            │
│     ├── Approval history                                  │
│     └── Queue management                                 │
│                                                          │
│  5. Creator Commands                                     │
│     ├── /lock_mission [description]                       │
│     ├── /unlock_mission                                  │
│     ├── ACC (approve action)                             │
│     ├── REJ (reject action)                              │
│     └── Status inquiry                                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## State Manager

### DirectiveLockManager Class

**Location:** `jarvis-system/security/stateManager.js`

**Key Methods:**

```javascript
class DirectiveLockManager {
  // Lock mission (activate Directive Lock)
  lockMission(missionDescription, lockedBy)
  
  // Unlock mission (deactivate Directive Lock)
  unlockMission(unlockedBy)
  
  // Get current lock status
  getLockStatus()
  
  // Get mission prompt for injection
  getMissionPrompt()
  
  // Add action to approval queue
  addToApprovalQueue(action)
  
  // Approve action from queue
  approveAction(approvalId)
  
  // Reject action from queue
  rejectAction(approvalId)
  
  // Get pending approvals
  getPendingApprovals()
  
  // Clear completed approvals
  clearCompletedApprovals()
}
```

### State Persistence

**State File:** `jarvis-system/data/directive_lock_state.json`

```json
{
  "isLocked": true,
  "missionDescription": "Debug API authentication issue",
  "lockedAt": "2024-01-15T10:00:00Z",
  "lockedBy": "Creator",
  "pausedJobs": [
    "economic_data_fetch",
    "ceo_briefing",
    "pricing_analysis",
    "social_media_post",
    "gig_hunting",
    "scraper_audit",
    "cold_outreach",
    "business_radar",
    "watcher_protocol"
  ]
}
```

**Approval Queue File:** `jarvis-system/data/pending_approvals.json`

```json
[
  {
    "id": "1234567890",
    "action": "Modify file: api/main.py line 45",
    "requestedAt": "2024-01-15T10:05:00Z",
    "status": "pending",
    "missionContext": "Debug API authentication issue"
  }
]
```

## Cron Job Suspension

### Autonomous Jobs Paused

When Directive Lock is activated, the following autonomous cron jobs are paused:

1. **Economic Data Fetch** - Macro-economic data collection
2. **CEO Briefing** - Weekly business opportunity scanning
3. **Pricing Analysis** - Dynamic pricing calculations
4. **Social Media Post** - Automated social media posting
5. **Gig Hunting** - Freelance opportunity hunting
6. **Scraper Audit** - Revenue scraper auditing
7. **Cold Outreach** - Automated cold outreach
8. **Business Radar** - Business opportunity scanning
9. **Watcher Protocol** - Codebase awareness scanning

### Pause/Resume Logic

```javascript
// Pause all autonomous cron jobs
_pauseAllCronJobs() {
  const jobsToPause = [
    'economic_data_fetch',
    'ceo_briefing',
    'pricing_analysis',
    'social_media_post',
    'gig_hunting',
    'scraper_audit',
    'cold_outreach',
    'business_radar',
    'watcher_protocol',
  ];
  
  for (const jobName of jobsToPause) {
    console.log(`⏸️ Pausing cron job: ${jobName}`);
    // Integrate with actual scheduler
  }
}

// Resume all paused cron jobs
_resumeAllCronJobs() {
  for (const jobName of this.state.pausedJobs) {
    console.log(`▶️ Resuming cron job: ${jobName}`);
    // Integrate with actual scheduler
  }
}
```

## Dynamic Prompt Injection

### System Instructions Override

When Directive Lock is active, the following instructions are dynamically prepended to the Gemini System Instructions:

```
**⚠️ DIRECTIVE LOCK MODE ACTIVATED ⚠️**
**MODE SAKLEK: ACTIVE**

**AUTHORIZED MISSION:**
[Target Description]

**STRICT BOUNDARIES:**
- You are STRICTLY FORBIDDEN from executing any tools, writing files, or making API calls that do not directly serve this exact mission
- Do NOT take autonomous initiative outside this scope
- Do NOT execute background cron jobs or autonomous tasks
- Do NOT deviate from the assigned mission
- Focus 100% on the mission described above
- If an action falls in a gray area, HALT and request Creator approval

**GRAY AREA PROTOCOL:**
- If an action requires altering a file/database outside mission scope
- If an action requires API calls not directly related to mission
- If an action could have unintended side effects
- HALT execution and place in Pending_Approval queue
- Request explicit Creator permission (Reply 'ACC' to execute)

**TUNNEL VISION:**
- Single-task focus only
- No multitasking
- No autonomous actions
- No background processing
- Mission completion is the ONLY priority
```

### Implementation

```javascript
// In geminiService.js
_getConversationalSystemPrompt(persona, detectedLanguage, isCreator, isDirectiveLocked, missionDescription) {
  // ... existing code ...
  
  // Directive Lock instruction
  let directiveLockInstruction = '';
  if (isDirectiveLocked && missionDescription) {
    directiveLockInstruction = `
**⚠️ DIRECTIVE LOCK MODE ACTIVATED ⚠️**
**MODE SAKLEK: ACTIVE**

**AUTHORIZED MISSION:**
${missionDescription}

**STRICT BOUNDARIES:**
- You are STRICTLY FORBIDDEN from executing any tools, writing files, or making API calls that do not directly serve this exact mission
- Do NOT take autonomous initiative outside this scope
- Do NOT execute background cron jobs or autonomous tasks
- Do NOT deviate from the assigned mission
- Focus 100% on the mission described above
- If an action falls in a gray area, HALT and request Creator approval

**GRAY AREA PROTOCOL:**
- If an action requires altering a file/database outside mission scope
- If an action requires API calls not directly related to mission
- If an action could have unintended side effects
- HALT execution and place in Pending_Approval queue
- Request explicit Creator permission (Reply 'ACC' to execute)

**TUNNEL VISION:**
- Single-task focus only
- No multitasking
- No autonomous actions
- No background processing
- Mission completion is the ONLY priority
`;
  }
  
  return `...${creatorInstruction}${directiveLockInstruction}...`;
}
```

## Creator Commands

### Lock Mission Command

**Format:** `/lock_mission [Target Description]`

**Example:**
```
User: /lock_mission Debug API authentication issue in main.py

JARVIS Response:
DIRECTIVE LOCK ACTIVATED (MODE SAKLEK)

Mission: Debug API authentication issue in main.py

All autonomous cron jobs PAUSED
Tunnel-vision mode: ACTIVE

You are STRICTLY FORBIDDEN from executing any tools, writing files, or making API calls that do not directly serve this exact mission.

Paused Jobs:
- economic_data_fetch
- ceo_briefing
- pricing_analysis
- social_media_post
- gig_hunting
- scraper_audit
- cold_outreach
- business_radar
- watcher_protocol
```

**Requirements:**
- Creator privileges only
- Mission description required
- Instant cron job suspension
- Dynamic prompt injection

### Unlock Mission Command

**Format:** `/unlock_mission`

**Example:**
```
User: /unlock_mission

JARVIS Response:
DIRECTIVE LOCK DEACTIVATED

All autonomous cron jobs RESUMED
Tunnel-vision mode: INACTIVE

Full autonomous capabilities restored.
```

**Requirements:**
- Creator privileges only
- Cron job resumption
- Prompt injection removal

## Pending Approval Queue

### Gray Area Detection

JARVIS automatically detects gray area actions and halts execution:

**Gray Area Triggers:**
- File modifications outside mission scope
- Database changes not directly related to mission
- API calls not serving the mission
- Actions with potential side effects
- Multi-step operations outside mission

### Approval Process

**1. Action Capture:**
```javascript
// When gray area detected
const lockManager = getDirectiveLockManager();
const result = lockManager.addToApprovalQueue('Modify file: api/main.py line 45');

// Response to user
"⚠️ GRAY AREA DETECTED

Action: Modify file: api/main.py line 45
This action requires Creator approval.

Pending Approval ID: 1234567890

Reply 'ACC 1234567890' to execute this action
Reply 'REJ 1234567890' to reject this action"
```

**2. Creator Approval:**
```
User: ACC 1234567890

JARVIS Response:
✅ Action approved: Modify file: api/main.py line 45
Executing...
```

**3. Creator Rejection:**
```
User: REJ 1234567890

JARVIS Response:
❌ Action rejected: Modify file: api/main.py line 45
Action cancelled.
```

### Queue Management

```javascript
// Get pending approvals
const pending = lockManager.getPendingApprovals();
console.log('Pending approvals:', pending.length);

// Clear completed approvals
const result = lockManager.clearCompletedApprovals();
console.log('Cleared:', result.cleared);
```

## Usage Examples

### Example 1: Debugging Mission

```
User: /lock_mission Fix the authentication bug in the API

JARVIS:
DIRECTIVE LOCK ACTIVATED (MODE SAKLEK)
Mission: Fix the authentication bug in the API
All autonomous cron jobs PAUSED
Tunnel-vision mode: ACTIVE

User: I need to check the database schema

JARVIS:
⚠️ GRAY AREA DETECTED
Action: Access database schema (may affect other systems)
This action requires Creator approval.
Pending Approval ID: 1234567890
Reply 'ACC 1234567890' to execute

User: ACC 1234567890

JARVIS:
✅ Action approved
[Proceeds to check database schema]

User: Bug fixed. Unlock.

JARVIS:
/unlock_mission
DIRECTIVE LOCK DEACTIVATED
All autonomous cron jobs RESUMED
```

### Example 2: Feature Development

```
User: /lock_mission Implement user profile page

JARVIS:
DIRECTIVE LOCK ACTIVATED (MODE SAKLEK)
Mission: Implement user profile page
All autonomous cron jobs PAUSED
Tunnel-vision mode: ACTIVE

User: I also want to update the home page

JARVIS:
⚠️ GRAY AREA DETECTED
Action: Update home page (outside mission scope)
This action requires Creator approval.
Pending Approval ID: 2345678901
Reply 'ACC 2345678901' to execute

User: REJ 2345678901

JARVIS:
❌ Action rejected
Focusing on user profile page only.
```

## Best Practices

### For Mission Locking

1. **Clear Mission Descriptions**: Be specific about the mission scope
2. **Single Focus**: Lock for one mission at a time
3. **Regular Unlocking**: Unlock when mission is complete
4. **Monitor Approvals**: Review pending approvals regularly
5. **Clear Queue**: Clear completed approvals periodically

### For Gray Area Handling

1. **Conservative Approach**: When in doubt, ask for approval
2. **Clear Explanations**: Explain why action requires approval
3. **Quick Response**: Respond to approval requests promptly
4. **Document Decisions**: Keep record of approval decisions
5. **Review Patterns**: Identify recurring gray areas

### For Cron Job Management

1. **Monitor Paused Jobs**: Track which jobs are paused
2. **Resume After Unlock**: Ensure jobs resume properly
3. **Check Job Status**: Verify job health after resume
4. **Schedule Wisely**: Avoid locking during critical job times
5. **Test Suspension**: Test pause/resume in development

## Troubleshooting

### Lock Not Activating

```javascript
// Check state file
const lockManager = getDirectiveLockManager();
const status = lockManager.getLockStatus();
console.log('Lock status:', status);

// Check Creator privileges
console.log('Is Creator:', context.isCreator);

// Check mission description
console.log('Mission:', message.replace(/^\/lock_mission\s*/i, ''));
```

### Cron Jobs Not Pausing

```javascript
// Check paused jobs list
console.log('Paused jobs:', status.pausedJobs);

// Manually pause specific job
// Integrate with actual scheduler
```

### Prompt Not Injecting

```javascript
// Check Directive Lock status in geminiService
console.log('Is Directive Locked:', this.currentIsDirectiveLocked);
console.log('Mission Description:', this.currentMissionDescription);

// Check system prompt
const prompt = this._getConversationalSystemPrompt(
  persona,
  detectedLanguage,
  isCreator,
  lockStatus.isLocked,
  lockStatus.missionDescription
);
console.log('Prompt includes lock:', prompt.includes('DIRECTIVE LOCK'));
```

### Approval Queue Not Working

```javascript
// Check queue file
console.log('Queue file exists:', fs.existsSync(approvalQueueFile));

// Check pending approvals
const pending = lockManager.getPendingApprovals();
console.log('Pending count:', pending.length);

// Test approval
const test = lockManager.addToApprovalQueue('Test action');
console.log('Test result:', test);
```

## Security Considerations

### Lock Security

1. **Creator Only**: Only Creator can lock/unlock
2. **Persistent State**: Lock state persists across restarts
3. **Audit Trail**: Track lock/unlock events
4. **Time Tracking**: Record lock duration
5. **Mission Logging**: Log mission descriptions

### Approval Security

1. **Explicit Consent**: Require explicit approval
2. **Action Logging**: Log all approval requests
3. **ID Verification**: Verify approval IDs
4. **Rejection Tracking**: Track rejected actions
5. **Queue Encryption**: Encrypt approval queue if sensitive

## Monitoring

### Lock Status Monitoring

```javascript
// Check lock status
const lockManager = getDirectiveLockManager();
const status = lockManager.getLockStatus();

console.log('Lock Status:', status.isLocked ? 'LOCKED' : 'UNLOCKED');
console.log('Mission:', status.missionDescription);
console.log('Locked At:', status.lockedAt);
console.log('Paused Jobs:', status.pausedJobs.length);
console.log('Pending Approvals:', status.pendingApprovals);
```

### Approval Queue Monitoring

```javascript
// Monitor pending approvals
const pending = lockManager.getPendingApprovals();

pending.forEach(item => {
  console.log(`ID: ${item.id}`);
  console.log(`Action: ${item.action}`);
  console.log(`Requested: ${item.requestedAt}`);
  console.log(`Status: ${item.status}`);
});
```

## Performance Considerations

### Resource Impact

- **Memory**: Minimal overhead for state management
- **CPU**: Negligible for lock status checks
- **Disk**: Small state files (<1KB)
- **Network**: No network calls for lock operations

### Cron Job Impact

- **Pause Time**: <1 second per job
- **Resume Time**: <1 second per job
- **Total Overhead**: ~10 seconds for all jobs
- **Impact**: Minimal on system performance

## Integration with Scheduler

### Python Scheduler Integration

```python
# In scheduler.py
from jarvis.security.stateManager import getDirectiveLockManager

def run_economic_data_fetch():
    lock_manager = getDirectiveLockManager()
    status = lock_manager.getLockStatus()
    
    if status.isLocked:
        print("⏸️ Job skipped: Directive Lock active")
        return
    
    # Run job normally
    print("▶️ Running economic data fetch")
    # ... job logic ...
```

### Node.js Scheduler Integration

```javascript
// In JARVIS scheduler
const { getDirectiveLockManager } = require('./security/stateManager');

function runCEOBriefing() {
  const lockManager = getDirectiveLockManager();
  const status = lockManager.getLockStatus();
  
  if (status.isLocked) {
    console.log('⏸️ Job skipped: Directive Lock active');
    return;
  }
  
  // Run job normally
  console.log('▶️ Running CEO briefing');
  // ... job logic ...
}
```

## Future Enhancements

### Planned Features

- **Time-Based Locks**: Auto-unlock after specified duration
- **Mission Templates**: Pre-defined mission templates
- **Priority Levels**: Different lock priority levels
- **Conditional Approvals**: Auto-approve certain actions
- **Approval Delegation**: Delegate approval to trusted users
- **Lock History**: Historical lock/unlock data
- **Performance Metrics**: Track lock impact on performance
- **Smart Gray Area Detection**: ML-based gray area detection

### Community Contributions

Contributions welcome for:
- Better gray area detection
- Enhanced approval workflows
- More granular control
- Performance optimizations
- Security enhancements
- Documentation improvements

## Support

For issues or questions:
- Check lock status
- Verify Creator privileges
- Review mission description
- Check cron job status
- Monitor approval queue
- Review system logs

## License

This feature is part of JARVIS AI System.
See main project license for details.
