# 📚 HUNTER AGENT AI MARKETING DIGITAL - API Documentation

## 🔗 Lead Detail API Route

### Overview
Dynamic API route for retrieving detailed lead information with AI reasoning and timeline data.

### Endpoint
```
GET /api/leads/[id]
```

### Parameters
- `id` (path parameter): Lead ID (integer)

### Request Example
```bash
# Fetch lead with ID 1
curl http://localhost:3000/api/leads/1

# Fetch lead with ID 5
curl http://localhost:3000/api/leads/5
```

### Response Format

#### Success Response (200 OK)
```json
{
  "success": true,
  "data": {
    "id": 1,
    "business_name": "PT. Maju Bersama Properti",
    "contact": "Budi Santoso",
    "phone": "+62812345678",
    "email": "budi@majubersama.co.id",
    "url": "https://majubersama-properti.com",
    "keywords": "investasi properti, rumah mewah, apartemen premium",
    "source": "website_inquiry",
    "score": 9.2,
    "location": "Jakarta Selatan",
    "city": "Jakarta",
    "status": "hot_lead",
    "priority": "high",
    "property_type": "apartment",
    "price_range": "2M-5M",
    "bedrooms": 3,
    "bathrooms": 2,
    "description": "Looking for premium investment properties in South Jakarta area",
    "date_found": "2024-05-23T10:30:00.000Z",
    "created_at": "2024-05-23T10:30:00.000Z",
    "updated_at": "2024-05-23T10:30:00.000Z",
    
    // AI Reasoning (Radar Chart Data)
    "ai_reasoning": {
      "intent": 90,
      "budget": 85,
      "urgency": 75,
      "fit": 95,
      "authority": 80
    },
    
    // Timeline Activities
    "timeline": [
      {
        "id": "1",
        "activity": "Lead Discovered",
        "timestamp": "2024-05-16T10:30:00.000Z",
        "type": "discovery",
        "details": "Found PT. Maju Bersama Properti through website_inquiry"
      },
      {
        "id": "2",
        "activity": "AI Validation Passed",
        "timestamp": "2024-05-18T10:30:00.000Z",
        "type": "validation",
        "details": "Lead scored 9.2/10 with high confidence"
      },
      {
        "id": "3",
        "activity": "Contact Information Extracted",
        "timestamp": "2024-05-20T10:30:00.000Z",
        "type": "extraction",
        "details": "Extracted phone: +62812345678, email: budi@majubersama.co.id"
      },
      {
        "id": "4",
        "activity": "Market Analysis Completed",
        "timestamp": "2024-05-22T10:30:00.000Z",
        "type": "analysis",
        "details": "High-value lead identified in Jakarta Selatan market"
      }
    ]
  }
}
```

#### Error Responses

**400 Bad Request** (Invalid ID)
```json
{
  "success": false,
  "message": "Invalid lead ID parameter"
}
```

**404 Not Found** (Lead doesn't exist)
```json
{
  "success": false,
  "message": "Lead with ID 999 not found"
}
```

**500 Internal Server Error** (Database issues)
```json
{
  "success": false,
  "message": "Database connection failed. Please try again later."
}
```

### Data Fields

#### Lead Information
| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique lead identifier |
| `business_name` | string | Company/business name |
| `contact` | string | Contact person name |
| `phone` | string | Phone number |
| `email` | string | Email address |
| `url` | string | Website URL |
| `keywords` | string | Search keywords |
| `source` | string | Lead source |
| `score` | float | Lead quality score (0-10) |
| `location` | string | Geographic location |
| `city` | string | City name |
| `status` | string | Lead status (new, qualified, hot_lead, etc.) |
| `priority` | string | Priority level (low, medium, high) |
| `property_type` | string | Property type (house, apartment, commercial, etc.) |
| `price_range` | string | Price range |
| `bedrooms` | integer | Number of bedrooms |
| `bathrooms` | integer | Number of bathrooms |
| `land_size` | float | Land size in m² |
| `building_size` | float | Building size in m² |
| `year_built` | integer | Year built |
| `description` | string | Lead description |
| `date_found` | datetime | When lead was discovered |
| `created_at` | datetime | Record creation timestamp |
| `updated_at` | datetime | Last update timestamp |

#### AI Reasoning (Radar Chart)
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `intent` | integer | 0-100 | Purchase intent strength |
| `budget` | integer | 0-100 | Budget alignment |
| `urgency` | integer | 0-100 | Purchase urgency |
| `fit` | integer | 0-100 | Product fit score |
| `authority` | integer | 0-100 | Decision-making authority |

#### Timeline Activities
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Activity identifier |
| `activity` | string | Activity description |
| `timestamp` | datetime | When activity occurred |
| `type` | string | Activity type (discovery, validation, extraction, analysis, contact) |
| `details` | string | Additional activity details |

### Usage Examples

#### JavaScript/TypeScript
```typescript
// Fetch lead details
async function fetchLeadDetails(leadId: number) {
  try {
    const response = await fetch(`/api/leads/${leadId}`);
    const data = await response.json();
    
    if (data.success) {
      console.log('Lead:', data.data.business_name);
      console.log('AI Reasoning:', data.data.ai_reasoning);
      console.log('Timeline:', data.data.timeline);
    } else {
      console.error('Error:', data.message);
    }
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

// Usage
fetchLeadDetails(1);
```

#### React Hook Example
```typescript
import { useState, useEffect } from 'react';

interface LeadDetail {
  id: number;
  business_name: string;
  contact: string;
  ai_reasoning: {
    intent: number;
    budget: number;
    urgency: number;
    fit: number;
    authority: number;
  };
  timeline: Array<{
    activity: string;
    timestamp: string;
    type: string;
    details?: string;
  }>;
}

export function useLeadDetail(leadId: number) {
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchLead() {
      try {
        const response = await fetch(`/api/leads/${leadId}`);
        const data = await response.json();

        if (data.success) {
          setLead(data.data);
        } else {
          setError(data.message);
        }
      } catch (err) {
        setError('Failed to fetch lead details');
      } finally {
        setLoading(false);
      }
    }

    if (leadId) {
      fetchLead();
    }
  }, [leadId]);

  return { lead, loading, error };
}
```

### Testing

#### Using the Test Script
```bash
# Make sure the development server is running
npm run dev

# Run the test script
node test_lead_api.js
```

#### Manual Testing
```bash
# Test valid lead
curl http://localhost:3000/api/leads/1

# Test invalid lead ID
curl http://localhost:3000/api/leads/999999

# Test invalid ID format
curl http://localhost:3000/api/leads/invalid
```

### Database Schema

The API connects to the `leads.db` SQLite database with the following table structure:

```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    contact TEXT,
    phone TEXT,
    email TEXT,
    url TEXT,
    keywords TEXT,
    source TEXT DEFAULT 'web_scraping',
    score REAL DEFAULT 0.0,
    location TEXT,
    city TEXT,
    status TEXT DEFAULT 'new',
    priority TEXT DEFAULT 'medium',
    property_type TEXT,
    price_range TEXT,
    bedrooms INTEGER,
    bathrooms INTEGER,
    land_size REAL,
    building_size REAL,
    year_built INTEGER,
    description TEXT,
    date_found DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_contacted DATETIME,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Performance Considerations

- **Database Connection**: Each API call opens and closes a database connection
- **Caching**: Response headers include `Cache-Control: no-store` for real-time data
- **Error Handling**: Comprehensive error handling for database and validation issues
- **Type Safety**: Full TypeScript implementation with interfaces

### Security Notes

- **Input Validation**: Lead ID parameter is validated for numeric format
- **SQL Injection**: Uses parameterized queries to prevent SQL injection
- **Error Messages**: Generic error messages to prevent information disclosure

### Future Enhancements

- **PUT Method**: Update lead information
- **DELETE Method**: Remove leads
- **Pagination**: For list endpoints
- **Filtering**: By status, location, score range
- **Authentication**: API key or JWT-based auth
- **Rate Limiting**: Prevent abuse

---

## 🚀 Quick Start

1. **Setup Database**:
   ```bash
   python data/database_forge.py
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Test API**:
   ```bash
   node test_lead_api.js
   ```

4. **Access in Browser**:
   ```
   http://localhost:3000/api/leads/1
   ```

---

*Last updated: May 30, 2026*
