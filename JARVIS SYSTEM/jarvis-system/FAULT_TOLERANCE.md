# JARVIS Fault Tolerance Documentation

Critical architectural documentation for JARVIS isolation and fault tolerance from lumina-overmind.

## Overview

JARVIS and lumina-overmind are strictly decoupled for fault tolerance. If lumina-overmind crashes, throws a fatal error, or goes offline, JARVIS remains 100% alive and unaffected.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Fault-Tolerant Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Process 1: lumina-app (Main Program)                     │
│  ├── Port: 8000                                          │
│  ├── Script: ./api/main.py                              │
│  ├── Memory Limit: 1G                                   │
│  ├── Autorestart: true                                  │
│  └── Purpose: Main Lumina Overmind application          │
│                                                          │
│  Process 2: jarvis-app (Isolated JARVIS)                 │
│  ├── Port: 3001                                         │
│  ├── Script: ./jarvis-system/index.js                   │
│  ├── Memory Limit: 500M                                 │
│  ├── Autorestart: true                                  │
│  └── Purpose: Isolated JARVIS AI system                 │
│                                                          │
│  Communication Bridge:                                  │
│  ├── REST API: http://localhost:3001/api/*              │
│  ├── Lumina API: http://localhost:8000                  │
│  ├── Manual Connect/Disconnect                          │
│  └── Creator-only control                               │
│                                                          │
│  Watcher Protocol:                                      │
│  ├── External codebase reading                          │
│  ├── RAG/Vector indexing                               │
│  ├── No direct integration                              │
│  └── 100% codebase awareness                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

### Isolated JARVIS System

```
lumina-overmind/
├── jarvis-system/                    # ISOLATED JARVIS ROOT
│   ├── index.js                      # JARVIS entry point
│   ├── channels/                     # Communication channels
│   │   ├── services/
│   │   │   └── geminiService.js     # Gemini AI brain
│   │   ├── telegram/
│   │   │   └── bot.js              # Telegram integration
│   │   └── whatsapp/
│   │       └── client.js            # WhatsApp integration
│   ├── security/                     # Security layer
│   │   └── creatorMiddleware.js     # Creator recognition
│   ├── intelligence/                 # Intelligence modules
│   │   └── watcherProtocol.js       # Codebase awareness
│   ├── omniscient/                   # Document ingestion
│   │   └── documentIngestionEngine.js
│   ├── economics/                    # Economic modules
│   │   ├── macroEconomicsService.js
│   │   └── dynamicPricing.js
│   ├── shadow_ceo/                   # CEO modules
│   │   ├── businessRadar.js
│   │   └── fiscalCalendar.js
│   ├── creative/                     # Creative modules
│   │   └── visualArchitect.js
│   ├── finance/                      # Financial modules
│   │   └── financialLedger.js
│   ├── revenue/                      # Revenue modules
│   │   ├── scraperAgent.js
│   │   └── coldOutreach.js
│   ├── business/                     # Business modules
│   │   ├── targetAnalyzer.js
│   │   └── vipCRM.js
│   ├── empire/                       # Empire modules
│   │   ├── gigHunter.js
│   │   └── socialMediaEngine.js
│   ├── invisible/                    # Invisible modules
│   │   ├── empireBuilder.js
│   │   └── darkSocialAgent.js
│   ├── data/                         # JARVIS data
│   │   ├── sessions/
│   │   ├── financial_ledger.db
│   │   └── vector_db/
│   ├── logs/                         # JARVIS logs
│   └── .env                         # JARVIS environment
│
├── api/                             # Lumina main program
├── dashboard/                       # Lumina dashboard
├── guide lengkap projek/            # Documentation
└── ecosystem.config.js              # PM2 configuration
```

### Key Isolation Points

**1. Directory Isolation:**
- All JARVIS files in `/jarvis-system/`
- No direct imports from lumina-overmind
- Separate `.env` file
- Separate data directory

**2. Process Isolation:**
- Separate PM2 apps
- Different ports (8000 vs 3001)
- Separate memory limits
- Independent autorestart

**3. Communication Isolation:**
- REST API bridge only
- Manual connect/disconnect
- Creator-only control
- No direct code dependencies

## PM2 Configuration

### ecosystem.config.js

```javascript
module.exports = {
  apps: [
    {
      name: 'lumina-app',
      script: './api/main.py',
      interpreter: 'python',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8000,
      },
      error_file: './logs/lumina-error.log',
      out_file: './logs/lumina-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
    },
    {
      name: 'jarvis-app',
      script: './jarvis-system/index.js',
      interpreter: 'node',
      cwd: './',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        JARVIS_PORT: 3001,
        LUMINA_API_URL: 'http://localhost:8000',
      },
      error_file: './logs/jarvis-error.log',
      out_file: './logs/jarvis-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
    },
  ],
};
```

### Starting the System

```bash
# Start both processes
pm2 start ecosystem.config.js

# Start only Lumina
pm2 start ecosystem.config.js --only lumina-app

# Start only JARVIS
pm2 start ecosystem.config.js --only jarvis-app

# Check status
pm2 status

# View logs
pm2 logs lumina-app
pm2 logs jarvis-app
```

## Watcher Protocol

### External Codebase Awareness

JARVIS maintains 100% codebase awareness of lumina-overmind without direct integration.

**How It Works:**

1. **External Reading**: JARVIS uses Node.js `fs` module to read lumina-overmind files
2. **RAG/Vector Indexing**: Files are indexed using document ingestion engine
3. **No Dependencies**: No direct imports or requires from lumina-overmind
4. **Periodic Scanning**: Codebase scanned every 60 seconds
5. **Query Capability**: JARVIS can query indexed codebase

### Watcher Protocol Code

```javascript
const { getWatcherProtocol } = require('./intelligence/watcherProtocol');

const watcher = getWatcherProtocol({
  luminaPath: '../',  // Path to lumina-overmind root
  watchInterval: 60000,  // Scan every minute
  excludePatterns: [
    'node_modules',
    '.git',
    '__pycache__',
    'jarvis-system',  // Don't watch JARVIS itself
  ],
  fileExtensions: ['.js', '.ts', '.py', '.json', '.md'],
  namespace: 'lumina-codebase',
});

// Start watching
await watcher.startWatching();

// Query codebase
const results = await watcher.queryCodebase('How does the API handle authentication?');

// Get file content
const fileContent = await watcher.getFileContent('api/main.py');

// Get directory structure
const structure = await watcher.getDirectoryStructure();
```

### Example: External Codebase Reading

```javascript
// JARVIS reads Lumina codebase externally
const fs = require('fs');
const path = require('path');

// Read Lumina main file
const luminaPath = path.resolve('../api/main.py');
const content = fs.readFileSync(luminaPath, 'utf-8');

// Index the file
const result = await documentIngestionEngine.ingestDocument(
  Buffer.from(content),
  'py',
  'lumina-codebase',
  { filePath: luminaPath }
);

// Query the indexed codebase
const queryResults = await documentIngestionEngine.queryVectorDB(
  'What are the API endpoints?',
  'lumina-codebase',
  5
);
```

## Connection Bridge

### REST API Bridge

JARVIS uses a REST API bridge to communicate with Lumina.

**Bridge Endpoints:**

```javascript
// Connect to Lumina
POST /api/bridge/connect
Response: { success: true, message: 'Connected to Lumina API' }

// Disconnect from Lumina
POST /api/bridge/disconnect
Response: { success: true, message: 'Disconnected from Lumina API' }

// Bridge status
GET /api/bridge/status
Response: { connected: true, luminaApiUrl: 'http://localhost:8000' }

// JARVIS message endpoint
POST /api/jarvis/message
Body: { userId, message, platform, context }
Response: { success: true, response: 'JARVIS response' }
```

### Connection Logic

```javascript
class JarvisSystem {
  async connectToLumina() {
    try {
      const response = await fetch(`${this.luminaApiUrl}/health`);
      
      if (response.ok) {
        this.isConnectedToLumina = true;
        this.lastConnectionTime = new Date().toISOString();
        
        return {
          success: true,
          message: 'Successfully connected to Lumina API',
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  }
  
  async disconnectFromLumina() {
    this.isConnectedToLumina = false;
    this.lastConnectionTime = null;
    
    return {
      success: true,
      message: 'Successfully disconnected from Lumina API',
    };
  }
}
```

## Creator Commands

### Connect/Disconnect Commands

**Connect to Lumina:**
```
User: "Jarvis, connect to Lumina's API"

JARVIS Response: "Connected to Lumina API. JARVIS can now communicate with Lumina."

Requirements: Creator privileges only
```

**Disconnect from Lumina:**
```
User: "Jarvis, isolate yourself from Lumina"

JARVIS Response: "Disconnected from Lumina API. JARVIS is now running in isolated mode."

Requirements: Creator privileges only
```

**Check Connection Status:**
```
User: "Jarvis, what is your connection status?"

JARVIS Response: "Connection Status: Connected to Lumina API (http://localhost:8000)
Last Connection: 2024-01-15T10:00:00Z
Mode: Connected"
```

### Command Implementation

```javascript
// In geminiService.js
async _handleLuminaConnect(context) {
  if (!context.isCreator) {
    return {
      success: false,
      response: 'Lumina connection control requires Creator privileges.',
      isLuminaCommand: true,
    };
  }
  
  const jarvisSystem = require('../index');
  const result = await jarvisSystem.connectToLumina();
  
  return {
    success: result.success,
    response: result.success 
      ? 'Connected to Lumina API. JARVIS can now communicate with Lumina.'
      : `Failed to connect: ${result.error}`,
    isLuminaCommand: true,
  };
}

async _handleLuminaDisconnect(context) {
  if (!context.isCreator) {
    return {
      success: false,
      response: 'Lumina connection control requires Creator privileges.',
      isLuminaCommand: true,
    };
  }
  
  const jarvisSystem = require('../index');
  const result = await jarvisSystem.disconnectFromLumina();
  
  return {
    success: result.success,
    response: result.success 
      ? 'Disconnected from Lumina API. JARVIS is now running in isolated mode.'
      : `Failed to disconnect: ${result.error}`,
    isLuminaCommand: true,
  };
}
```

## Fault Tolerance Scenarios

### Scenario 1: Lumina Crashes

**What Happens:**
- Lumina app crashes (memory leak, fatal error, etc.)
- PM2 detects crash and restarts lumina-app
- JARVIS app continues running unaffected
- JARVIS maintains 100% functionality
- No data loss in JARVIS

**JARVIS Status:**
- ✅ Still alive and responsive
- ✅ All channels operational (WhatsApp, Telegram)
- ✅ AI brain functional
- ✅ Database accessible
- ✅ Watcher Protocol active

**Recovery:**
- Lumina restarts automatically
- JARVIS can reconnect when ready
- No manual intervention required

### Scenario 2: Lumina Goes Offline

**What Happens:**
- Lumina network connection lost
- Lumina app stops responding
- JARVIS detects connection failure
- JARVIS continues in isolated mode
- JARVIS functions independently

**JARVIS Status:**
- ✅ Still alive and responsive
- ✅ All channels operational
- ✅ AI brain functional
- ✅ Database accessible
- ⚠️ Lumina bridge disconnected (expected)

**Recovery:**
- JARVIS auto-reconnects when Lumina back online
- Creator can manually reconnect via command
- No data loss

### Scenario 3: JARVIS Crashes

**What Happens:**
- JARVIS app crashes
- PM2 detects crash and restarts jarvis-app
- Lumina continues running unaffected
- Lumina maintains 100% functionality

**Lumina Status:**
- ✅ Still alive and responsive
- ✅ API endpoints operational
- ✅ Dashboard accessible
- ✅ Database accessible

**Recovery:**
- JARVIS restarts automatically
- Reconnects to Lumina if configured
- No data loss in Lumina

### Scenario 4: Both Crash

**What Happens:**
- Both apps crash simultaneously
- PM2 detects both crashes
- Both apps restart independently
- No cross-contamination
- Independent recovery

**Recovery:**
- Both apps restart automatically
- No manual intervention required
- Independent health checks
- Separate log files

## Migration Steps

### Step 1: Create Isolated Directory

```bash
# Create jarvis-system directory
mkdir jarvis-system

# Create subdirectories
mkdir jarvis-system/channels
mkdir jarvis-system/channels/services
mkdir jarvis-system/channels/telegram
mkdir jarvis-system/channels/whatsapp
mkdir jarvis-system/security
mkdir jarvis-system/intelligence
mkdir jarvis-system/omniscient
mkdir jarvis-system/economics
mkdir jarvis-system/shadow_ceo
mkdir jarvis-system/creative
mkdir jarvis-system/finance
mkdir jarvis-system/revenue
mkdir jarvis-system/business
mkdir jarvis-system/empire
mkdir jarvis-system/invisible
mkdir jarvis-system/data
mkdir jarvis-system/data/sessions
mkdir jarvis-system/logs
```

### Step 2: Move JARVIS Files

```bash
# Move all JARVIS files to jarvis-system
mv jarvis/* jarvis-system/

# Verify structure
ls jarvis-system/
```

### Step 3: Update Imports

**Before (in lumina-overmind):**
```javascript
const { getGeminiService } = require('./jarvis/channels/services/geminiService');
```

**After (isolated):**
```javascript
// No direct imports from JARVIS
// Use REST API bridge instead
const response = await fetch('http://localhost:3001/api/jarvis/message', {
  method: 'POST',
  body: JSON.stringify({ userId, message, platform, context }),
});
```

### Step 4: Update PM2 Configuration

```bash
# Create ecosystem.config.js
# (See configuration above)

# Start both processes
pm2 start ecosystem.config.js

# Verify status
pm2 status
```

### Step 5: Test Isolation

```bash
# Test Lumina crash
pm2 stop lumina-app
# Verify JARVIS still running
curl http://localhost:3001/health

# Test JARVIS crash
pm2 stop jarvis-app
# Verify Lumina still running
curl http://localhost:8000/health

# Restart both
pm2 restart all
```

## Best Practices

### For Fault Tolerance

1. **Separate Logs**: Keep log files separate for each process
2. **Memory Limits**: Set appropriate memory limits for each process
3. **Autorestart**: Enable autorestart for both processes
4. **Health Checks**: Implement health check endpoints
5. **Monitoring**: Monitor both processes independently
6. **Backup**: Regular backups of both databases
7. **Testing**: Regular fault tolerance testing

### For Connection Bridge

1. **Manual Control**: Keep connection under Creator control
2. **Error Handling**: Robust error handling for connection failures
3. **Timeouts**: Set appropriate timeouts for API calls
4. **Retry Logic**: Implement retry logic for transient failures
5. **Status Monitoring**: Monitor connection status continuously
6. **Graceful Degradation**: Function without connection when needed

### For Watcher Protocol

1. **Exclude Patterns**: Exclude unnecessary directories
2. **File Size Limits**: Skip very large files
3. **Scan Interval**: Balance between freshness and performance
4. **Error Handling**: Handle file read errors gracefully
5. **Namespace Management**: Use separate namespaces for different codebases
6. **Query Optimization**: Optimize vector queries for performance

## Troubleshooting

### Both Processes Not Starting

```bash
# Check PM2 logs
pm2 logs --lines 50

# Check port conflicts
netstat -ano | findstr :8000
netstat -ano | findstr :3001

# Check file permissions
ls -la jarvis-system/
```

### JARVIS Cannot Connect to Lumina

```bash
# Check Lumina status
pm2 status lumina-app

# Check Lumina health
curl http://localhost:8000/health

# Check JARVIS connection status
curl http://localhost:3001/api/bridge/status

# Manual reconnect
curl -X POST http://localhost:3001/api/bridge/connect
```

### Watcher Protocol Not Working

```javascript
// Check watcher status
const status = watcher.getWatchStatus();
console.log(status);

// Check lumina path
console.log('Lumina path exists:', fs.existsSync(config.luminaPath));

// Test file reading
const testFile = await watcher.getFileContent('api/main.py');
console.log('File read test:', testFile);
```

## Security Considerations

### Isolation Security

1. **Access Control**: Restrict access to JARVIS API
2. **Authentication**: Implement API authentication
3. **Firewall**: Configure firewall rules
4. **Network Segmentation**: Separate network segments if possible
5. **Secrets Management**: Keep secrets separate for each process

### Bridge Security

1. **Creator Only**: Connection control requires Creator privileges
2. **HTTPS**: Use HTTPS in production
3. **Rate Limiting**: Implement rate limiting on bridge
4. **Input Validation**: Validate all bridge inputs
5. **Audit Logging**: Log all bridge activities

## Monitoring

### PM2 Monitoring

```bash
# Real-time monitoring
pm2 monit

# Resource usage
pm2 show lumina-app
pm2 show jarvis-app

# Logs
pm2 logs lumina-app
pm2 logs jarvis-app
```

### Health Checks

```bash
# Lumina health
curl http://localhost:8000/health

# JARVIS health
curl http://localhost:3001/health

# Bridge status
curl http://localhost:3001/api/bridge/status
```

### Custom Monitoring

```javascript
// Monitor connection status
setInterval(async () => {
  const status = await fetch('http://localhost:3001/api/bridge/status');
  const data = await status.json();
  console.log('Bridge Status:', data);
}, 60000);
```

## Performance Considerations

### Resource Allocation

- **Lumina**: 1GB memory limit (main application)
- **JARVIS**: 500MB memory limit (AI system)
- **CPU**: Balanced allocation
- **Disk**: Separate storage for each process

### Network

- **Lumina Port**: 8000
- **JARVIS Port**: 3001
- **Bridge**: REST API over HTTP
- **Latency**: <100ms for local bridge

### Scalability

- **Horizontal Scaling**: Can scale each process independently
- **Load Balancing**: Can add load balancer for each process
- **Database**: Separate databases for each process
- **Caching**: Separate caching for each process

## Disaster Recovery

### Backup Strategy

1. **Database Backups**: Regular backups of both databases
2. **Code Backups**: Version control for both codebases
3. **Configuration Backups**: Backup PM2 configuration
4. **Log Backups**: Archive log files regularly
5. **Secrets Backups**: Secure backup of secrets

### Recovery Procedure

1. **Stop Processes**: `pm2 stop all`
2. **Restore Databases**: Restore from backups
3. **Restore Code**: Checkout from version control
4. **Restore Configuration**: Restore ecosystem.config.js
5. **Start Processes**: `pm2 start ecosystem.config.js`
6. **Verify Health**: Check health endpoints
7. **Test Bridge**: Test connection bridge

## Future Enhancements

### Planned Features

- **WebSocket Bridge**: Real-time bidirectional communication
- **Message Queue**: Use message queue for reliable communication
- **Service Discovery**: Automatic service discovery
- **Load Balancing**: Built-in load balancing
- **Health Monitoring**: Advanced health monitoring
- **Auto-Scaling**: Automatic scaling based on load
- **Circuit Breaker**: Circuit breaker pattern for bridge
- **Retry with Backoff**: Exponential backoff for retries

### Community Contributions

Contributions welcome for:
- Better isolation strategies
- Advanced fault tolerance patterns
- Performance optimizations
- Security enhancements
- Monitoring improvements
- Documentation improvements

## Support

For issues or questions:
- Check PM2 logs
- Verify port availability
- Test health endpoints
- Review configuration
- Check file permissions
- Monitor resource usage

## License

This feature is part of JARVIS AI System.
See main project license for details.
