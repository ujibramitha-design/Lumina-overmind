# JARVIS AI System

Proactive, intelligent AI assistant for Lumina Overmind Enterprise with multi-channel communication, codebase awareness, and autonomous capabilities.

## 📁 Structure

```
jarvis/
├── channels/                    # Multi-Channel Communication
│   ├── whatsapp/
│   │   └── client.js           # WhatsApp connection manager
│   ├── telegram/
│   │   └── bot.js              # Telegram connection manager
│   ├── hub.js                 # Central communication hub
│   ├── ecosystem.config.js    # PM2 daemon configuration
│   ├── .env.example           # Environment template
│   └── README.md              # Channels documentation
├── proactive/                  # Proactive Engine
│   ├── scheduler.py           # Cron-job scheduler
│   ├── triggers.py            # Event triggers
│   ├── proactive_engine.py    # Main proactive logic
│   └── config.py              # Proactive configuration
├── memory/                     # Contextual Memory Module
│   ├── memory_handler.py      # Main memory management
│   ├── context_store.py       # Context storage (SQLite/Redis)
│   ├── conversation_history.py # Conversation tracking
│   └── cross_platform_sync.py  # Sync across platforms
├── awareness/                  # Codebase Awareness Module
│   ├── code_indexer.py        # File scanner & indexer
│   ├── ast_parser.py          # AST parser for code structure
│   ├── embedder.py            # Vector embedding (ChromaDB)
│   ├── vector_store.py        # ChromaDB integration
│   ├── query_engine.py        # Semantic search & retrieval
│   └── code_reader.py        # Direct file reading
└── data/                       # JARVIS Data Storage
    ├── sessions/              # Session persistence
    │   ├── whatsapp/          # WhatsApp session files
    │   └── telegram/          # Telegram session files
    ├── jarvis_memory.db       # Memory database
    └── code_index/            # Code index storage
        ├── chroma_db/        # Vector database
        ├── ast_cache/         # AST metadata cache
        └── file_cache/        # Raw file cache
```

## 🚀 Quick Start

### 1. Setup Channels

```bash
cd jarvis/channels
npm install whatsapp-web.js qrcode-terminal node-telegram-bot-api dotenv
cp .env.example .env
# Edit .env with your tokens
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### 2. Setup Python Modules

```bash
# Install Python dependencies
pip install apscheduler chromadb sentence-transformers watchdog
```

### 3. Configure Environment

Copy `jarvis/channels/.env.example` to `.env` and configure:
- Telegram Bot Token
- WhatsApp session path
- Service authentication token

## 📱 Multi-Channel Communication

### WhatsApp
- Persistent session with LocalAuth
- Auto-reconnect on server restart
- QR code authentication (first time only)
- Session saved to `jarvis/data/sessions/whatsapp/`

### Telegram
- Token-based authentication
- Robust error handling
- Automatic polling restart
- Health check endpoint

### WebSocket
- Real-time bi-directional chat
- Dashboard integration
- Mini floating widget

## 🧠 Codebase Awareness

JARVIS has complete knowledge of the Lumina Overmind codebase:

**Features:**
- AST parsing for code structure
- Vector embeddings for semantic search
- Hybrid RAG + AST approach
- Auto-reindex on file changes

**Usage:**
```python
# Query codebase
result = jarvis.query_code("How does the lead generation work?")
```

## 🔔 Proactive Engine

JARVIS initiates conversations based on:

**Triggers:**
- Time-based (morning greetings, daily summaries)
- Data-based (database changes, system events)
- System-based (CPU/memory thresholds)

**Configuration:**
```bash
JARVIS_PROACTIVE_ENABLED=true
JARVIS_MORNING_GREETING_TIME=08:00
JARVIS_DAILY_SUMMARY_TIME=18:00
```

## 💾 Memory Module

Cross-platform contextual memory:

**Storage Options:**
- SQLite (default)
- Redis (for distributed systems)
- JSON (for simple setups)

**Features:**
- Conversation history tracking
- Context persistence
- Cross-platform sync
- Configurable retention

## 🔐 Service Authentication

JARVIS uses dedicated service token for autonomous operation:

**Separate from User Auth:**
- Stored in `.env` (never exposed to frontend)
- Root/admin privileges
- HMAC-SHA256 signature
- Audit logging

**Usage:**
```python
# In API endpoints
from jarvis.middleware.jarvis_service_auth import verify_jarvis_token

@router.get("/system-status")
async def get_system_status(jarvis = Depends(verify_jarvis_token)):
    # JARVIS root access
    pass
```

## 🏥 Health Monitoring

**Health Check Endpoint:**
```
GET http://localhost:3001/health
```

**PM2 Monitoring:**
```bash
pm2 status
pm2 logs jarvis-hub
pm2 monit
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    JARVIS SYSTEM                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  WhatsApp    │  │  Telegram    │  │  WebSocket   │  │
│  │  Client      │  │  Bot         │  │  Server      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┘           │
│                           │                             │
│                    ┌──────▼──────┐                      │
│                    │  Hub (JS)   │                      │
│                    └──────┬──────┘                      │
│                           │                             │
│         ┌─────────────────┼─────────────────┐           │
│         │                 │                 │           │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐  │
│  │ Proactive   │  │   Memory    │  │  Awareness   │  │
│  │  Engine     │  │   Module    │  │   Module     │  │
│  │  (Python)   │  │  (Python)   │  │  (Python)    │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┘           │
│                           │                             │
│                    ┌──────▼──────┐                      │
│                    │ JARVIS Agent│                      │
│                    │   (Python)   │                     │
│                    └──────┬──────┘                      │
│                           │                             │
│                    ┌──────▼──────┐                      │
│                    │  Lumina     │                      │
│                    │  Overmind   │                      │
│                    │  APIs       │                      │
│                    └─────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Environment Variables

See `jarvis/channels/.env.example` for full configuration options.

### Key Settings

```bash
# Service Auth
JARVIS_SERVICE_TOKEN=your_secure_token

# Channels
JARVIS_WHATSAPP_ENABLED=true
JARVIS_TELEGRAM_ENABLED=true
JARVIS_TELEGRAM_BOT_TOKEN=your_bot_token

# Proactive
JARVIS_PROACTIVE_ENABLED=true
JARVIS_MORNING_GREETING_TIME=08:00

# Memory
JARVIS_MEMORY_STORAGE_TYPE=sqlite
JARVIS_MEMORY_DB_PATH=./jarvis/data/jarvis_memory.db

# Awareness
JARVIS_CODE_AWARENESS_ENABLED=true
JARVIS_CODE_INDEX_PATH=./jarvis/data/code_index
```

## 📝 Development

### Adding New Channels

1. Create folder in `jarvis/channels/`
2. Implement connection manager
3. Register in `hub.js`
4. Add to `.env.example`

### Adding Proactive Triggers

1. Add trigger in `jarvis/proactive/triggers.py`
2. Configure in `jarvis/proactive/config.py`
3. Register in scheduler

### Extending Memory

1. Add storage backend in `jarvis/memory/context_store.py`
2. Update configuration
3. Test cross-platform sync

## 🚨 Troubleshooting

### WhatsApp Not Connecting
- Check session directory: `jarvis/data/sessions/whatsapp/`
- Delete session and re-scan QR code
- Verify Puppeteer installation

### Telegram Not Polling
- Verify bot token is correct
- Check bot is not blocked
- Review logs for errors

### Memory Issues
- Check database path
- Verify storage type
- Review retention settings

### Code Index Not Working
- Verify embedding model installation
- Check ChromaDB persistence
- Review index path permissions

## 📚 Documentation

- [Channels Documentation](channels/README.md)
- [Proactive Engine Documentation](proactive/README.md) - Coming Soon
- [Memory Module Documentation](memory/README.md) - Coming Soon
- [Awareness Module Documentation](awareness/README.md) - Coming Soon

## 🤝 Integration

JARVIS integrates with:
- Lumina Overmind Dashboard
- Lumina Overmind APIs
- Existing authentication system
- Database systems

## 📄 License

Part of Lumina Overmind Enterprise
