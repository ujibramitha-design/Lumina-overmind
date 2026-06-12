# Fase 3: The Automation & Outreach - Jalur A (The Intake Engine)

## 📋 Overview

Fase 3 memperkenalkan sistem automation dan outreach untuk Lumina OS, dimulai dengan **Jalur A: The Intake Engine** yang menggunakan webhook untuk menerima data lead dari platform pihak ketiga.

## 🎯 Fitur yang Diimplementasikan

### 1. Webhook Endpoint (`lumina_os/api/endpoints/webhook.py`)

**Security Features:**
- ✅ Token-based authentication menggunakan header `X-Lumina-Token: DUMMY-TOKEN-123`
- ✅ Payload validation untuk memastikan data完整性
- ✅ Comprehensive error handling dan logging

**Core Functionality:**
- ✅ `POST /api/webhook/incoming-lead` - Menerima data lead dari platform eksternal
- ✅ Integrasi dengan `PredictiveScoringEngine` untuk automatic lead scoring
- ✅ Penyimpanan data ke SQLite database menggunakan `DatabaseManager`
- ✅ Response HTTP 201 Created untuk sukses processing

**Additional Endpoints:**
- ✅ `GET /api/webhook/health` - Health check untuk webhook system
- ✅ `POST /api/webhook/test` - Test endpoint dengan sample data

### 2. API Registration (`lumina_os/api/__init__.py`)

- ✅ Import dan registrasi `webhook_bp` blueprint
- ✅ CORS headers untuk cross-origin requests
- ✅ Proper error handlers

### 3. Simulation Script (`scripts/simulate_incoming_leads.py`)

**Test Cases:**
1. **Lead 1 - Facebook Ads (Hot)**: Data lengkap, PNS, lokasi jelas, siap DP
2. **Lead 2 - TikTok Ads (Warm)**: Data standar, ada email dan catatan, budget spesifik  
3. **Lead 3 - Organic Web (Cold)**: Data minim, hanya nama dan telepon

**Features:**
- ✅ Colored terminal output untuk better visibility
- ✅ Progress tracking dan error reporting
- ✅ Success rate calculation
- ✅ Expected vs actual category comparison

## 🚀 Quick Start

### 1. Start Lumina OS API Server

```bash
cd lumina_os/api
python run_server.py
```

Server akan berjalan di `http://localhost:5000`

### 2. Run Webhook Simulation

```bash
cd scripts
python simulate_incoming_leads.py
```

## 📊 Expected Results

### Lead 1 - Facebook Ads (Expected: Hot)
```json
{
  "nama": "Budi Santoso, S.T.",
  "no_hp": "08123456789", 
  "email": "budi.santoso@engineering.co.id",
  "sumber": "Facebook Ads",
  "campaign": "Summer Property Promo 2024",
  "catatan": "Saya tertarik dengan tipe 36/72, sudah siap DP 30%. Pekerjaan sebagai PNS di Kementerian PU, penghasilan stabil. Lokasi di Serang dekat kantor.",
  "lokasi": "Serang",
  "pekerjaan": "PNS"
}
```

**Expected Scoring:**
- Phone: +20 points ✅
- Job (PNS): +30 points ✅  
- Location (Serang): +20 points ✅
- Email: +10 points ✅
- Complete data: +15 points ✅
- Property intent: +25 points ✅
- **Total: ~120/100 (capped at 100) → HOT**

### Lead 2 - TikTok Ads (Expected: Warm)
```json
{
  "nama": "Sarah Putri",
  "no_hp": "08234567890",
  "email": "sarah.putri@gmail.com", 
  "sumber": "TikTok Ads",
  "campaign": "Gen Z Property Hunt",
  "catatan": "Cari rumah untuk keluarga muda, budget 300-400 juta. Lokasi preferensi Serang atau sekitarnya.",
  "lokasi": "Serang",
  "pekerjaan": "Wirausaha"
}
```

**Expected Scoring:**
- Phone: +20 points ✅
- Job (Wirausaha): +15 points
- Location (Serang): +20 points ✅
- Email: +10 points ✅
- Complete data: +15 points ✅
- Property intent: +25 points ✅
- **Total: ~105/100 (capped at 100) → WARM**

### Lead 3 - Organic Web (Expected: Cold)
```json
{
  "nama": "Rudi",
  "no_hp": "08345678901",
  "email": "",
  "sumber": "Organic Web",
  "campaign": "",
  "catatan": "",
  "lokasi": "",
  "pekerjaan": ""
}
```

**Expected Scoring:**
- Phone: +20 points ✅
- Job: 0 points
- Location: 0 points  
- Email: 0 points
- Complete data: 0 points
- Property intent: 0 points
- **Total: ~20/100 → COLD**

## 🔧 API Endpoints

### Webhook Incoming Lead
```
POST /api/webhook/incoming-lead
Headers:
  Content-Type: application/json
  X-Lumina-Token: DUMMY-TOKEN-123

Body:
{
  "nama": "John Doe",
  "no_hp": "08123456789", 
  "email": "john@example.com",
  "sumber": "Facebook Ads",
  "campaign": "Summer Promo 2024",
  "catatan": "Interested in 2BR unit"
}
```

### Webhook Health Check
```
GET /api/webhook/health
```

### Webhook Test
```
POST /api/webhook/test
Headers:
  X-Lumina-Token: DUMMY-TOKEN-123
```

## 📝 Response Format

### Success Response (201 Created)
```json
{
  "success": true,
  "message": "Lead processed successfully",
  "data": {
    "lead_id": 123,
    "nama": "John Doe", 
    "skor_akhir": 85.5,
    "kategori": "Hot",
    "waktu_proses": "2024-05-28T14:30:00"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Invalid or missing security token"
}
```

## 🔒 Security

### Token Authentication
- **Default Token**: `DUMMY-TOKEN-123`
- **Environment Variable**: `LUMINA_WEBHOOK_TOKEN`
- **Header**: `X-Lumina-Token`

### Payload Validation
- **Required Fields**: `nama`, `no_hp`
- **Phone Validation**: Minimum 10 characters
- **Type Checking**: String validation for all fields

## 📊 Integration Testing

### Manual Testing with curl
```bash
# Test webhook health
curl -H "X-Lumina-Token: DUMMY-TOKEN-123" \
     http://localhost:5000/api/webhook/health

# Test incoming lead
curl -X POST \
     -H "Content-Type: application/json" \
     -H "X-Lumina-Token: DUMMY-TOKEN-123" \
     -d '{"nama":"Test User","no_hp":"08123456789","email":"test@example.com","sumber":"Manual Test"}' \
     http://localhost:5000/api/webhook/incoming-lead
```

### Python Testing
```python
import requests

headers = {
    'Content-Type': 'application/json',
    'X-Lumina-Token': 'DUMMY-TOKEN-123'
}

data = {
    'nama': 'Test User',
    'no_hp': '08123456789',
    'email': 'test@example.com',
    'sumber': 'Python Test'
}

response = requests.post(
    'http://localhost:5000/api/webhook/incoming-lead',
    json=data,
    headers=headers
)

print(response.json())
```

## 🎯 Next Steps

### Fase 3 Continuation:
1. **Jalur B**: Email Automation System
2. **Jalur C**: SMS/WhatsApp Automation  
3. **Jalur D**: Social Media Integration

### Enhancement Opportunities:
- Real-time lead validation
- Advanced lead deduplication
- Multi-platform webhook support
- Lead scoring customization

## 📁 File Structure

```
lumina_os/
├── api/
│   ├── endpoints/
│   │   ├── webhook.py          # Webhook endpoint implementation
│   │   └── leads.py            # Existing leads API
│   ├── __init__.py             # API initialization with webhook registration
│   └── run_server.py          # Server runner script
scripts/
└── simulate_incoming_leads.py  # Webhook simulation script
```

## 🚀 System Status

- ✅ **Webhook Endpoint**: Fully functional with security
- ✅ **Predictive Scoring**: Integrated and working
- ✅ **Database Integration**: Lead storage operational
- ✅ **Simulation Script**: Ready for testing
- ✅ **API Registration**: Properly configured

**Lumina OS Intake Engine siap untuk production testing!** 🎉
