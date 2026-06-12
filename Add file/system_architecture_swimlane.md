# HUNTER_AGENT_AI_MARKETING_DIGITAL - System Architecture Swimlane

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                              SYSTEM ARCHITECTURE                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│    NEXT.JS UI       │    │   FASTAPI SERVER    │    │  RUNNER MANAGER     │    │   PYTHON SCRIPTS     │
│   (Port 3000)       │    │   (Port 8000)       │    │   (Process Mgmt)    │    │   (Background)       │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘    └─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            USER INTERACTIONS                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

👤 USER ACTIONS:
├─ 🌐 Opens http://localhost:3000/orchestrator
├─ 👁️ Views Master Orchestrator Dashboard
├─ 🔄 Clicks Toggle Switches to Start/Stop Runners
├─ 📊 Monitors Real-time Status Updates
└─ ⚠️ Views Error Messages (if any)

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           FRONTEND FLOW (NEXT.JS)                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🎯 NEXT.JS COMPONENTS:
├─ 📱 app/orchestrator/page.tsx
│  ├─ 🔍 useEffect() → fetch('http://localhost:8000/api/runners') [Every 5 seconds]
│  ├─ 🔄 handleToggleRunner() → POST to FastAPI
│  ├─ ⏳ setLoadingStates() → Show Spinner
│  ├─ 📊 setRunners() → Update UI State
│  └─ ❌ setApiError() → Display Errors
│
├─ 🎨 UI Components:
│  ├─ 🃏 Switch Component (Custom Toggle)
│  ├─ 📋 Card Components (Runner Cards)
│  ├─ 📈 System Metrics Cards
│  └─ 🏷️ Badge Components (Status Indicators)
│
└─ 🔄 State Management:
   ├─ 📊 runners: RunnerCard[] (6 runners)
   ├─ ⚡ loadingStates: Record<string, boolean>
   ├─ 🚨 apiError: string | null
   ├─ 🕐 lastSync: Date
   └─ 📈 systemMetrics: SystemMetrics

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            API LAYER (FASTAPI)                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🚀 FASTAPI SERVER:
├─ 🌐 api/main.py
│  ├─ 🔧 CORS Middleware (localhost:3000)
│  ├─ 📊 GET /api/runners → Return all runners status
│  ├─ ▶️ POST /api/runners/{name}/start → Start runner
│  ├─ ⏹️ POST /api/runners/{name}/stop → Stop runner
│  ├─ 🏥 GET /health → Health check
│  └─ 📋 GET /api/system → System information
│
├─ 🛠️ Core Modules:
│  ├─ 📦 utils/process_manager.py
│  │  ├─ 🏃 RunnerManager Class
│  │  ├─ 🔄 start_runner(script_name)
│  │  ├─ 🛑 stop_runner(script_name)
│  │  ├─ 📊 get_status()
│  │  └─ 🧹 cleanup_dead_processes()
│  │
│  └─ 📝 utils/__init__.py
│
└─ 🔗 API Response Format:
   ├─ ✅ success: boolean
   ├─ 📦 data: object
   ├─ 🕐 timestamp: string
   └─ ❌ error: string (if failed)

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         PROCESS MANAGEMENT LAYER                                       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🎛️ RUNNER MANAGER:
├─ 🗃️ Process Storage:
│  ├─ 📋 processes: Dict[string, ProcessInfo]
│  └─ 🔄 runner_mapping: Dict[string, script_file]
│
├─ 🚀 Process Operations:
│  ├─ ▶️ subprocess.Popen() → Start Python Script
│  ├─ 📊 psutil.Process() → Monitor CPU/Memory
│  ├─ 🛑 process.terminate() → Graceful Shutdown
│  ├─ 💀 process.kill() → Force Kill (if needed)
│  └─ 👶 process.children() → Cleanup Child Processes
│
└─ 📊 Process Information:
   ├─ 🆔 PID (Process ID)
   ├─ 💻 CPU Usage (%)
   ├─ 🧠 Memory Usage (%)
   ├─ 🕐 Start Time
   └─ 📝 Command Line

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          PYTHON SCRIPTS LAYER                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🤖 PRODUCTION RUNNERS:
├─ 👥 lead_generation → run_lead_generation.py
│  └─ 📈 Multi-engine lead acquisition system
│
├─ 🏛️ banten_government → run_banten_government_intelligence.py
│  └─ 📋 PNS/P3K market analysis
│
├─ 🚗 ride_hailing → run_ride_hailing_intelligence.py
│  └─ 📊 Transportation pattern analysis
│
├─ 🏠 property_scraper → run_property_market_scraper.py
│  └─ 🏘️ Real estate data monitoring
│
├─ ✅ social_verifier → run_social_proof_verifier.py
│  └─ 📱 Social media sentiment analysis
│
└─ 📈 behavioral_tester → run_behavioral_velocity_tester.py
   └─ 👤 User behavior tracking

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            DATA FLOW PATTERNS                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🔄 REAL-TIME SYNC FLOW:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   NEXT.JS   │───▶│  FASTAPI    │───▶│ RUNNER MGR  │───▶│   PSUTIL    │───▶│   PROCESS   │
│   UI Page   │    │   API       │    │             │    │   LIBRARY   │    │   STATUS    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │                   │
       │◀───────────────────│◀───────────────────│◀───────────────────│◀───────────────────│
       │                   │                   │                   │                   │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   UPDATE    │    │   JSON      │    │   PROCESS   │    │   SYSTEM    │    │   RUNNING   │
│   STATE     │    │  RESPONSE   │    │    INFO     │    │    METRICS  │    │   SCRIPTS   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

🎮 CONTROL FLOW (Start/Stop):
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  USER CLICK │───▶│  TOGGLE     │───▶│   POST      │───▶│   START/    │───▶│  PYTHON    │
│   SWITCH    │    │   HANDLER   │    │   REQUEST   │    │   STOP      │    │   SCRIPT    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │                   │
       │⏳                 │⏳                 │⏳                 │⏳                 │⏳
       │LOADING            │LOADING            │PROCESSING         │STARTING/         │EXECUTING
       │SPINNER            │STATE             │REQUEST            │STOPPING          │CODE
       │                   │                   │                   │                   │
       │◀───────────────────│◀───────────────────│◀───────────────────│◀───────────────────│
       │                   │                   │                   │                   │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   UPDATE    │    │   SUCCESS/  │    │   PROCESS   │    │   PROCESS   │    │   SCRIPT    │
│   UI STATE  │    │   ERROR     │    │   STATUS    │    │   MANAGED   │    │   RUNNING   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           ERROR HANDLING FLOW                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

❌ ERROR PROPAGATION:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PROCESS   │───▶│  RUNNER     │───▶│  FASTAPI    │───▶│  NEXT.JS   │───▶│   USER     │
│   ERROR     │    │  MANAGER    │    │   CATCH     │    │   CATCH     │    │   SEES     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │                   │
       │🔄                 │🔄                 │🔄                 │🔄                 │🔄
       │RECOVERY           │CLEANUP           │ERROR RESPONSE    │ERROR STATE       │ERROR MESSAGE
       │ATTEMPT            │DEAD PROCESSES    │500/400 ERROR     │UI INDICATOR      │DISPLAY
       │                   │                   │                   │                   │

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          TECHNOLOGY STACK                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🛠️ FRONTEND:
├─ ⚛️ React 18 + Next.js 14
├─ 🎨 Tailwind CSS + shadcn/ui
├─ 🔄 useState + useEffect Hooks
├─ 🌐 Fetch API for HTTP Requests
└─ 🎯 TypeScript (with some lint issues)

🔧 BACKEND:
├─ 🚀 FastAPI (Python Web Framework)
├─ 🌐 Uvicorn ASGI Server
├─ 📦 psutil (Process Management)
├─ 🔧 subprocess (Process Execution)
└─ 📝 Python Logging

🗄️ DATA MANAGEMENT:
├─ 🔄 In-Memory Process Tracking
├─ 📊 Real-time System Metrics
├─ 🕐 Timestamp-based Sync
└─ 📋 JSON API Responses

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           DEPLOYMENT ARCHITECTURE                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🏗️ DEVELOPMENT SETUP:
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TERMINAL 1: NEXT.JS DEVELOPMENT SERVER                                        │ TERMINAL 2: FASTAPI SERVER │
│                                                                              │                            │
│ $ cd dashboard                                                              │ $ cd api                    │
│ $ npm run dev                                                              │ $ python main.py            │
│                                                                              │                            │
│ 🌐 http://localhost:3000                                                    │ 🚀 http://localhost:8000    │
│ 📱 Orchestrator Page: /orchestrator                                         │ 📊 API Docs: /docs          │
│ 🔄 Hot Reload Enabled                                                       │ 🔄 Auto Reload Enabled      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🔗 COMMUNICATION:
├─ 🌐 HTTP/JSON REST API
├─ 🔗 CORS-enabled Cross-origin
├─ 📊 5-second Polling Interval
├─ ⚡ Real-time State Synchronization
└─ 🚨 Error Propagation Chain

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                            SECURITY CONSIDERATIONS                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐

🔒 SECURITY MEASURES:
├─ 🌐 CORS: localhost:3000 only (Development)
├─ 🚫 No Authentication (Development Mode)
├─ 📝 Process Isolation (subprocess)
├─ 🛡️ Safe Process Termination (psutil)
├─ 🔍 Input Validation (FastAPI)
└─ 📋 Error Message Sanitization

⚠️ PRODUCTION CONSIDERATIONS:
├─ 🔐 Add Authentication/Authorization
├─ 🌐 Configure CORS for Production Domains
├─ 🔍 Add Request Rate Limiting
├─ 🗄️ Add Persistent Process Storage
├─ 📊 Add Monitoring & Logging
└─ 🚀 Add Containerization (Docker)

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           FUTURE ENHANCEMENTS                                            │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

🚀 UPCOMING FEATURES:
├─ 🔄 WebSocket Integration (Real-time Updates)
├─ 📊 Advanced Process Monitoring
├─ 🗄️ Database-backed Process State
├─ 🔐 Multi-user Support
├─ 📱 Mobile Responsive Design
├─ 🌐 Production Deployment
├─ 📈 Performance Metrics Dashboard
└─ 🔔 Alert System Integration

📊 SYSTEM METRICS:
├─ 📈 6 Production Runners
├─ ⚡ 5-second Sync Interval
├─ 🎯 100% API Success Rate (Target)
├─ 🔄 <100ms Response Time (Target)
└─ 💾 <50MB Memory Usage (Target)

```

## 🎯 Summary

The HUNTER_AGENT_AI_MARKETING_DIGITAL system consists of **4 main layers**:

1. **Frontend (Next.js)** - User interface with real-time dashboard
2. **API Layer (FastAPI)** - RESTful API for process management
3. **Process Manager** - Handles Python script execution and monitoring
4. **Python Scripts** - Actual business logic runners

**Key Features:**
- 🔄 Real-time synchronization (5-second polling)
- 🎮 Interactive start/stop controls
- 📊 Live system metrics
- 🛡️ Safe process management
- 🚨 Comprehensive error handling
- 🎨 Professional dark mode UI

The system provides complete control over production Python scripts through a modern web interface, with robust error handling and real-time feedback.
