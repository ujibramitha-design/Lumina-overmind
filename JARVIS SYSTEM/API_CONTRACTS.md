# JARVIS AI System API Contracts

Kontrak API lengkap untuk JARVIS AI System dengan endpoint, request/response formats, dan data models.

## Overview

Dokumen ini mendefinisikan semua API contracts untuk JARVIS AI System, termasuk REST API dan WebSocket API.

## Base URL

### Development
- JARVIS API: `http://localhost:3001/api`
- Lumina API: `http://localhost:8000/api`

### Production
- JARVIS API: `https://jarvis.devproflow.com/api`
- Lumina API: `https://lumina.devproflow.com/api`

## Authentication

### JWT Authentication
```http
Authorization: Bearer <jwt_token>
```

### Creator Authentication
```http
X-Creator-ID: <creator_id>
X-Creator-Token: <creator_token>
```

## REST API Endpoints

### Health Endpoints

#### GET /health
Check system health status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "services": {
    "jarvis": "healthy",
    "lumina": "healthy",
    "database": "healthy",
    "ai": "healthy"
  }
}
```

#### GET /api/status
Get detailed system status.

**Response**:
```json
{
  "status": "operational",
  "uptime": 86400,
  "version": "6.0.0",
  "provider": {
    "current": "gemini",
    "status": "healthy",
    "last_failover": null
  },
  "peers": {
    "connected": 2,
    "total": 3
  }
}
```

---

### AI Endpoints

#### POST /api/chat
Send chat message to JARVIS.

**Request**:
```json
{
  "message": "Hello JARVIS",
  "platform": "whatsapp",
  "user_id": "user123",
  "context": {
    "previous_messages": [],
    "user_profile": {}
  }
}
```

**Response**:
```json
{
  "response": "Hello! How can I help you today?",
  "confidence": 0.95,
  "provider": "gemini",
  "timestamp": "2024-01-15T10:00:00Z",
  "processing_time": 1.5
}
```

#### POST /api/chat/stream
Stream chat response.

**Request**:
```json
{
  "message": "Tell me about JARVIS",
  "platform": "telegram",
  "user_id": "user123"
}
```

**Response**: Server-Sent Events (SSE) stream

---

### Security Endpoints

#### POST /api/security/override
Activate God Mode (Creator only).

**Request**:
```json
{
  "creator_id": "creator123",
  "verification_token": "token123",
  "command": "override"
}
```

**Response**:
```json
{
  "success": true,
  "message": "God Mode activated",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### POST /api/security/terminate
Execute Terminate Protocol (Creator only).

**Request**:
```json
{
  "creator_id": "creator123",
  "verification_token": "token123",
  "command": "terminate"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Terminate Protocol executed",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### POST /api/security/lock-mission
Activate Directive Lock.

**Request**:
```json
{
  "creator_id": "creator123",
  "verification_token": "token123",
  "mission_description": "Complete project X",
  "duration": 7
}
```

**Response**:
```json
{
  "success": true,
  "message": "Directive Lock activated",
  "lock_id": "lock123",
  "expires_at": "2024-01-22T10:00:00Z"
}
```

#### POST /api/security/unlock-mission
Deactivate Directive Lock.

**Request**:
```json
{
  "creator_id": "creator123",
  "verification_token": "token123",
  "lock_id": "lock123"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Directive Lock deactivated"
}
```

---

### Business Endpoints

#### GET /api/business/radar
Get business radar scan results.

**Response**:
```json
{
  "opportunities": [
    {
      "id": "opp123",
      "title": "New project opportunity",
      "score": 0.85,
      "source": "freelancer",
      "url": "https://example.com"
    }
  ],
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### GET /api/business/fiscal-calendar
Get fiscal calendar events.

**Response**:
```json
{
  "events": [
    {
      "id": "event123",
      "title": "Q1 Earnings",
      "date": "2024-03-31",
      "importance": "high"
    }
  ],
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

### Financial Endpoints

#### GET /api/finance/ledger
Get financial ledger entries.

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 50)
- `from_date`: Start date (ISO format)
- `to_date`: End date (ISO format)

**Response**:
```json
{
  "entries": [
    {
      "id": "entry123",
      "date": "2024-01-15",
      "debit": 1000.00,
      "credit": 0.00,
      "account": "cash",
      "description": "Payment received"
    }
  ],
  "total": 100,
  "page": 1,
  "pages": 2
}
```

#### GET /api/finance/balance-sheet
Get balance sheet.

**Response**:
```json
{
  "assets": {
    "current": 50000.00,
    "fixed": 100000.00,
    "total": 150000.00
  },
  "liabilities": {
    "current": 30000.00,
    "long_term": 50000.00,
    "total": 80000.00
  },
  "equity": 70000.00,
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### GET /api/finance/profit-loss
Get profit and loss statement.

**Response**:
```json
{
  "revenue": 100000.00,
  "expenses": 60000.00,
  "profit": 40000.00,
  "margin": 0.40,
  "period": "2024-01",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

### Corporation Endpoints

#### POST /api/corporation/bounty
Post new bounty.

**Request**:
```json
{
  "task_description": "Design a modern dashboard",
  "requirements": "React, Tailwind CSS, responsive",
  "budget": 500,
  "platform": "upwork"
}
```

**Response**:
```json
{
  "success": true,
  "bounty_id": "bounty123",
  "platform_url": "https://upwork.com/jobs/bounty123",
  "status": "open"
}
```

#### POST /api/corporation/review
Review submitted work.

**Request**:
```json
{
  "bounty_id": "bounty123",
  "submission_id": "sub123",
  "work_data": {
    "files": ["file1", "file2"],
    "description": "Work description"
  }
}
```

**Response**:
```json
{
  "success": true,
  "review": {
    "score": 85,
    "issues": [],
    "recommendation": "approve",
    "feedback": "Good work"
  }
}
```

#### POST /api/corporation/payout
Execute payout.

**Request**:
```json
{
  "type": "crypto",
  "recipient": "0x1234567890abcdef",
  "amount": 0.1,
  "bounty_id": "bounty123",
  "submission_id": "sub123"
}
```

**Response**:
```json
{
  "success": true,
  "payout_id": "payout123",
  "tx_hash": "0xabcdef123456",
  "status": "completed"
}
```

---

### Hardware Endpoints

#### POST /api/hardware/device-control
Control IoT device.

**Request**:
```json
{
  "device_id": "device123",
  "command": "on",
  "protocol": "mqtt"
}
```

**Response**:
```json
{
  "success": true,
  "device_id": "device123",
  "status": "on",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### POST /api/hardware/reboot
Execute physical hard reboot.

**Request**:
```json
{
  "relay_device_id": "relay123",
  "delay": 5000
}
```

**Response**:
```json
{
  "success": true,
  "message": "Physical Hard Reboot completed",
  "device_id": "relay123",
  "delay": 5000,
  "completed_at": "2024-01-15T10:00:05Z"
}
```

---

### Hydra Endpoints

#### GET /api/hydra/status
Get Hydra protocol status.

**Response**:
```json
{
  "node_id": "node123",
  "is_leader": true,
  "leader_id": "node123",
  "peers": [
    {
      "id": "node456",
      "status": "connected",
      "last_seen": "2024-01-15T10:00:00Z"
    }
  ],
  "heartbeat_interval": 5000
}
```

#### POST /api/hydra/elect-leader
Trigger leader election.

**Request**:
```json
{
  "force": true
}
```

**Response**:
```json
{
  "success": true,
  "message": "Leader election triggered",
  "election_id": "election123"
}
```

---

### Legacy Endpoints

#### GET /api/legacy/status
Get Dead Man's Switch status.

**Response**:
```json
{
  "last_interaction": "2024-01-15T10:00:00Z",
  "last_interaction_source": "manual",
  "delta_days": 0,
  "critical_threshold": 30,
  "is_critical": false,
  "emergency_mode": false
}
```

#### POST /api/legacy/record-interaction
Record Creator interaction.

**Request**:
```json
{
  "source": "manual"
}
```

**Response**:
```json
{
  "success": true,
  "timestamp": "2024-01-15T10:00:00Z",
  "source": "manual"
}
```

#### POST /api/legacy/execute-will
Execute legacy will (emergency only).

**Request**:
```json
{
  "emergency": true,
  "reason": "Emergency execution"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Legacy will executed",
  "executed_at": "2024-01-15T10:00:00Z"
}
```

---

## WebSocket API

### Connection

**URL**: `ws://localhost:3001/ws`

**Authentication**: Send token in first message

```json
{
  "type": "auth",
  "token": "jwt_token"
}
```

### Events

#### chat
Send chat message via WebSocket.

**Client → Server**:
```json
{
  "type": "chat",
  "message": "Hello JARVIS",
  "platform": "whatsapp",
  "user_id": "user123"
}
```

**Server → Client**:
```json
{
  "type": "chat_response",
  "response": "Hello! How can I help?",
  "confidence": 0.95,
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### status
Subscribe to status updates.

**Client → Server**:
```json
{
  "type": "subscribe",
  "channel": "status"
}
```

**Server → Client**:
```json
{
  "type": "status_update",
  "status": "operational",
  "provider": "gemini",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### ui
Subscribe to UI updates (Generative UI).

**Client → Server**:
```json
{
  "type": "subscribe",
  "channel": "ui"
}
```

**Server → Client**:
```json
{
  "type": "ui_component",
  "component": {
    "id": "comp123",
    "code": "React.createElement(...)",
    "type": "react",
    "props": {}
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### heartbeat
Heartbeat for connection health.

**Client → Server**:
```json
{
  "type": "ping"
}
```

**Server → Client**:
```json
{
  "type": "pong",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {}
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| AUTH_INVALID | Invalid authentication | 401 |
| AUTH_EXPIRED | Authentication expired | 401 |
| AUTH_INSUFFICIENT | Insufficient permissions | 403 |
| NOT_FOUND | Resource not found | 404 |
| VALIDATION_ERROR | Request validation failed | 400 |
| RATE_LIMIT_EXCEEDED | Rate limit exceeded | 429 |
| INTERNAL_ERROR | Internal server error | 500 |
| SERVICE_UNAVAILABLE | Service temporarily unavailable | 503 |
| AI_TIMEOUT | AI service timeout | 504 |
| AI_ERROR | AI service error | 500 |

---

## Rate Limiting

### Default Limits
- 100 requests per minute per IP
- 1000 requests per hour per user
- 10000 requests per day per user

### Priority Users
- Creator: No limits
- VIP users: 10x limits
- Regular users: Standard limits

---

## Data Models

### User
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'creator' | 'vip' | 'regular';
  created_at: string;
  updated_at: string;
}
```

### Message
```typescript
interface Message {
  id: string;
  user_id: string;
  content: string;
  platform: 'whatsapp' | 'telegram' | 'web';
  timestamp: string;
  response?: string;
  confidence?: number;
}
```

### Transaction
```typescript
interface Transaction {
  id: string;
  date: string;
  debit: number;
  credit: number;
  account: string;
  description: string;
  created_at: string;
}
```

### Bounty
```typescript
interface Bounty {
  id: string;
  task_description: string;
  requirements: string;
  budget: number;
  platform: string;
  status: 'open' | 'in_progress' | 'completed';
  created_at: string;
  submissions: Submission[];
}
```

### Device
```typescript
interface Device {
  id: string;
  name: string;
  type: 'relay' | 'sensor' | 'actuator';
  protocol: 'mqtt' | 'http';
  status: 'online' | 'offline';
  last_seen: string;
}
```

---

## Versioning

API versioning is done via URL path:
- v1: `/api/v1/*` (current)
- v2: `/api/v2/*` (future)

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Core endpoints implemented
- WebSocket support added
- Authentication implemented

### v1.1.0 (2024-01-20)
- Added Corporation endpoints
- Added Hardware endpoints
- Added Hydra endpoints
- Added Legacy endpoints
