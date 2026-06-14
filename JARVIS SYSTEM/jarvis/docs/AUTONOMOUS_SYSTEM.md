# JARVIS Autonomous System Documentation

Complete guide for JARVIS's autonomous capabilities: Self-Evolution and Proactive Life Integration.

## Overview

JARVIS has evolved from a reactive tool to an autonomous entity with:
- **Observer Loop**: Weekly self-refinement and autonomous code fixes
- **Life Context Integration**: Proactive assistance based on calendar, location, and weather data

## Observer Loop (Self-Evolution)

### What It Does

The Observer Loop runs weekly to:
1. Analyze past week's chat logs for misunderstandings
2. Review error logs for code bottlenecks
3. Generate self-refinement report using Gemini AI
4. Identify actionable improvements
5. Apply code fixes autonomously (with user approval)
6. Create git branches, run tests, and push PRs
7. Notify user via WhatsApp about autonomous fixes

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Observer Loop (Weekly)                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Gather Chat Logs (SQLite)                           │
│     ├── Conversation summaries                          │
│     ├── Key facts extracted                             │
│     └── User feedback patterns                          │
│                                                          │
│  2. Gather Error Logs (Log Files)                       │
│     ├── Error messages                                  │
│     ├── Stack traces                                    │
│     └── Performance metrics                             │
│                                                          │
│  3. Gemini Analysis                                     │
│     ├── Identify misunderstandings                       │
│     ├── Find weak prompts                               │
│     ├── Detect code bottlenecks                         │
│     └── Generate fixes                                   │
│                                                          │
│  4. Autonomous Fixes                                     │
│     ├── Create git branch                               │
│     ├── Apply code fix                                  │
│     ├── Run tests                                       │
│     ├── Commit changes                                  │
│     ├── Push branch                                     │
│     └── Notify user (WhatsApp)                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Configuration

```python
# In observer_loop.py
config = {
    'chat_db_path': './jarvis/data/jarvis_memory.db',
    'error_log_path': './logs/jarvis_channels.log',
    'git_repo_path': os.getcwd(),
    'git_branch_prefix': 'jarvis/auto-fix-',
    'notification_channel': 'whatsapp',
    'notification_user_id': 'your_phone_number',
    'analysis_weeks': 1,  # Analyze past 1 week
    'min_confidence': 0.7,  # Minimum confidence for auto-fix
}
```

### Scheduler Configuration

```python
# In scheduler.py
task_configs = {
    'observer_loop': {
        'enabled': True,
        'day': 'sunday',  # Weekly on Sunday
        'time': '03:00',  # 3:00 AM
        'description': 'Weekly self-refinement and autonomous fixes',
    },
}
```

### Self-Refinement Analysis

JARVIS analyzes his own performance using Gemini AI:

**Analysis Prompt:**
```
You are JARVIS, analyzing your own performance over the past week.

**Chat Logs Summary:**
- Total conversations: 150
- Platforms: whatsapp, telegram
- Date range: 2024-01-08 to 2024-01-15

**Error Logs Summary:**
- Total errors: 25
- Error types: ERROR, warning

**Your Task:**
Analyze these logs and identify:
1. Misunderstandings: Where you misunderstood user intent
2. Weak Prompts: Areas where system prompts could be improved
3. Code Bottlenecks: Performance issues or inefficient code
4. Suggestions: Concrete improvements you can make

**Output Format:**
JSON with:
- summary: Overall assessment
- misunderstandings: List of specific misunderstandings
- weak_prompts: List of prompt improvements needed
- code_bottlenecks: List of code issues found
- suggestions: List of actionable improvements
- code_fixes: List of specific code fixes with file_path, issue, fix_code, confidence
```

**Example Response:**
```json
{
  "summary": "JARVIS performed well this week with 95% user satisfaction. However, I noticed recurring misunderstandings in technical explanations.",
  "misunderstandings": [
    {
      "context": "User asked about Docker setup",
      "issue": "I provided generic instructions instead of project-specific ones",
      "frequency": 3
    }
  ],
  "weak_prompts": [
    {
      "prompt": "Conversational system prompt",
      "improvement": "Add more context about project structure"
    }
  ],
  "code_bottlenecks": [
    {
      "file": "jarvis/channels/hub.js",
      "issue": "Synchronous message processing causes delays",
      "impact": "medium"
    }
  ],
  "suggestions": [
    "Add project-specific documentation to system prompt",
    "Implement async message processing"
  ],
  "code_fixes": [
    {
      "file_path": "jarvis/channels/hub.js",
      "issue": "Synchronous message processing",
      "fix_code": "async function processMessage(msg) { ... }",
      "confidence": 0.85
    }
  ]
}
```

### Autonomous Fix Process

When JARVIS identifies a code fix with confidence ≥ 0.7:

1. **Create Git Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b jarvis/auto-fix-20240115-030000
   ```

2. **Apply Fix with Backup**
   ```python
   # Create backup
   backup_path = f'{file_path}.backup_{timestamp}'
   shutil.copy2(file_path, backup_path)
   
   # Apply fix
   with open(file_path, 'w') as f:
       f.write(fix_code)
   ```

3. **Run Tests**
   ```bash
   npm test  # or pytest for Python
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "JARVIS Auto-Fix: [issue description]"
   ```

5. **Push Branch**
   ```bash
   git push origin jarvis/auto-fix-20240115-030000
   ```

6. **Notify User**
   ```
   🤖 JARVIS Auto-Fix PR Created
   ==============================
   
   Branch: jarvis/auto-fix-20240115-030000
   Issue: Synchronous message processing
   Tests: ✅ Passed
   
   I've identified and fixed an issue autonomously. Please review and merge if approved.
   ```

### Safety Features

- **Minimum Confidence**: Only applies fixes with confidence ≥ 0.7
- **Automatic Backups**: Creates timestamped backups before changes
- **Test Verification**: Runs tests before committing
- **User Notification**: Always notifies user of autonomous changes
- **Manual Review**: User must review and merge PR manually

## Life Context Integration

### What It Does

JARVIS receives life data from Mobile APK:
- **Calendar Events**: Meetings, appointments, reminders
- **Geolocation**: Current location, movement patterns
- **Weather**: Local weather conditions

Proactive alerts based on analysis:
- Calendar conflicts (overlapping events)
- Travel time conflicts (can't reach event on time)
- Weather conflicts (outdoor events in bad weather)
- Location-based suggestions

### API Endpoints

#### Sync Life Data

```http
POST /api/jarvis-life/sync
Content-Type: application/json
X-Jarvis-Service-Token: your_token

{
  "user_id": "user_123",
  "device_id": "device_abc",
  "calendar_events": [
    {
      "id": "event_1",
      "title": "Team Meeting",
      "start_time": "2024-01-15T10:00:00Z",
      "end_time": "2024-01-15T11:00:00Z",
      "location": "Office Building A",
      "event_type": "meeting"
    }
  ],
  "geolocation": {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "accuracy": 10.0,
    "timestamp": "2024-01-15T09:30:00Z"
  },
  "weather": {
    "temperature": 22.5,
    "humidity": 65.0,
    "condition": "sunny",
    "timestamp": "2024-01-15T09:30:00Z"
  }
}
```

#### Get Calendar Events

```http
GET /api/jarvis-life/events/{user_id}?start_date=2024-01-15&end_date=2024-01-16
X-Jarvis-Service-Token: your_token
```

#### Get Current Location

```http
GET /api/jarvis-life/location/{user_id}
X-Jarvis-Service-Token: your_token
```

#### Get Current Weather

```http
GET /api/jarvis-life/weather/{user_id}
X-Jarvis-Service-Token: your_token
```

#### Get Conflict Alerts

```http
GET /api/jarvis-life/alerts/{user_id}
X-Jarvis-Service-Token: your_token
```

### Conflict Detection

#### Calendar Conflicts

**Overlapping Events:**
```python
def events_overlap(event1, event2):
    return (
        event1.start_time < event2.end_time and
        event1.end_time > event2.start_time
    )
```

**Travel Time Conflicts:**
```python
# Check if user can reach event on time
travel_time = estimate_travel_time(current_location, event.location)
time_available = (event.start_time - now).total_seconds() / 60

if time_available < travel_time:
    # Alert: Cannot reach event on time
```

#### Weather Conflicts

**Outdoor Events in Bad Weather:**
```python
if is_outdoor_event(event) and weather.condition in ['rainy', 'stormy']:
    # Alert: Weather conflict
```

**Extreme Temperatures:**
```python
if weather.temperature > 35 or weather.temperature < 0:
    # Alert: Extreme temperature
```

### Proactive Notifications

When high-severity conflicts are detected, JARVIS sends proactive WhatsApp messages:

**Calendar Conflict Alert:**
```
🚨 JARVIS Proactive Alert
========================

Alert Type: calendar_conflict
Severity: HIGH

Message: Calendar conflict: 'Team Meeting' overlaps with 'Client Call'

Suggested Actions:
1. Reschedule 'Team Meeting' to a different time
2. Reschedule 'Client Call' to a different time
3. Decline one of the events

Affected Events: event_1, event_2

Timestamp: 2024-01-15 09:30:00
```

**Location Conflict Alert:**
```
🚨 JARVIS Proactive Alert
========================

Alert Type: location_conflict
Severity: HIGH

Message: Cannot reach 'Team Meeting' on time from current location

Suggested Actions:
1. Leave immediately
2. Request to join virtually
3. Reschedule the event
4. Request a later start time

Affected Events: event_1

Timestamp: 2024-01-15 09:30:00
```

**Weather Conflict Alert:**
```
🚨 JARVIS Proactive Alert
========================

Alert Type: weather_conflict
Severity: MEDIUM

Message: Weather alert for 'Outdoor Event': rainy conditions expected

Suggested Actions:
1. Move event indoors
2. Reschedule for better weather
3. Prepare rain gear/umbrella
4. Request virtual attendance

Affected Events: event_2

Timestamp: 2024-01-15 09:30:00
```

## Mobile APK Integration

### Sending Life Data

```javascript
// In Mobile APK
async function syncLifeData() {
  const payload = {
    user_id: getUserId(),
    device_id: getDeviceId(),
    calendar_events: await getCalendarEvents(),
    geolocation: await getCurrentLocation(),
    weather: await getCurrentWeather(),
  };
  
  const response = await fetch('https://jarvis.yourdomain.com/api/jarvis-life/sync', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Jarvis-Service-Token': getServiceToken(),
    },
    body: JSON.stringify(payload),
  });
  
  const data = await response.json();
  console.log('Sync result:', data);
}
```

### Receiving Alerts

```javascript
// In Mobile APK
async function getConflictAlerts() {
  const response = await fetch(
    `https://jarvis.yourdomain.com/api/jarvis-life/alerts/${getUserId()}`,
    {
      headers: {
        'X-Jarvis-Service-Token': getServiceToken(),
      },
    }
  );
  
  const data = await response.json();
  return data.alerts;
}
```

## Configuration

### Environment Variables

```bash
# Observer Loop
JARVIS_OBSERVER_LOOP_ENABLED=true
JARVIS_OBSERVER_LOOP_DAY=sunday
JARVIS_OBSERVER_LOOP_TIME=03:00
JARVIS_GIT_BRANCH_PREFIX=jarvis/auto-fix-
JARVIS_NOTIFICATION_CHANNEL=whatsapp
JARVIS_NOTIFICATION_USER_ID=your_phone_number

# Life Data
JARVIS_LIFE_DATA_ENABLED=true
JARVIS_WEATHER_API_KEY=your_weather_api_key
JARVIS_MAPS_API_KEY=your_google_maps_api_key
```

### Database Schema

**Conversation Summaries Table:**
```sql
CREATE TABLE conversation_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    summary TEXT NOT NULL,
    key_points TEXT,
    token_count INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(platform, user_id, date)
);
```

## Monitoring

### Observer Loop Statistics

```python
observer_loop = get_observer_loop()

stats = observer_loop.stats
print(f"Last analysis: {stats['last_analysis']}")
print(f"Total analyses: {stats['total_analyses']}")
print(f"Auto fixes applied: {stats['auto_fixes_applied']}")
print(f"PR notifications sent: {stats['pr_notifications_sent']}")
```

### Life Data Alerts

```python
# Get all alerts
alerts = conflict_alerts

# Get user-specific alerts
user_alerts = [a for a in alerts if a.get('user_id') == 'user_123']

# Get high-severity alerts
critical_alerts = [a for a in alerts if a.severity == 'critical']
```

## Best Practices

### For Observer Loop

1. **Review PRs Carefully**: Always review autonomous fixes before merging
2. **Monitor Confidence Levels**: Adjust `min_confidence` based on results
3. **Keep Backups**: Don't delete backup files immediately
4. **Test Thoroughly**: Ensure tests pass before merging
5. **Document Changes**: Add comments to auto-generated code

### For Life Data

1. **Privacy First**: Only collect necessary data
2. **User Consent**: Always get user permission for data collection
3. **Secure Transmission**: Use HTTPS and authentication
4. **Data Retention**: Clean up old data regularly
5. **Opt-Out Option**: Allow users to disable features

### For Autonomous Fixes

1. **Start Conservative**: Set high confidence threshold initially
2. **Monitor Results**: Track success rate of auto-fixes
3. **Gradual Expansion**: Increase scope as confidence grows
4. **Rollback Plan**: Always have rollback procedure ready
5. **User Feedback**: Collect feedback on autonomous changes

## Troubleshooting

### Observer Loop Issues

**Git Branch Creation Fails:**
```bash
# Check git status
git status

# Ensure clean working directory
git stash

# Pull latest changes
git pull origin main
```

**Tests Fail:**
```bash
# Run tests manually
npm test

# Check test logs
cat npm-debug.log

# Fix issues manually
```

**Gemini Analysis Fails:**
```python
# Check API key
echo $GEMINI_API_KEY

# Test Gemini connection
python -c "from services.geminiService import getGeminiService; service = getGeminiService(); print(service.healthCheck())"
```

### Life Data Issues

**API Returns 403:**
```python
# Verify service token
X-Jarvis-Service-Token: your_token

# Check token verification logic
def verify_service_token(token):
    return token == os.getenv('JARVIS_SERVICE_TOKEN')
```

**No Alerts Generated:**
```python
# Check if data is being received
print(life_data_store)

# Check analysis logic
await analyze_life_data(payload)

# Check notification system
await send_proactive_notification(user_id, alert)
```

## Security Considerations

### Observer Loop

- **Git Access**: Ensure JARVIS has proper git permissions
- **File Permissions**: Limit write access to specific directories
- **Branch Naming**: Use predictable branch naming pattern
- **Test Execution**: Run tests in isolated environment
- **Rollback Capability**: Always maintain ability to rollback

### Life Data

- **Authentication**: Require service token for all endpoints
- **Encryption**: Encrypt sensitive data at rest
- **Access Control**: Limit access to user's own data
- **Data Minimization**: Only collect necessary data
- **Audit Logging**: Log all data access

## Future Enhancements

### Planned Features

- **Multi-Repository Support**: Auto-fixes across multiple repos
- **Rollback Automation**: Automatic rollback if tests fail
- **Performance Monitoring**: Track JARVIS performance metrics
- **User Feedback Loop**: Learn from user corrections
- **Advanced Weather**: Use weather API for accurate forecasts
- **Traffic Analysis**: Real-time traffic data for travel time
- **Calendar Integration**: Direct calendar API integration
- **Smart Suggestions**: AI-powered proactive suggestions

### Community Contributions

Contributions welcome for:
- Additional conflict detection rules
- Better analysis prompts
- Enhanced security features
- Performance optimizations
- Documentation improvements

## Support

For issues or questions:
- Check Observer Loop logs
- Review git branch history
- Verify API authentication
- Test with simple scenarios first
- Monitor system resources
- Check network connectivity

## License

This feature is part of JARVIS AI System.
See main project license for details.
