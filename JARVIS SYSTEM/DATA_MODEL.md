# JARVIS AI System Data Model

Model data lengkap untuk JARVIS AI System dengan schema, relationships, dan data structures.

## Overview

Dokumen ini mendefinisikan semua model data yang digunakan dalam JARVIS AI System, termasuk database schema, data structures, dan relationships.

## Database Schema

### SQLite Database

#### financial_ledger.db

**transactions** table
```sql
CREATE TABLE transactions (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  debit REAL DEFAULT 0,
  credit REAL DEFAULT 0,
  account TEXT NOT NULL,
  description TEXT,
  category TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_date ON transactions(date);
CREATE INDEX idx_transactions_account ON transactions(account);
CREATE INDEX idx_transactions_category ON transactions(category);
```

**accounts** table
```sql
CREATE TABLE accounts (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'asset', 'liability', 'equity', 'revenue', 'expense'
  balance REAL DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**bounties** table
```sql
CREATE TABLE bounties (
  id TEXT PRIMARY KEY,
  task_description TEXT NOT NULL,
  requirements TEXT,
  budget REAL NOT NULL,
  platform TEXT NOT NULL,
  platform_url TEXT,
  status TEXT DEFAULT 'open', -- 'open', 'in_progress', 'completed'
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**submissions** table
```sql
CREATE TABLE submissions (
  id TEXT PRIMARY KEY,
  bounty_id TEXT NOT NULL,
  worker_id TEXT,
  work_data TEXT, -- JSON
  review_score REAL,
  review_feedback TEXT,
  status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (bounty_id) REFERENCES bounties(id)
);
```

**payouts** table
```sql
CREATE TABLE payouts (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL, -- 'crypto', 'stripe'
  recipient TEXT NOT NULL,
  amount REAL NOT NULL,
  currency TEXT NOT NULL,
  tx_hash TEXT,
  stripe_payout_id TEXT,
  bounty_id TEXT,
  submission_id TEXT,
  status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'failed'
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**devices** table
```sql
CREATE TABLE devices (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- 'relay', 'sensor', 'actuator'
  protocol TEXT NOT NULL, -- 'mqtt', 'http'
  topic TEXT, -- for MQTT
  url TEXT, -- for HTTP
  status TEXT DEFAULT 'offline', -- 'online', 'offline'
  last_seen TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**users** table
```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  phone TEXT UNIQUE,
  role TEXT DEFAULT 'regular', -- 'creator', 'vip', 'regular'
  whatsapp_number TEXT,
  telegram_id TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**messages** table
```sql
CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  content TEXT NOT NULL,
  platform TEXT NOT NULL, -- 'whatsapp', 'telegram', 'web'
  direction TEXT NOT NULL, -- 'inbound', 'outbound'
  response TEXT,
  confidence REAL,
  provider TEXT, -- 'gemini', 'ollama'
  processing_time REAL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## JSON State Files

### directive_lock_state.json
```json
{
  "is_locked": false,
  "lock_id": null,
  "creator_id": null,
  "mission_description": null,
  "activated_at": null,
  "expires_at": null,
  "pending_approvals": []
}
```

### pending_approvals.json
```json
{
  "approvals": [
    {
      "id": "approval123",
      "action": "execute_command",
      "command": "/some_command",
      "reason": "gray_area_action",
      "requested_at": "2024-01-15T10:00:00Z",
      "status": "pending"
    }
  ]
}
```

### hydra_state.json
```json
{
  "node_id": "node123",
  "is_leader": true,
  "leader_id": "node123",
  "peers": {
    "node456": {
      "last_seen": "2024-01-15T10:00:00Z",
      "status": "connected"
    }
  },
  "last_election": null,
  "failover_count": 0
}
```

### last_creator_interaction.json
```json
{
  "timestamp": "2024-01-15T10:00:00Z",
  "source": "manual"
}
```

### sustenance_mode.json
```json
{
  "mode": "normal",
  "activated_at": null,
  "budget": 0.05,
  "objectives": [],
  "restrictions": []
}
```

## Data Structures

### TypeScript Interfaces

#### User
```typescript
interface User {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  role: 'creator' | 'vip' | 'regular';
  whatsapp_number?: string;
  telegram_id?: string;
  created_at: string;
  updated_at: string;
}
```

#### Message
```typescript
interface Message {
  id: string;
  user_id: string;
  content: string;
  platform: 'whatsapp' | 'telegram' | 'web';
  direction: 'inbound' | 'outbound';
  response?: string;
  confidence?: number;
  provider?: 'gemini' | 'ollama';
  processing_time?: number;
  created_at: string;
}
```

#### Transaction
```typescript
interface Transaction {
  id: string;
  date: string;
  debit: number;
  credit: number;
  account: string;
  description?: string;
  category?: string;
  created_at: string;
  updated_at: string;
}
```

#### Account
```typescript
interface Account {
  id: string;
  name: string;
  type: 'asset' | 'liability' | 'equity' | 'revenue' | 'expense';
  balance: number;
  created_at: string;
  updated_at: string;
}
```

#### Bounty
```typescript
interface Bounty {
  id: string;
  task_description: string;
  requirements?: string;
  budget: number;
  platform: string;
  platform_url?: string;
  status: 'open' | 'in_progress' | 'completed';
  created_at: string;
  updated_at: string;
  submissions?: Submission[];
}
```

#### Submission
```typescript
interface Submission {
  id: string;
  bounty_id: string;
  worker_id?: string;
  work_data?: any;
  review_score?: number;
  review_feedback?: string;
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
  updated_at: string;
}
```

#### Payout
```typescript
interface Payout {
  id: string;
  type: 'crypto' | 'stripe';
  recipient: string;
  amount: number;
  currency: string;
  tx_hash?: string;
  stripe_payout_id?: string;
  bounty_id?: string;
  submission_id?: string;
  status: 'pending' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}
```

#### Device
```typescript
interface Device {
  id: string;
  name: string;
  type: 'relay' | 'sensor' | 'actuator';
  protocol: 'mqtt' | 'http';
  topic?: string;
  url?: string;
  status: 'online' | 'offline';
  last_seen?: string;
  created_at: string;
  updated_at: string;
}
```

#### DirectiveLock
```typescript
interface DirectiveLock {
  is_locked: boolean;
  lock_id?: string;
  creator_id?: string;
  mission_description?: string;
  activated_at?: string;
  expires_at?: string;
  pending_approvals: PendingApproval[];
}
```

#### PendingApproval
```typescript
interface PendingApproval {
  id: string;
  action: string;
  command?: string;
  reason: string;
  requested_at: string;
  status: 'pending' | 'approved' | 'rejected';
}
```

#### HydraState
```typescript
interface HydraState {
  node_id: string;
  is_leader: boolean;
  leader_id: string;
  peers: Record<string, PeerInfo>;
  last_election?: string;
  failover_count: number;
}
```

#### PeerInfo
```typescript
interface PeerInfo {
  last_seen: string;
  status: 'connected' | 'disconnected';
}
```

## Vector Database Schema

### Knowledge Graph

#### Entities
```typescript
interface Entity {
  id: string;
  type: 'person' | 'organization' | 'concept' | 'event' | 'location';
  name: string;
  properties: Record<string, any>;
  embeddings: number[];
  created_at: string;
  updated_at: string;
}
```

#### Relationships
```typescript
interface Relationship {
  id: string;
  source_id: string;
  target_id: string;
  type: string;
  properties: Record<string, any>;
  created_at: string;
  updated_at: string;
}
```

## Data Relationships

### Entity Relationship Diagram

```
User (1) ----< (N) Message
User (1) ----< (N) Transaction (as creator)
Account (1) ----< (N) Transaction
Bounty (1) ----< (N) Submission
Submission (1) ----< (1) Payout
Device (N) ----< (1) IoT Bridge
Entity (N) ----< (N) Relationship ----> (N) Entity
```

### Relationships Details

**User → Message**
- One user can have many messages
- Messages are linked to users via user_id

**Account → Transaction**
- One account can have many transactions
- Transactions are linked to accounts via account field

**Bounty → Submission**
- One bounty can have many submissions
- Submissions are linked to bounties via bounty_id

**Submission → Payout**
- One submission can have one payout
- Payouts are linked to submissions via submission_id

**Entity → Relationship**
- Entities are connected via relationships
- Relationships have source and target entities

## Data Validation

### Validation Rules

**User**
- id: Required, unique
- name: Required, min 2 characters
- email: Optional, valid email format
- phone: Optional, valid phone format
- role: Required, one of: creator, vip, regular

**Transaction**
- id: Required, unique
- date: Required, valid date format
- debit: Required, >= 0
- credit: Required, >= 0
- account: Required, must exist in accounts table
- description: Optional
- category: Optional

**Bounty**
- id: Required, unique
- task_description: Required, min 10 characters
- budget: Required, > 0
- platform: Required, one of: upwork, freelancer
- status: Required, one of: open, in_progress, completed

**Device**
- id: Required, unique
- name: Required, min 2 characters
- type: Required, one of: relay, sensor, actuator
- protocol: Required, one of: mqtt, http
- status: Required, one of: online, offline

## Data Migration

### Migration Strategy

1. **Version Control**: All schema changes tracked in migrations
2. **Backward Compatibility**: Maintain backward compatibility when possible
3. **Rollback**: Always provide rollback script
4. **Testing**: Test migrations in staging first

### Migration Files

Migrations are stored in `data/migrations/` directory with naming convention:
- `YYYYMMDDHHMMSS_description.sql`

Example:
- `20240115100000_add_user_role.sql`
- `20240115110000_add_device_table.sql`

## Data Backup

### Backup Strategy

1. **Daily Backups**: Automated daily backups
2. **Weekly Full Backups**: Full system backup weekly
3. **Monthly Archives**: Monthly archives for long-term storage
4. **Off-site Storage**: Cloud storage for disaster recovery

### Backup Procedure

```bash
# Backup SQLite database
sqlite3 data/financial_ledger.db ".backup backups/$(date +%Y%m%d).db"

# Backup JSON state files
cp data/*.json backups/$(date +%Y%m%d)/

# Compress backup
tar -czf backups/$(date +%Y%m%d).tar.gz backups/$(date +%Y%m%d)/
```

## Data Privacy

### Sensitive Data

**Personally Identifiable Information (PII)**
- User email
- User phone
- WhatsApp number
- Telegram ID

**Financial Data**
- Transaction amounts
- Account balances
- Payout information

**Security Data**
- API keys (stored in .env, not database)
- Creator tokens (stored in .env, not database)

### Data Protection

1. **Encryption**: Encrypt sensitive data at rest
2. **Access Control**: Role-based access control
3. **Audit Logging**: Log all data access
4. **Data Retention**: Define retention policies
5. **Data Deletion**: Provide data deletion capability

## Data Retention

### Retention Policy

**Messages**: 90 days
**Transactions**: 7 years (legal requirement)
**Bounties**: 1 year
**Submissions**: 1 year
**Payouts**: 7 years (legal requirement)
**Logs**: 30 days
**Backups**: 30 days daily, 1 year weekly, 7 years monthly

## Data Performance

### Indexing Strategy

**Indexes Created**:
- transactions.date
- transactions.account
- transactions.category
- messages.user_id
- messages.created_at

**Query Optimization**:
- Use indexes for frequent queries
- Avoid full table scans
- Use query execution plans
- Optimize slow queries

### Caching Strategy

**Cache Layers**:
1. Application cache (in-memory)
2. Redis cache (distributed)
3. CDN cache (static assets)

**Cache TTL**:
- User data: 1 hour
- Transaction data: 5 minutes
- Status data: 30 seconds
- Static data: 1 day

## Data Consistency

### Transaction Management

**ACID Properties**:
- Atomicity: All or nothing
- Consistency: Data remains valid
- Isolation: Transactions don't interfere
- Durability: Committed data persists

**Transaction Isolation**:
- Read committed (default)
- Repeatable read (for financial transactions)
- Serializable (for critical operations)

### Data Integrity

**Constraints**:
- Primary keys
- Foreign keys
- Unique constraints
- Check constraints

**Triggers**:
- Update timestamps
- Maintain balances
- Audit logging

## Data Monitoring

### Metrics to Monitor

**Database Metrics**:
- Query performance
- Connection pool usage
- Lock contention
- Disk usage

**Data Quality Metrics**:
- Data completeness
- Data accuracy
- Data consistency
- Data freshness

**Security Metrics**:
- Access patterns
- Failed authentication attempts
- Data access violations
- Encryption status

## Data Recovery

### Recovery Procedures

**Point-in-Time Recovery**:
1. Stop all writes
2. Restore from backup
3. Apply transaction logs
4. Verify data integrity
5. Resume operations

**Disaster Recovery**:
1. Assess damage
2. Restore from off-site backup
3. Verify system functionality
4. Monitor for issues
5. Document incident

## Data Governance

### Governance Policies

**Data Ownership**:
- Creator owns all data
- Creator can request data deletion
- Creator can export data

**Data Access**:
- Role-based access control
- Audit trail for all access
- Regular access reviews

**Data Quality**:
- Regular data quality checks
- Data validation rules
- Data cleansing procedures

## Appendix

### Database Commands

```bash
# Create database
sqlite3 data/financial_ledger.db

# Run migration
sqlite3 data/financial_ledger.db < migrations/001_initial.sql

# Backup database
sqlite3 data/financial_ledger.db ".backup backup.db"

# Check integrity
sqlite3 data/financial_ledger.db "PRAGMA integrity_check;"

# Optimize database
sqlite3 data/financial_ledger.db "VACUUM;"

# Analyze query plan
sqlite3 data/financial_ledger.db "EXPLAIN QUERY PLAN SELECT * FROM transactions;"
```

### Data Export Formats

**CSV Export**:
```sql
.headers on
.mode csv
.output transactions.csv
SELECT * FROM transactions;
```

**JSON Export**:
```sql
.mode json
.output transactions.json
SELECT * FROM transactions;
```

**XML Export**:
```sql
.mode xml
.output transactions.xml
SELECT * FROM transactions;
```
