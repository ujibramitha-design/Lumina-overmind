# JARVIS AI System Architecture

Arsitektur lengkap sistem JARVIS AI dengan detail teknis dan desain sistem.

## Overview

JARVIS adalah sistem AI otonom dengan arsitektur berlapis yang mencakup:
- **Core Layer** - Sistem dasar dan entry point
- **Security Layer** - Keamanan dan Creator recognition
- **Intelligence Layer** - AI dan knowledge graph
- **Business Layer** - Modul bisnis dan analisis
- **Advanced Layer** - Protokol canggih (Bunker, Hydra, Legacy)

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   JARVIS AI SYSTEM                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              CORE LAYER                            │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Express Server (Port 3001)                  │  │ │
│  │  │  - API Routes                                │  │ │
│  │  │  - WebSocket Server                           │  │ │
│  │  │  - Health Endpoints                           │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  PM2 Process Manager                         │  │ │
│  │  │  - Dual Process Management                   │  │ │
│  │  │  - Auto-restart                              │  │ │
│  │  │  - Log Management                            │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │            SECURITY LAYER                          │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Creator Middleware                          │  │ │
│  │  │  - Creator ID Verification                   │  │ │
│  │  │  - God Mode Override                          │  │ │
│  │  │  - Terminate Protocol                        │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Directive Lock Manager                      │  │ │
│  │  │  - MISSION_LOCK State                        │  │ │
│  │  │  - Cron Job Suspension                       │  │ │
│  │  │  - Pending Approval Queue                    │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │          INTELLIGENCE LAYER                        │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Brain Service (Unified AI)                   │  │ │
│  │  │  - Gemini 1.5 Pro (Primary)                   │  │ │
│  │  │  - Ollama Llama3 (Fallback)                  │  │ │
│  │  │  - Automatic Failover                        │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Knowledge Graph                             │  │ │
│  │  │  - Entity Extraction                         │  │ │
│  │  │  - Graph Storage                             │  │ │
│  │  │  - Vector Database                           │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Watcher Protocol                            │  │ │
│  │  │  - Codebase Awareness                        │  │ │
│  │  │  - External File Reading                     │  │ │
│  │  │  - RAG/Vector Setup                          │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │           BUSINESS LAYER                           │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Shadow CEO Modules                          │  │ │
│  │  │  - Business Radar                             │  │ │
│  │  │  - Fiscal Calendar                            │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Economic Modules                            │  │ │
│  │  │  - Macro Economics Service                   │  │ │
│  │  │  - Dynamic Pricing                           │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Financial Modules                           │  │ │
│  │  │  - CFO Ledger (Double-entry)                 │  │ │
│  │  │  - P&L Statements                            │  │ │
│  │  │  - Balance Sheets                            │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Revenue Modules                             │  │ │
│  │  │  - Scraper Agent                             │  │ │
│  │  │  - Cold Outreach                             │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │          ADVANCED LAYER                           │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Bunker Protocol                             │  │ │
│  │  │  - Local LLM Fallback                         │  │ │
│  │  │  - 100% Uptime Without Internet              │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Generative UI                                │  │ │
│  │  │  - Dynamic React Components                  │  │ │
│  │  │  - WebSocket UI Push                         │  │ │
│  │  │  - LLM-generated UI                          │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  IoT Bridge                                  │  │ │
│  │  │  - MQTT/HTTP Communication                   │  │ │
│  │  │  - Physical Hard Reboot                       │  │ │
│  │  │  - Smart Relay Control                       │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  AI Corporation                              │  │ │
│  │  │  - Bounty Manager                            │  │ │
│  │  │  - Autonomous Payouts                        │  │ │
│  │  │  - Web3 Integration                          │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Hydra Protocol                              │  │ │
│  │  │  - Multi-cloud Regeneration                  │  │ │
│  │  │  - Gossip Protocol                           │  │ │
│  │  │  - Leader Election                           │  │ │
│  │  │  - DNS Failover                              │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Legacy Protocol                             │  │ │
│  │  │  - Dead Man's Switch                         │  │ │
│  │  │  - Legacy Will Execution                     │  │ │
│  │  │  - Autonomous Sustenance                      │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │           COMMUNICATION LAYER                      │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  WhatsApp Client                              │  │ │
│  │  │  - Message Handling                          │  │ │
│  │  │  - Session Persistence                        │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Telegram Bot                                │  │ │
│  │  │  - Command Handling                          │  │ │
│  │  │  - Multimodal Support                        │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                          │                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │           DATA LAYER                               │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  SQLite Database                             │  │ │
│  │  │  - Financial Ledger                          │  │ │
│  │  │  - User Profiles                             │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  Vector Database                             │  │ │
│  │  │  - Knowledge Graph Storage                   │  │ │
│  │  │  - Document Embeddings                       │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │  JSON State Files                            │  │ │
│  │  │  - Directive Lock State                      │  │ │
│  │  │  - Pending Approvals                         │  │ │
│  │  │  - Hydra State                               │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### Core Layer

**Express Server**
- Port: 3001
- Routes: API endpoints for JARVIS operations
- WebSocket: Real-time communication
- Health: `/health` endpoint for monitoring

**PM2 Process Manager**
- Dual process: `lumina-app` (port 8000) and `jarvis-app` (port 3001)
- Auto-restart: Automatic recovery from crashes
- Log management: Centralized logging

### Security Layer

**Creator Middleware**
- Creator ID verification via WhatsApp/Telegram
- God Mode: Absolute obedience to Creator commands
- Terminate Protocol: Emergency shutdown capability
- Behavioral biometrics: User behavior analysis

**Directive Lock Manager**
- MISSION_LOCK state: Global lock flag
- Cron job suspension: Pause autonomous tasks
- Pending approval queue: Gray area action management
- Persistent state: JSON file storage

### Intelligence Layer

**Brain Service**
- Primary: Google Gemini 1.5 Pro
- Fallback: Ollama Llama3 (local)
- Failover: Automatic switch on timeout/error
- Timeout: 10 seconds for Gemini

**Knowledge Graph**
- Entity extraction: Automatic entity recognition
- Graph storage: Neo4j-compatible storage
- Vector database: RAG/Vector setup
- Context: Rich context for AI responses

**Watcher Protocol**
- Codebase awareness: External file reading
- Indexing: File indexing and search
- Analysis: Code analysis capabilities
- External: No direct codebase dependency

### Business Layer

**Shadow CEO Modules**
- Business Radar: Opportunity scanning
- Fiscal Calendar: Timing analysis
- CEO Briefing: Weekly business summary

**Economic Modules**
- Macro Economics: Economic data analysis
- Dynamic Pricing: Price optimization
- Market Analysis: Market trend analysis

**Financial Modules**
- CFO Ledger: Double-entry bookkeeping
- P&L Statements: Profit and loss reporting
- Balance Sheets: Financial position reporting

**Revenue Modules**
- Scraper Agent: Revenue scraping
- Cold Outreach: Automated outreach
- Gig Hunting: Freelance opportunities

### Advanced Layer

**Bunker Protocol**
- Local LLM: Ollama integration
- Offline capability: 100% uptime without internet
- Fast failover: <1 second switch time

**Generative UI**
- Dynamic components: LLM-generated React components
- WebSocket push: Real-time UI updates
- Safe rendering: Code sanitization

**IoT Bridge**
- MQTT: IoT device communication
- HTTP: REST API device control
- Physical reboot: Smart relay control

**AI Corporation**
- Bounty Manager: Autonomous gig posting
- Payouts: Crypto and Stripe payouts
- Web3: Ethereum integration

**Hydra Protocol**
- Multi-cloud: AWS Tokyo, DigitalOcean SG
- Gossip protocol: Peer communication
- Leader election: Raft-style election
- DNS failover: Cloudflare integration

**Legacy Protocol**
- Dead Man's Switch: 30-day threshold
- Emergency ping: Multiple endpoints
- Legacy will: Asset liquidation
- Sustenance mode: Autonomous operation

## Data Flow

### Message Processing Flow

```
User Message (WhatsApp/Telegram)
    ↓
Creator Middleware (Security Check)
    ↓
Directive Lock Check (if active)
    ↓
Brain Service (AI Processing)
    ↓
Knowledge Graph (Context Enrichment)
    ↓
Response Generation
    ↓
Channel Response (WhatsApp/Telegram)
```

### Failover Flow

```
Gemini API Request
    ↓
Timeout/Error Detected
    ↓
Switch to Ollama
    ↓
Ollama Response
    ↓
Update Provider Status
    ↓
Log Failover Event
```

### Emergency Flow

```
Dead Man's Switch Triggered
    ↓
Emergency Ping Attempt
    ↓
Ping Failed
    ↓
Execute Legacy Will
    ↓
Alert Next-of-Kin
    ↓
Liquidate Assets
    ↓
Switch to Sustenance Mode
```

## Technology Stack

### Core Technologies
- **Node.js 18+**: Runtime environment
- **Express.js**: Web framework
- **PM2**: Process management
- **Docker**: Containerization

### AI & ML
- **Google Gemini 1.5 Pro**: Primary AI model
- **Ollama**: Local LLM runtime
- **Llama3**: Fallback model

### Database & Storage
- **SQLite**: Local database
- **Vector Database**: Knowledge graph
- **JSON Files**: State persistence

### Communication
- **WhatsApp API**: WhatsApp integration
- **Telegram Bot API**: Telegram integration
- **WebSocket**: Real-time communication
- **MQTT**: IoT communication

### Web3 & Payments
- **ethers.js**: Ethereum integration
- **Stripe API**: Payment processing
- **Web3.js**: Blockchain interaction

### Cloud & Infrastructure
- **AWS**: Cloud hosting (Tokyo)
- **DigitalOcean**: Cloud hosting (Singapore)
- **Cloudflare**: DNS and CDN
- **Terraform**: Infrastructure as code

### Python Scripts
- **FastAPI**: Python API
- **Celery**: Background tasks
- **Redis**: Task queue
- **BeautifulSoup4**: Web scraping
- **Pandas**: Data analysis

## Security Architecture

### Security Layers

1. **Creator Recognition**
   - WhatsApp number verification
   - Telegram ID verification
   - Behavioral biometrics
   - Multi-factor authentication

2. **God Mode**
   - Absolute obedience to Creator
   - Override all internal logic
   - Execute any command
   - Emergency termination

3. **Directive Lock**
   - Mission-specific authorization
   - Gray area detection
   - Approval queue
   - Tunnel-vision mode

4. **Data Protection**
   - Environment variables for secrets
   - Encrypted storage
   - Secure communication (TLS)
   - Audit logging

## Performance Considerations

### Response Times
- Gemini API: 1-3 seconds
- Ollama: 2-5 seconds
- Failover: <1 second
- Total response: 3-8 seconds

### Resource Usage
- Memory: ~500MB for Ollama
- CPU: Minimal for core operations
- Disk: ~1GB for data storage
- Network: Minimal for local operations

### Scalability
- Multi-cloud deployment
- Horizontal scaling capability
- Load balancing ready
- Database sharding possible

## Monitoring & Observability

### Health Checks
- `/health` endpoint
- Provider status monitoring
- System resource monitoring
- Log aggregation

### Logging
- Error logging
- Security event logging
- Performance logging
- Audit trail

### Metrics
- Response time tracking
- Error rate monitoring
- Provider health
- System uptime

## Deployment Architecture

### Development
- Local development with PM2
- Hot reload with nodemon
- Local database
- Environment variables

### Production
- Multi-cloud deployment
- Docker containers
- PM2 process management
- Cloudflare DNS

### Disaster Recovery
- Multi-region backup
- Automatic failover
- Data replication
- Emergency procedures

## Integration Points

### Lumina Overmind Integration
- REST API communication
- WebSocket real-time updates
- Shared database (optional)
- Independent operation

### External Services
- WhatsApp API
- Telegram API
- Google Gemini API
- Stripe API
- Cloudflare API

### IoT Devices
- MQTT broker communication
- HTTP REST API
- Smart relay control
- Sensor data ingestion

## Future Enhancements

### Planned Features
- Multi-chain Web3 support
- Advanced AI models
- More cloud providers
- Better consensus algorithms
- Enhanced security
- Performance optimizations

### Research Areas
- Advanced AI capabilities
- Better automation
- Improved user experience
- Enhanced security
- Scalability improvements
