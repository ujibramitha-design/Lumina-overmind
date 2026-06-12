# 🚀 Lumina Webhook Intake Engine - Documentation

## Overview
Advanced webhook system for receiving and processing lead data with AI-powered scoring, token-based authentication, and database integration.

## 🔐 Security & Authentication

### Token-Based Authentication
- **Token**: `DUMMY-TOKEN-123` (configurable)
- **Header**: `X-Lumina-Token`
- **Validation**: FastAPI dependency function
- **Status Codes**: 401 Unauthorized for invalid/missing tokens

### Security Features
- **Header Validation**: Mandatory X-Lumina-Token header
- **Token Comparison**: Exact string matching
- **Error Logging**: Invalid token attempts logged
- **Rate Limiting**: Recommended for production

## 🎯 API Endpoints

### 1. GET /api/webhook/health
Webhook health check endpoint

**Request:**
```http
GET /api/webhook/health
```

**Response:**
```json
{
  "status": "OK",
  "service": "Lumina Webhook Intake Engine",
  "timestamp": "2026-05-30T01:45:00.000Z",
  "version": "1.0.0"
}
```

**Features:**
- Service status check
- Version information
- Timestamp
- No authentication required

### 2. POST /api/webhook/incoming-lead
Process incoming lead webhook with AI scoring and database storage

**Request Headers:**
```http
Content-Type: application/json
X-Lumina-Token: DUMMY-TOKEN-123
```

**Request Body:**
```json
{
  "nama": "John Doe",
  "no_hp": "08123456789",
  "email": "john@example.com",
  "sumber": "website",
  "campaign": "summer_promo",
  "catatan": "Interested in property investment",
  "lokasi": "Jakarta",
  "pekerjaan": "Software Engineer"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Lead processed successfully",
  "data": {
    "lead_id": 123,
    "nama": "John Doe",
    "no_hp": "08123456789",
    "email": "john@example.com",
    "sumber": "website",
    "campaign": "summer_promo",
    "lokasi": "Jakarta",
    "pekerjaan": "Software Engineer",
    "score": 85,
    "status": "Hot",
    "keywords_found": ["jual", "investasi", "jakarta"],
    "processed_at": "2026-05-30T01:45:00.000Z"
  }
}
```

**Features:**
- Token validation via dependency
- Pydantic model validation
- AI-powered lead scoring
- Database storage
- Comprehensive response data

## 📊 Pydantic Models

### LeadWebhookPayload Model
```python
class LeadWebhookPayload(BaseModel):
    """Pydantic model for incoming lead webhook payload"""
    nama: str = Field(..., min_length=1, max_length=255, description="Lead name")
    no_hp: str = Field(..., min_length=10, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")
    sumber: str = Field(..., min_length=1, max_length=100, description="Lead source")
    campaign: Optional[str] = Field(None, max_length=100, description="Campaign name")
    catatan: Optional[str] = Field(None, max_length=1000, description="Additional notes")
    lokasi: Optional[str] = Field(None, max_length=255, description="Location")
    pekerjaan: Optional[str] = Field(None, max_length=100, description="Occupation")
```

### WebhookResponse Model
```python
class WebhookResponse(BaseModel):
    """Pydantic model for webhook response"""
    success: bool
    message: str
    data: Dict[str, Any]
```

## 🔧 Technical Implementation

### Dependency Function
```python
def verify_webhook_token(x_lumina_token: str = None):
    """
    Dependency function to validate X-Lumina-Token header
    """
    if x_lumina_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Lumina-Token header is missing"
        )
    
    if x_lumina_token != LUMINA_WEBHOOK_TOKEN:
        logger.warning(f"Invalid webhook token: {x_lumina_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Lumina-Token"
        )
    
    return x_lumina_token
```

### Lead Processing Pipeline
```python
@app.post("/api/webhook/incoming-lead", status_code=status.HTTP_201_CREATED)
async def incoming_lead_webhook(
    payload: LeadWebhookPayload,
    token: str = Depends(verify_webhook_token)
):
    try:
        # 1. Log incoming lead
        logger.info(f"Received webhook lead: {payload.nama} from {payload.sumber}")
        
        # 2. Initialize AI scorer
        from api.utils.predictive_scoring import LeadScorer
        scorer = LeadScorer()
        
        # 3. Create combined text for scoring
        combined_text = f"{payload.nama} {payload.catatan or ''} {payload.lokasi or ''} {payload.pekerjaan or ''}"
        
        # 4. Score the lead
        scoring_result = scorer.calculate_score(
            title=payload.nama,
            description=combined_text,
            source=payload.sumber
        )
        
        # 5. Prepare database data
        business_name = payload.nama
        contact = f"Phone: {payload.no_hp}"
        if payload.email:
            contact += f", Email: {payload.email}"
        if payload.pekerjaan:
            contact += f", Occupation: {payload.pekerjaan}"
        if payload.lokasi:
            contact += f", Location: {payload.lokasi}"
        if payload.catatan:
            contact += f", Notes: {payload.catatan}"
        
        # 6. Store in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(insert_query, (business_name, contact, url, keywords, ...))
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 7. Return response
        return WebhookResponse(
            success=True,
            message="Lead processed successfully",
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process lead: {str(e)}"
        )
```

## 📈 Lead Scoring Integration

### Scoring Process
1. **Text Combination**: Combine all relevant fields into scoring text
2. **AI Analysis**: Use LeadScorer for keyword-based evaluation
3. **Score Calculation**: 0-100 scale with Hot/Warm/Cold classification
4. **Keyword Detection**: Extract found keywords for analysis

### Scoring Data Flow
```python
# Input payload
payload = {
    "nama": "JUAL Rumah Murah Jakarta",
    "catatan": "Sangat tertarik dengan harga promo",
    "lokasi": "Jakarta Selatan"
}

# Scoring text
combined_text = "JUAL Rumah Murah Jakarta Sangat tertarik dengan harga promo Jakarta Selatan"

# Scoring result
scoring_result = {
    "score": 85,
    "status": "Hot",
    "keywords_found": ["jual", "murah", "jakarta", "promo", "tertarik"]
}
```

### Database Storage
```sql
INSERT INTO leads (
    business_name, contact, url, keywords, source, score, status, 
    location, date_found, created_at, updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
```

**Data Mapping:**
- **business_name**: payload.nama
- **contact**: Formatted contact string
- **url**: webhook_source_timestamp
- **keywords**: webhook,campaign,location
- **source**: payload.sumber
- **score**: AI score
- **status**: AI status
- **location**: payload.lokasi

## 🚨 Error Handling

### HTTP Status Codes
- **201 Created**: Lead processed successfully
- **401 Unauthorized**: Invalid or missing token
- **400/422**: Invalid payload validation
- **500 Internal Server Error**: Database or system errors

### Error Response Format
```json
{
  "detail": "Error message description",
  "timestamp": "2026-05-30T01:45:00.000Z"
}
```

### Error Scenarios
```python
# Missing token
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="X-Lumina-Token header is missing"
)

# Invalid token
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid X-Lumina-Token"
)

# Missing required field
# Pydantic automatically returns 422 Unprocessable Entity

# Database error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to save lead to database"
)
```

## 🧪 Testing

### Test Script Usage
```bash
# Run webhook tests
python test_webhook_api.py
```

### Test Coverage
- ✅ Webhook health check
- ✅ Token validation (missing, invalid, valid)
- ✅ Payload validation (valid, invalid)
- ✅ Lead scoring integration
- ✅ Database integration
- ✅ Response format validation
- ✅ Error handling

### Test Examples
```python
# Valid webhook call
headers = {"X-Lumina-Token": "DUMMY-TOKEN-123"}
payload = {
    "nama": "John Doe",
    "no_hp": "08123456789",
    "sumber": "website"
}

response = requests.post(
    "http://localhost:8000/api/webhook/incoming-lead",
    json=payload,
    headers=headers
)
```

## 🔌 Webhook Client Integration

### JavaScript/Node.js
```javascript
const webhookUrl = 'http://localhost:8000/api/webhook/incoming-lead';
const token = 'DUMMY-TOKEN-123';

const leadData = {
    nama: 'John Doe',
    no_hp: '08123456789',
    email: 'john@example.com',
    sumber: 'website',
    campaign: 'summer_promo',
    catatan: 'Interested in property',
    lokasi: 'Jakarta',
    pekerjaan: 'Software Engineer'
};

async function submitLead(lead) {
    try {
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Lumina-Token': token
            },
            body: JSON.stringify(lead)
        });
        
        const result = await response.json();
        
        if (response.status === 201) {
            console.log('Lead processed successfully:', result);
            return result.data;
        } else {
            throw new Error(`HTTP ${response.status}: ${result.detail}`);
        }
    } catch (error) {
        console.error('Webhook error:', error);
        throw error;
    }
}

// Usage
submitLead(leadData);
```

### Python
```python
import requests
import json

def submit_webhook_lead(lead_data):
    url = 'http://localhost:8000/api/webhook/incoming-lead'
    token = 'DUMMY-TOKEN-123'
    
    headers = {
        'Content-Type': 'application/json',
        'X-Lumina-Token': token
    }
    
    try:
        response = requests.post(url, json=lead_data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            print(f"Lead processed: {result['data']['lead_id']}")
            return result
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

### cURL
```bash
curl -X POST http://localhost:8000/api/webhook/incoming-lead \
  -H "Content-Type: application/json" \
  -H "X-Lumina-Token: DUMMY-TOKEN-123" \
  -d '{
    "nama": "John Doe",
    "no_hp": "08123456789",
    "email": "john@example.com",
    "sumber": "website",
    "campaign": "summer_promo",
    "catatan": "Interested in property",
    "lokasi": "Jakarta",
    "pekerjaan": "Software Engineer"
  }'
```

## 📱 Frontend Integration

### React Component Example
```jsx
import React, { useState } from 'react';

function WebhookLeadForm() {
  const [formData, setFormData] = useState({
    nama: '',
    no_hp: '',
    email: '',
    sumber: '',
    campaign: '',
    catatan: '',
    lokasi: '',
    pekerjaan: ''
  });
  
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/webhook/incoming-lead', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Lumina-Token': 'DUMMY-TOKEN-123'
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.status === 201) {
        setResult(data.data);
        // Reset form
        setFormData({
          nama: '',
          no_hp: '',
          email: '',
          sumber: '',
          campaign: '',
          catatan: '',
          lokasi: '',
          pekerjaan: ''
        });
      } else {
        setError(data.detail || 'Failed to submit lead');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-zinc-950 rounded-lg border border-zinc-800">
      <h2 className="text-2xl font-bold text-zinc-100 mb-6">
        Submit Lead
      </h2>
      
      {result && (
        <div className="mb-6 p-4 bg-emerald-900/20 border border-emerald-500/30 rounded-lg">
          <h3 className="text-emerald-400 font-semibold mb-2">
            Lead Processed Successfully!
          </h3>
          <div className="text-zinc-300 text-sm">
            <p><strong>ID:</strong> {result.lead_id}</p>
            <p><strong>Score:</strong> {result.score}</p>
            <p><strong>Status:</strong> {result.status}</p>
            <p><strong>Keywords:</strong> {result.keywords_found.join(', ')}</p>
          </div>
        </div>
      )}

      {error && (
        <div className="mb-6 p-4 bg-red-900/20 border border-red-500/30 rounded-lg">
          <h3 className="text-red-400 font-semibold mb-2">
            Error
          </h3>
          <div className="text-zinc-300 text-sm">{error}</div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Name *
          </label>
          <input
            type="text"
            name="nama"
            value={formData.nama}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Enter lead name"
          />
        </div>

        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Phone Number *
          </label>
          <input
            type="tel"
            name="no_hp"
            value={formData.no_hp}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Enter phone number"
          />
        </div>

        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Email
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Enter email address"
          />
        </div>

        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Source *
          </label>
          <input
            type="text"
            name="sumber"
            value={formData.sumber}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Enter lead source"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-zinc-300 text-sm font-medium mb-2">
              Campaign
            </label>
            <input
              type="text"
              name="campaign"
              value={formData.campaign}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
              placeholder="Campaign name"
            />
          </div>

          <div>
            <label className="block text-zinc-300 text-sm font-medium mb-2">
              Location
            </label>
            <input
              type="text"
              name="lokasi"
              value={formData.lokasi}
              onChange={handleChange}
              className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
              placeholder="Location"
            />
          </div>
        </div>

        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Occupation
          </label>
          <input
            type="text"
            name="pekerjaan"
            value={formData.pekerjaan}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Occupation"
          />
        </div>

        <div>
          <label className="block text-zinc-300 text-sm font-medium mb-2">
            Notes
          </label>
          <textarea
            name="catatan"
            value={formData.catatan}
            onChange={handleChange}
            rows={3}
            className="w-full px-3 py-2 bg-zinc-800 border border-zinc-700 rounded-lg text-zinc-100 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            placeholder="Additional notes"
          />
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-emerald-500 hover:bg-emerald-600 text-black font-semibold py-3 px-4 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? 'Submitting...' : 'Submit Lead'}
        </button>
      </form>
    </div>
  );
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Webhook Token (optional, defaults to DUMMY-TOKEN-123)
LUMINA_WEBHOOK_TOKEN=your-secure-token-here

# API Configuration
API_HOST=localhost
API_PORT=8000
```

### Token Management
```python
# In production, use environment variables
import os
LUMINA_WEBHOOK_TOKEN = os.getenv('LUMINA_WEBHOOK_TOKEN', 'DUMMY-TOKEN-123')
```

### Custom Token Validation
```python
def verify_webhook_token(x_lumina_token: str = None):
    # Add custom validation logic
    if not x_lumina_token:
        raise HTTPException(status_code=401, detail="Token required")
    
    # Add token expiration check
    if is_token_expired(x_lumina_token):
        raise HTTPException(status_code=401, detail="Token expired")
    
    return x_lumina_token
```

## 📊 Monitoring & Logging

### Logging Configuration
```python
logger.info(f"Received webhook lead: {payload.nama} from {payload.sumber}")
logger.warning(f"Invalid webhook token: {x_lumina_token}")
logger.error(f"Database error in webhook: {e}")
logger.info(f"Successfully processed lead {lead_id}: {payload.nama}")
```

### Metrics to Track
- Request count per source
- Lead scoring distribution
- Processing time
- Error rates
- Token validation failures

## 🔮 Production Deployment

### Security Considerations
- Use HTTPS in production
- Implement rate limiting
- Use environment variables for tokens
- Add request logging
- Set up monitoring alerts

### Performance Optimization
- Database connection pooling
- Async processing for heavy operations
- Caching for frequent requests
- Load balancer configuration

### Scaling Considerations
- Horizontal scaling with multiple instances
- Database sharding for high volume
- Message queue for async processing
- CDN for static assets

## 🚀 Quick Start

### 1. Start API Server
```bash
python api/main.py
```

### 2. Test Webhook
```bash
python test_webhook_api.py
```

### 3. Submit Test Lead
```bash
curl -X POST http://localhost:8000/api/webhook/incoming-lead \
  -H "Content-Type: application/json" \
  -H "X-Lumina-Token: DUMMY-TOKEN-123" \
  -d '{"nama": "Test User", "no_hp": "08123456789", "sumber": "test"}'
```

### 4. Check Results
```bash
# Query database
sqlite3 data/leads.db "SELECT * FROM leads WHERE source = 'test' ORDER BY created_at DESC LIMIT 5;"
```

## 📁 File Structure
```
dashboard/
├── api/
│   └── main.py                    # FastAPI endpoints
├── api/utils/
│   └── predictive_scoring.py     # Lead scoring utility
├── data/
│   └── leads.db                  # SQLite database
├── test_webhook_api.py              # Test script
└── WEBHOOK_DOCUMENTATION.md          # This documentation
```

## 🔧 Troubleshooting

### Common Issues

#### Connection Timeout
```bash
# Check if API server is running
curl http://localhost:8000/api/webhook/health

# Start server if needed
python api/main.py
```

#### Token Authentication Error
```bash
# Check token in headers
curl -H "X-Lumina-Token: DUMMY-TOKEN-123" http://localhost:8000/api/webhook/health

# Verify token constant
grep -n "LUMINA_WEBHOOK_TOKEN" api/main.py
```

#### Database Errors
```bash
# Check database file
ls -la data/leads.db

# Check database schema
sqlite3 data/leads.db ".schema leads"

# Test database connection
python -c "import sqlite3; conn = sqlite3.connect('data/leads.db'); print('Database connected')"
```

#### Pydantic Validation Errors
```bash
# Test with valid payload
python -c "
import requests
payload = {'nama': 'Test', 'no_hp': '08123456789', 'sumber': 'test'}
headers = {'X-Lumina-Token': 'DUMMY-TOKEN-123'}
response = requests.post('http://localhost:8000/api/webhook/incoming-lead', json=payload, headers=headers)
print(f'Status: {response.status_code}')
print(f'Response: {response.text}')
"
```

---

## 🎯 Key Features Summary

### Security Features
- **Token-Based Authentication**: Secure API access
- **Header Validation**: Mandatory X-Lumina-Token
- **Pydantic Models**: Input validation and sanitization
- **Error Handling**: Comprehensive error responses

### Processing Pipeline
- **AI Scoring**: LeadScorer integration
- **Database Storage**: SQLite with proper schema
- **Response Format**: Structured JSON responses
- **Logging**: Comprehensive error tracking

### Integration Ready
- **Multiple Clients**: JavaScript, Python, cURL examples
- **Frontend Components**: React integration example
- **API Documentation**: Complete endpoint reference
- **Test Suite**: Comprehensive validation

---

*Last updated: May 30, 2026*
