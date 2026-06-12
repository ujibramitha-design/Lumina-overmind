# 🔐 Google Sheets Credentials Setup Guide

## 📋 Overview

This guide explains how to set up Google Sheets service account credentials for the HUNTER_AGENT_AI_MARKETING_DIGITAL Dashboard Bridge module.

## 🎯 Prerequisites

1. **Google Account** with Google Cloud Console access
2. **Google Cloud Platform** project
3. **Google Sheets API** enabled
4. **Google Drive API** enabled

## 📝 Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click **"NEW PROJECT"** or select existing project
4. Enter project name: `hunter-ai-sheets-integration`
5. Click **"CREATE"**

### Step 2: Enable Required APIs

1. In your project, go to **APIs & Services** → **Library**
2. Search and enable these APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Step 3: Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"Service account"**
4. Fill in service account details:
   - **Service account name**: `hunter-ai-sheets-service`
   - **Service account ID**: `hunter-ai-sheets-service@your-project-id.iam.gserviceaccount.com`
   - **Description**: `Service account for HUNTER_AGENT_AI_MARKETING_DIGITAL Google Sheets integration`
5. Click **"CREATE AND CONTINUE"**
6. Skip adding roles for now (we'll add permissions manually)
7. Click **"DONE"**

### Step 4: Generate Service Account Key

1. Find your service account in the credentials list
2. Click on the service account name
3. Go to **"KEYS"** tab
4. Click **"ADD KEY"** → **"Create new key"**
5. Select **"JSON"** as key type
6. Click **"CREATE"**
7. **Important**: The JSON file will download automatically. Save it securely!

### Step 5: Set Up Google Sheets Access

1. Open your Google Sheets document
2. Click the **"Share"** button (top right)
3. Add the service account email:
   - Email: `hunter-ai-sheets-service@your-project-id.iam.gserviceaccount.com`
   - Role: **"Editor"**
4. Click **"Send"**

### Step 6: Configure Credentials File

1. **Copy the downloaded JSON file** to your project:
   ```bash
   # Copy your downloaded file
   cp /path/to/downloaded/credentials.json config/google_sheets_credentials.json
   ```

2. **Or create the file manually**:
   - Create new file: `config/google_sheets_credentials.json`
   - Copy the content from your downloaded JSON file
   - Paste it into the new file

3. **Set proper permissions**:
   ```bash
   chmod 600 config/google_sheets_credentials.json
   ```

### Step 7: Update Environment Variables

Add these variables to your `.env` file:

```env
# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS=config/google_sheets_credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
# Or use URL instead:
# GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/your_spreadsheet_id_here/edit
```

**To get Spreadsheet ID:**
1. Open your Google Sheets document
2. Look at the URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`
3. Copy the `[SPREADSHEET_ID]` part

## 🧪 Test the Setup

### Method 1: Run Test Script
```bash
python core_modules/dashboard_bridge/sheets_connector.py
```

### Method 2: Python Test
```python
from core_modules.dashboard_bridge.sheets_connector import GoogleSheetsConnector

# Test connection
connector = GoogleSheetsConnector()
status = connector.get_connection_status()
print(f"Connected: {status['connected']}")
```

### Expected Output:
```
2026-05-28 14:30:00 - sheets_connector - INFO - [SUCCESS] Kredensial Google Sheets ditemukan dan valid: config/google_sheets_credentials.json
2026-05-28 14:30:00 - sheets_connector - INFO - Google Sheets Connector initialized successfully
2026-05-28 14:30:01 - sheets_connector - INFO - Successfully connected to spreadsheet: Your Spreadsheet Name
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "[WARNING] Kredensial Google Sheets tidak ditemukan"
**Solution**: 
- Check file path in `.env` file
- Ensure credentials file exists at specified location
- Verify file permissions

#### 2. "[ERROR] File kredensial tidak valid (bukan format JSON)"
**Solution**:
- Ensure the file contains valid JSON
- Check for extra characters or formatting issues
- Re-download the credentials file

#### 3. "Spreadsheet not found"
**Solution**:
- Verify spreadsheet ID is correct
- Check if service account has Editor permissions
- Ensure Google Sheets API is enabled

#### 4. "Permission denied"
**Solution**:
- Share the spreadsheet with service account email
- Give Editor permissions (not just Viewer)
- Wait a few minutes for permissions to propagate

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger('core_modules.dashboard_bridge.sheets_connector').setLevel(logging.DEBUG)
```

## 📁 File Structure

After setup, your project should have:
```
config/
├── google_sheets_credentials.json          # Your actual credentials (DO NOT commit to Git)
├── google_sheets_credentials.json.example # Template file (safe to commit)
└── README_CREDENTIALS_SETUP.md           # This guide
```

## 🔒 Security Best Practices

### 1. Protect Your Credentials
```bash
# Set restrictive file permissions
chmod 600 config/google_sheets_credentials.json

# Add to .gitignore
echo "config/google_sheets_credentials.json" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Use Different Credentials for Different Environments
- **Development**: Use a separate service account
- **Production**: Use a different service account with limited permissions

### 3. Regular Key Rotation
- Rotate service account keys every 90 days
- Delete old keys immediately after creating new ones

### 4. Monitor API Usage
- Check Google Cloud Console for API quota usage
- Set up alerts for unusual activity

## 🎯 Next Steps

Once credentials are set up:

1. **Test the connection** using the test script
2. **Configure your spreadsheet** with proper column headers
3. **Test lead insertion** with sample data
4. **Set up database sync** if using SQLite integration
5. **Monitor logs** for any issues

## 📞 Support

If you encounter issues:

1. Check the logs: `logs/system_logs/sheets_connector.log`
2. Verify all steps in this guide
3. Test with a simple spreadsheet first
4. Check Google Cloud Console for API status

## 🔄 Alternative Setup (OAuth2)

If you prefer OAuth2 instead of service account:

1. Create OAuth2 credentials in Google Cloud Console
2. Set up consent screen
3. Use OAuth2 flow instead of service account
4. Update the connector class accordingly

*Note: Service account is recommended for server-to-server integration.*

---

**⚠️ Important**: Never commit your actual credentials file to version control. Always use the `.example` file for documentation and keep your actual credentials secure.
