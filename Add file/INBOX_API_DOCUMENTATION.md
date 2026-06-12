# 📱 Omni-Channel Inbox API - Documentation

## Overview
RESTful API endpoints for managing Omni-Channel Inbox functionality with SQLite database integration and JSON parsing for follow-up notes.

## 🎯 API Endpoints

### 1. GET /api/inbox/pending
Retrieve all leads with status 'Follow Up' and non-null catatan_followup

**Request:**
```http
GET /api/inbox/pending
```

**Response:**
```json
{
  "success": true,
  "data": {
    "leads": [
      {
        "id": 1,
        "business_name": "Test Lead 1 - Follow Up with Notes",
        "contact": "Interested in property investment",
        "url": "https://example.com/1",
        "keywords": "investasi,properti",
        "source": "web",
        "score": 85.0,
        "status": "Follow Up",
        "location": "Jakarta",
        "date_found": "2026-05-30T01:30:00",
        "created_at": "2026-05-30T01:30:00",
        "updated_at": "2026-05-30T01:30:00",
        "catatan_followup": {
          "message": "Lead is interested in investment properties, follow up required",
          "metadata": {
            "priority": "high",
            "contact_method": "phone",
            "last_contact": "2026-05-29"
          },
          "raw_json": "{\"message\": \"Lead is interested...\", \"metadata\": {...}}"
        }
      }
    ],
    "total": 1
  },
  "timestamp": "2026-05-30T01:30:00.000Z"
}
```

**Features:**
- Queries leads with `status = 'Follow Up'` and `catatan_followup IS NOT NULL`
- Parses JSON in `catatan_followup` column
- Extracts `message` and `metadata` from Gemini responses
- Handles JSON parsing errors gracefully
- Returns raw JSON for debugging

### 2. POST /api/inbox/approve/{lead_id}
Update lead status to 'Contacted'

**Request:**
```http
POST /api/inbox/approve/123
```

**Response:**
```json
{
  "success": true,
  "data": {
    "lead_id": 123,
    "old_status": "Follow Up",
    "new_status": "Contacted",
    "updated_at": "2026-05-30T01:30:00.000Z"
  },
  "message": "Lead 123 approved and marked as contacted",
  "timestamp": "2026-05-30T01:30:00.000Z"
}
```

**Features:**
- Validates lead_id parameter
- Checks if lead exists
- Updates status to 'Contacted'
- Updates timestamp
- Returns before/after status

### 3. GET /api/inbox/stats
Get inbox statistics and lead counts

**Request:**
```http
GET /api/inbox/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_leads": 100,
    "pending_leads": 25,
    "status_breakdown": {
      "Follow Up": 30,
      "Contacted": 40,
      "New": 20,
      "Qualified": 8,
      "Closed": 2
    },
    "pending_breakdown": {
      "follow_up_with_notes": 25,
      "follow_up_total": 30,
      "new_leads": 20,
      "contacted_leads": 40,
      "qualified_leads": 8,
      "closed_leads": 2
    }
  },
  "timestamp": "2026-05-30T01:30:00.000Z"
}
```

**Features:**
- Total lead count
- Pending leads count (with notes)
- Status breakdown
- Detailed pending breakdown

## 🔧 Technical Implementation

### Database Schema
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    contact TEXT,
    url TEXT,
    keywords TEXT,
    source TEXT DEFAULT 'web_scraping',
    score REAL DEFAULT 0.0,
    status TEXT DEFAULT 'new',
    location TEXT,
    date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    catatan_followup TEXT  -- JSON from Gemini AI
);
```

### Database Helper Function
```python
def get_db_connection():
    """Get database connection with proper error handling"""
    db_path = os.path.join('data', 'leads.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
```

### JSON Parsing Logic
```python
# Parse catatan_followup JSON safely
try:
    if row["catatan_followup"]:
        followup_data = json.loads(row["catatan_followup"])
        
        # Extract message and metadata from Gemini response
        parsed_followup = {
            "message": followup_data.get("message", ""),
            "metadata": followup_data.get("metadata", {}),
            "raw_json": row["catatan_followup"]
        }
        lead_data["catatan_followup"] = parsed_followup
        
except json.JSONDecodeError as e:
    logger.warning(f"Failed to parse catatan_followup for lead {row['id']}: {e}")
    # Keep raw data if parsing fails
    lead_data["catatan_followup"] = {
        "message": row["catatan_followup"],
        "metadata": {},
        "raw_json": row["catatan_followup"],
        "parse_error": str(e)
    }
```

## 🚨 Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (lead doesn't exist)
- **500**: Internal Server Error (database issues)

### Error Response Format
```json
{
  "detail": "Error message description",
  "timestamp": "2026-05-30T01:30:00.000Z"
}
```

### Common Error Scenarios

#### Invalid Lead ID
```http
POST /api/inbox/approve/invalid
```
**Response:** 404 Not Found

#### Lead Not Found
```http
POST /api/inbox/approve/99999
```
**Response:** 404 Not Found

#### Database Connection Error
**Response:** 500 Internal Server Error

#### JSON Parsing Error
**Response:** 200 Success (with parse_error field)

## 📊 Database Queries

### Pending Leads Query
```sql
SELECT id, business_name, contact, url, keywords, source, score, status, 
       location, date_found, created_at, updated_at, catatan_followup
FROM leads 
WHERE status = 'Follow Up' AND catatan_followup IS NOT NULL AND catatan_followup != ''
ORDER BY date_found DESC
```

### Status Update Query
```sql
UPDATE leads 
SET status = 'Contacted', updated_at = ?
WHERE id = ?
```

### Statistics Queries
```sql
-- Status breakdown
SELECT status, COUNT(*) as count 
FROM leads 
GROUP BY status
ORDER BY count DESC

-- Pending leads count
SELECT COUNT(*) as count
FROM leads 
WHERE status = 'Follow Up' AND catatan_followup IS NOT NULL AND catatan_followup != ''

-- Total leads
SELECT COUNT(*) as count FROM leads
```

## 🔍 Usage Examples

### Frontend Integration
```javascript
// Get pending leads
async function getPendingLeads() {
  try {
    const response = await fetch('/api/inbox/pending');
    const data = await response.json();
    
    if (data.success) {
      return data.data.leads;
    } else {
      throw new Error(data.detail);
    }
  } catch (error) {
    console.error('Failed to get pending leads:', error);
    return [];
  }
}

// Approve lead
async function approveLead(leadId) {
  try {
    const response = await fetch(`/api/inbox/approve/${leadId}`, {
      method: 'POST'
    });
    const data = await response.json();
    
    if (data.success) {
      return data.data;
    } else {
      throw new Error(data.detail);
    }
  } catch (error) {
    console.error('Failed to approve lead:', error);
    throw error;
  }
}

// Get inbox stats
async function getInboxStats() {
  try {
    const response = await fetch('/api/inbox/stats');
    const data = await response.json();
    
    if (data.success) {
      return data.data;
    } else {
      throw new Error(data.detail);
    }
  } catch (error) {
    console.error('Failed to get inbox stats:', error);
    return null;
  }
}
```

### React Component Example
```jsx
import { useState, useEffect } from 'react';

function InboxPendingLeads() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const data = await getPendingLeads();
        setLeads(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLeads();
  }, []);

  const handleApprove = async (leadId) => {
    try {
      await approveLead(leadId);
      // Refresh leads list
      const data = await getPendingLeads();
      setLeads(data);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Pending Leads ({leads.length})</h2>
      {leads.map(lead => (
        <div key={lead.id}>
          <h3>{lead.business_name}</h3>
          <p>Score: {lead.score}</p>
          <p>Location: {lead.location}</p>
          <p>Follow-up: {lead.catatan_followup?.message}</p>
          <button onClick={() => handleApprove(lead.id)}>
            Approve
          </button>
        </div>
      ))}
    </div>
  );
}
```

## 🧪 Testing

### Test Script Usage
```bash
# Update database schema
python update_database_schema.py

# Run API tests
python test_inbox_api.py
```

### Test Coverage
- ✅ Database setup and schema validation
- ✅ API health check
- ✅ GET /api/inbox/pending endpoint
- ✅ POST /api/inbox/approve/{id} endpoint
- ✅ Error handling for invalid requests
- ✅ JSON parsing for catatan_followup
- ✅ Database integrity checks
- ✅ Statistics endpoint

### Test Data
The test script creates sample leads with various scenarios:
- Valid JSON in catatan_followup
- Invalid JSON (parsing error handling)
- Null catatan_followup (excluded from pending)
- Different statuses (Follow Up, Contacted, New)

## 📱 Frontend Integration

### API Client Setup
```javascript
// api/inbox.js
const API_BASE_URL = 'http://localhost:8000/api/inbox';

export const inboxAPI = {
  getPending: () => fetch(`${API_BASE_URL}/pending`).then(r => r.json()),
  approve: (id) => fetch(`${API_BASE_URL}/approve/${id}`, { method: 'POST' }).then(r => r.json()),
  getStats: () => fetch(`${API_BASE_URL}/stats`).then(r => r.json())
};
```

### State Management
```javascript
// stores/inbox.js
import { defineStore } from 'pinia';
import { inboxAPI } from '@/api/inbox';

export const useInboxStore = defineStore('inbox', {
  state: () => ({
    pendingLeads: [],
    stats: null,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchPendingLeads() {
      this.loading = true;
      try {
        const response = await inboxAPI.getPending();
        this.pendingLeads = response.data.leads;
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    
    async approveLead(leadId) {
      try {
        await inboxAPI.approve(leadId);
        // Refresh pending leads
        await this.fetchPendingLeads();
        await this.fetchStats();
      } catch (error) {
        this.error = error.message;
        throw error;
      }
    },
    
    async fetchStats() {
      try {
        const response = await inboxAPI.getStats();
        this.stats = response.data;
      } catch (error) {
        this.error = error.message;
      }
    }
  }
});
```

## 🔧 Configuration

### Environment Variables
```bash
# Database path (optional, defaults to data/leads.db)
DATABASE_PATH=./data/leads.db

# API settings
API_HOST=localhost
API_PORT=8000
```

### Database Setup
```python
# Ensure database directory exists
os.makedirs('data', exist_ok=True)

# Run schema update
python update_database_schema.py
```

## 🚀 Quick Start

### 1. Setup Database
```bash
python update_database_schema.py
```

### 2. Start API Server
```bash
python api/main.py
```

### 3. Test Endpoints
```bash
python test_inbox_api.py
```

### 4. Frontend Integration
```javascript
import { inboxAPI } from '@/api/inbox';

// Get pending leads
const leads = await inboxAPI.getPending();

// Approve a lead
await inboxAPI.approve(123);

// Get statistics
const stats = await inboxAPI.getStats();
```

## 📁 File Structure
```
dashboard/
├── api/
│   └── main.py                    # FastAPI endpoints
├── data/
│   └── leads.db                  # SQLite database
├── test_inbox_api.py              # Test script
├── update_database_schema.py      # Schema update script
└── INBOX_API_DOCUMENTATION.md      # This documentation
```

## 🔮 Future Enhancements

### Additional Endpoints
- `GET /api/inbox/lead/{id}` - Get single lead details
- `PUT /api/inbox/lead/{id}` - Update lead information
- `DELETE /api/inbox/lead/{id}` - Delete lead
- `POST /api/inbox/bulk-approve` - Approve multiple leads

### Advanced Features
- Pagination for pending leads
- Search and filtering
- Real-time updates via WebSocket
- Lead assignment to agents
- Follow-up scheduling

### Performance Optimizations
- Database indexing
- Query optimization
- Caching layer
- Connection pooling

---

## 🎯 Key Features Summary

### Database Integration
- **SQLite Database**: Local storage with proper schema
- **JSON Parsing**: Safe parsing of Gemini AI responses
- **Error Handling**: Graceful error handling for invalid data
- **Data Integrity**: Proper validation and constraints

### API Features
- **RESTful Design**: Standard HTTP methods and status codes
- **JSON Responses**: Consistent response format
- **Error Handling**: Comprehensive error responses
- **Validation**: Input validation and sanitization

### Business Logic
- **Lead Status Management**: Follow Up → Contacted workflow
- **Follow-up Notes**: Parsed AI-generated notes
- **Statistics**: Real-time lead counts and breakdowns
- **Data Filtering**: Status-based lead filtering

---

*Last updated: May 30, 2026*
