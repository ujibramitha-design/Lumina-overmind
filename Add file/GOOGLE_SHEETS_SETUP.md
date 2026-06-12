# 📊 Google Sheets Integration Setup Guide

## 🎯 Overview

This guide explains how to set up Google Sheets integration for the HUNTER_AGENT_AI_MARKETING_DIGITAL Dashboard Bridge module.

## 🔧 Prerequisites

1. **Google Account** with Google Sheets access
2. **Google Cloud Platform** project
3. **Service Account** with Google Sheets API access
4. **Python 3.8+** with required dependencies

## 📋 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Step 2: Create Service Account

1. In Google Cloud Console, go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Fill in service account details:
   - **Name**: `hunter-ai-sheets-connector`
   - **Description**: `Service account for HUNTER_AGENT_AI_MARKETING_DIGITAL Sheets integration`
4. Click **Create and Continue**
5. Skip roles for now (we'll set permissions manually)
6. Click **Done**

### Step 3: Generate Service Account Key

1. Find your service account in the list
2. Click on the service account name
3. Go to **Keys** tab
4. Click **Add Key** → **Create new key**
5. Select **JSON** as key type
6. Click **Create** - this will download a JSON file
7. **Save this file securely** - you'll need it for the next step

### Step 4: Set Up Google Sheets

1. Create a new Google Sheet or use existing one
2. Share the sheet with your service account:
   - Click **Share** button
   - Add the service account email (from JSON file)
   - Give **Editor** permissions
3. Copy the **Spreadsheet ID** from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
   - Copy the `[SPREADSHEET_ID]` part

### Step 5: Configure Environment Variables

1. Copy the service account JSON file to your project:
   ```bash
   mkdir -p config
   cp /path/to/your-service-account-key.json config/google_sheets_credentials.json
   ```

2. Add environment variables to `.env` file:
   ```env
   # Google Sheets Configuration
   GOOGLE_SHEETS_CREDENTIALS=config/google_sheets_credentials.json
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
   ```

   Or use URL instead of ID:
   ```env
   GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/your_spreadsheet_id_here
   ```

### Step 6: Install Dependencies

```bash
pip install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 7: Test the Connection

```python
# Test the Google Sheets connector
python core_modules/dashboard_bridge/sheets_connector.py
```

## 🚀 Usage Examples

### Basic Usage

```python
from core_modules.dashboard_bridge.sheets_connector import GoogleSheetsConnector

# Initialize connector
connector = GoogleSheetsConnector()

# Insert a new lead
lead_data = {
    'nama': 'John Doe',
    'no_hp': '0812-3456-7890',
    'skor_ai': 8.5,
    'status': 'New',
    'sumber': 'Website',
    'lokasi': 'Serang',
    'catatan': 'Interested in property near industrial area'
}

success = connector.push_new_lead(lead_data)
if success:
    print("Lead inserted successfully!")
```

### Sync from SQLite

```python
# Sync all leads from database
success = connector.sync_all_from_sqlite('data/leads.db')
if success:
    print("Database sync completed!")
```

### Get Connection Status

```python
status = connector.get_connection_status()
print(f"Connected: {status['connected']}")
print(f"Spreadsheet: {status['spreadsheet_title']}")
print(f"Worksheets: {status['worksheet_count']}")
```

## 📊 Worksheet Structure

### Leads Worksheet

| Column | Description | Example |
|--------|-------------|---------|
| Timestamp | When lead was added | 2026-05-28 14:30:00 |
| Nama | Lead name | John Doe |
| No HP | Phone number | 0812-3456-7890 |
| Skor AI | AI score (0-10) | 8.5 |
| Status | Lead status | New, Qualified, Closed |
| Sumber | Lead source | Website, Instagram, Manual |
| Lokasi | Location | Serang |
| Catatan | Additional notes | Interested in property |

### All Leads Worksheet

| Column | Description |
|--------|-------------|
| ID | Lead ID |
| URL | Source URL |
| Title | Lead title |
| Content | Content snippet |
| Score | AI score |
| Source | Source platform |
| Timestamp | Creation time |
| Status | Current status |
| Contact Info | Contact details |
| Urgency | Urgency score |
| Value | Potential value |
| Quality | Data quality score |
| Location | Geographic location |
| Type | Lead type |
| Query Used | Search query |

## 🔒 Security Best Practices

### 1. Protect Your Credentials

```bash
# Set proper file permissions
chmod 600 config/google_sheets_credentials.json
chmod 600 .env

# Add to .gitignore
echo "config/google_sheets_credentials.json" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Use Service Account Principle

- **Least Privilege**: Only give necessary permissions
- **Domain-Wide Delegation**: Not recommended for production
- **Regular Rotation**: Rotate keys periodically

### 3. Monitor API Usage

- Check Google Cloud Console for API quota
- Monitor logs for rate limiting
- Set up alerts for unusual activity

## ⚠️ Troubleshooting

### Common Issues

#### 1. "Credentials file not found"
```bash
# Check file path
ls -la config/google_sheets_credentials.json

# Verify environment variable
echo $GOOGLE_SHEETS_CREDENTIALS
```

#### 2. "Spreadsheet not found"
- Verify spreadsheet ID is correct
- Check service account has access
- Ensure sharing permissions are set to "Editor"

#### 3. "API quota exceeded"
- Implement rate limiting (built into connector)
- Wait for quota to reset (daily limit)
- Consider upgrading to paid plan

#### 4. "Permission denied"
- Check service account permissions in Google Cloud
- Verify Google Sheets API is enabled
- Ensure service account is shared on the sheet

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger('core_modules.dashboard_bridge.sheets_connector').setLevel(logging.DEBUG)
```

## 📈 Advanced Features

### Rate Limiting

The connector implements automatic rate limiting:

```python
# Configurable delay between API calls
connector.rate_limit_delay = 1.0  # seconds
```

### Batch Processing

Large datasets are processed in batches:

```python
# Automatic batch processing
batch_size = 100  # records per batch
```

### Error Handling

Comprehensive error handling with retry logic:

```python
# Automatic retry with exponential backoff
max_retry_attempts = 3
```

## 🔗 Integration Examples

### Integration with Main System

```python
# In main.py or orchestrator
from core_modules.dashboard_bridge.sheets_connector import GoogleSheetsConnector

class DashboardManager:
    def __init__(self):
        self.sheets_connector = GoogleSheetsConnector()
    
    def sync_leads_to_dashboard(self, leads):
        """Sync leads to Google Sheets dashboard"""
        for lead in leads:
            self.sheets_connector.push_new_lead({
                'nama': lead.get('name'),
                'no_hp': lead.get('phone'),
                'skor_ai': lead.get('score'),
                'status': lead.get('status'),
                'sumber': lead.get('source'),
                'lokasi': lead.get('location'),
                'catatan': lead.get('notes')
            })
```

### Webhook Integration

```python
# In API endpoint
@app.post('/webhook/lead')
def handle_new_lead():
    lead_data = request.json
    
    # Insert to Google Sheets
    connector = GoogleSheetsConnector()
    success = connector.push_new_lead(lead_data)
    
    return {'success': success}
```

## 📚 Additional Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [gspread Library Documentation](https://gspread.readthedocs.io/)
- [Google Cloud Authentication](https://cloud.google.com/docs/authentication)

## 🆘 Support

If you encounter issues:

1. Check the logs: `logs/system_logs/sheets_connector.log`
2. Verify configuration in `.env`
3. Test with the provided test script
4. Check Google Cloud Console for API status

For additional support, create an issue in the project repository.
