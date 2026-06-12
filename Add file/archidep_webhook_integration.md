# 🤖 Archidep M2M Webhook Integration Guide

## Overview

This document explains how to integrate the Archidep system with Lumina OS using the Machine-to-Machine (M2M) webhook endpoint for automated siteplan file transfers.

## 🔐 Authentication

The webhook uses a secret key for authentication. Configure this in your environment:

```bash
# In .env file
ARCHIDEP_SECRET_KEY=Lumina-Archidep-Secret-X99
```

## 🚪 Webhook Endpoint

### Primary Endpoint
- **URL:** `POST /api/webhooks/archidep/receive-siteplan`
- **Authentication:** `X-API-KEY` header required
- **Content-Type:** `multipart/form-data` or `application/json`

### Status Update Endpoint
- **URL:** `POST /api/webhooks/archidep/status-update`
- **Authentication:** `X-API-KEY` header required
- **Content-Type:** `application/json`

## 📋 Integration Methods

### Method 1: File Upload (Multipart)

**Request:**
```bash
curl -X POST http://your-domain.com/api/webhooks/archidep/receive-siteplan \
  -H "X-API-KEY: Lumina-Archidep-Secret-X99" \
  -F "project_name=Luxury Villa Project" \
  -F "file=@/path/to/siteplan.obj" \
  -F "file_type=3D_MODEL" \
  -F 'metadata={"archidep_version": "2.1.0", "render_quality": "ultra"}'
```

**Response:**
```json
{
  "success": true,
  "message": "Siteplan uploaded successfully via webhook",
  "siteplan_id": "cuid123...",
  "status": "READY_FOR_VFX"
}
```

### Method 2: JSON with File URL

**Request:**
```bash
curl -X POST http://yourdomain.com/api/webhooks/archidep/receive-siteplan \
  -H "X-API-KEY: Lumina-Archidep-Secret-X99" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Luxury Villa Project",
    "file_url": "https://archidep.example.com/siteplans/luxury-villa.obj",
    "file_type": "3D_MODEL",
    "file_size": 15728640,
    "metadata": {
      "archidep_version": "2.1.0",
      "render_quality": "ultra",
      "dimensions": {"width": 1920, "height": 1080}
    },
    "project_id": "project-uuid-123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Siteplan received successfully via webhook URL",
  "siteplan_id": "cuid123...",
  "status": "READY_FOR_VFX"
}
```

## 📊 Status Updates

Archidep can receive status updates about VFX processing:

**Request:**
```bash
curl -X POST http://yourdomain.com/api/webhooks/archidep/status-update \
  -H "X-API-KEY: Lumina-Archidep-Secret-X99" \
  -H "Content-Type: application/json" \
  -d '{
    "siteplan_id": "cuid123...",
    "status": "RENDERING"
  }'
```

**Valid Statuses:**
- `READY_FOR_VFX` - Initial state
- `RENDERING` - VFX processing in progress
- `PUBLISHED` - Processing completed
- `FAILED` - Processing failed

## 🧪 Testing

### Test Webhook Configuration

Get webhook information:
```bash
curl http://yourdomain.com/api/webhooks/archidep/webhook-info
```

### Test Webhook Endpoint

Test file upload simulation:
```bash
curl -X POST http://yourdomain.com/api/webhooks/test-webhook \
  -F "project_name=Test Project" \
  -F "test_mode=json"
```

## 🔧 Implementation Examples

### Python Implementation

```python
import requests
import json

def send_siteplan_to_lumina(project_name, file_path, metadata=None):
    """Send siteplan file to Lumina OS via webhook"""
    
    url = "http://yourdomain.com/api/webhooks/archidep/receive-siteplan"
    headers = {
        "X-API-KEY": "Lumina-Archidep-Secret-X99"
    }
    
    # Prepare form data
    files = {
        'file': open(file_path, 'rb')
    }
    
    data = {
        'project_name': project_name,
        'file_type': '3D_MODEL',
        'metadata': json.dumps(metadata) if metadata else None
    }
    
    # Send request
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success! Siteplan ID: {result['siteplan_id']}")
        return result['siteplan_id']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Usage
siteplan_id = send_siteplan_to_lumina(
    project_name="Luxury Villa Project",
    file_path="/path/to/siteplan.obj",
    metadata={
        "archidep_version": "2.1.0",
        "render_quality": "ultra"
    }
)
```

### Node.js Implementation

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function sendSiteplanToLumina(projectName, filePath, metadata = null) {
    const url = 'http://yourdomain.com/api/webhooks/archidep/receive-siteplan';
    const headers = {
        'X-API-KEY': 'Lumina-Archidep-Secret-X99'
    };
    
    const form = new FormData();
    form.append('project_name', projectName);
    form.append('file', fs.createReadStream(filePath));
    form.append('file_type', '3D_MODEL');
    
    if (metadata) {
        form.append('metadata', JSON.stringify(metadata));
    }
    
    try {
        const response = await axios.post(url, form, { headers });
        console.log('Success! Siteplan ID:', response.data.siteplan_id);
        return response.data.siteplan_id;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        return null;
    }
}

// Usage
sendSiteplanToLumina(
    'Luxury Villa Project',
    '/path/to/siteplan.obj',
    {
        archidep_version: '2.1.0',
        render_quality: 'ultra'
    }
);
```

### PHP Implementation

```php
<?php

function sendSiteplanToLumina($projectName, $filePath, $metadata = null) {
    $url = 'http://yourdomain.com/api/webhooks/archidep/receive-siteplan';
    
    $ch = curl_init();
    
    // Create form data
    $postFields = [
        'project_name' => $projectName,
        'file' => new CURLFile($filePath),
        'file_type' => '3D_MODEL'
    ];
    
    if ($metadata) {
        $postFields['metadata'] = json_encode($metadata);
    }
    
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $postFields,
        CURLOPT_HTTPHEADER => [
            'X-API-KEY: Lumina-Archidep-Secret-X99'
        ]
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        $result = json_decode($response, true);
        echo "Success! Siteplan ID: " . $result['siteplan_id'];
        return $result['siteplan_id'];
    } else {
        echo "Error: $httpCode - $response";
        return null;
    }
}

// Usage
sendSiteplanToLumina(
    'Luxury Villa Project',
    '/path/to/siteplan.obj',
    [
        'archidep_version' => '2.1.0',
        'render_quality' => 'ultra'
    ]
);

?>
```

## 🔄 Automated Workflow

### Archidep Automation Script

```python
#!/usr/bin/env python3
"""
Archidep to Lumina OS Automation Script
Monitors output directory and automatically sends new siteplans
"""

import os
import time
import requests
from pathlib import Path

# Configuration
LUMINA_WEBHOOK_URL = "http://yourdomain.com/api/webhooks/archidep/receive-siteplan"
API_KEY = "Lumina-Archidep-Secret-X99"
ARCHIDEP_OUTPUT_DIR = "/path/to/archidep/output"
PROCESSED_DIR = "/path/to/archidep/processed"

def monitor_output_directory():
    """Monitor Archidep output directory for new files"""
    
    processed_files = set()
    
    # Load processed files list
    if os.path.exists(f"{PROCESSED_DIR}/processed_files.txt"):
        with open(f"{PROCESSED_DIR}/processed_files.txt", "r") as f:
            processed_files = set(line.strip() for line in f)
    
    while True:
        try:
            # Scan for new files
            for file_path in Path(ARCHIDEP_OUTPUT_DIR).glob("*.obj"):
                if str(file_path) not in processed_files:
                    print(f"New siteplan detected: {file_path}")
                    
                    # Send to Lumina OS
                    project_name = file_path.stem
                    metadata = {
                        "archidep_version": "2.1.0",
                        "auto_detected": True,
                        "detected_at": time.time()
                    }
                    
                    if send_to_lumina(project_name, str(file_path), metadata):
                        # Mark as processed
                        processed_files.add(str(file_path))
                        
                        # Save processed files list
                        with open(f"{PROCESSED_DIR}/processed_files.txt", "w") as f:
                            f.write("\n".join(processed_files))
                        
                        # Move to processed directory
                        processed_path = Path(PROCESSED_DIR) / file_path.name
                        file_path.rename(processed_path)
                        
                        print(f"✅ Processed: {project_name}")
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error in monitoring: {e}")
            time.sleep(60)  # Wait longer on error

def send_to_lumina(project_name, file_path, metadata):
    """Send file to Lumina OS webhook"""
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'project_name': project_name,
                'file_type': '3D_MODEL',
                'metadata': json.dumps(metadata)
            }
            headers = {'X-API-KEY': API_KEY}
            
            response = requests.post(
                LUMINA_WEBHOOK_URL,
                headers=headers,
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Webhook success: {result['siteplan_id']}")
                return True
            else:
                print(f"❌ Webhook failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error sending to Lumina: {e}")
        return False

if __name__ == "__main__":
    print("🚁 Starting Archidep to Lumina OS monitoring...")
    monitor_output_directory()
```

## 🔒 Security Considerations

### API Key Protection
- Store the `ARCHIDEP_SECRET_KEY` securely in environment variables
- Never expose the secret key in client-side code
- Use HTTPS for all webhook communications
- Implement IP whitelisting if needed

### File Validation
- The webhook validates file types and sizes
- Files are scanned for integrity using SHA-256 hashing
- Suspicious files are rejected automatically

### Rate Limiting
- Consider implementing rate limiting for webhook endpoints
- Monitor for unusual activity patterns
- Set up alerts for failed webhook attempts

## 🚨 Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check if `X-API-KEY` header matches `ARCHIDEP_SECRET_KEY`
   - Ensure the environment variable is set correctly

2. **400 Bad Request**
   - Verify required fields are present
   - Check file format and size limits
   - Ensure JSON payload is valid

3. **500 Internal Server Error**
   - Check server logs for detailed error messages
   - Verify database connectivity
   - Ensure upload directory permissions

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

Check webhook health:
```bash
curl http://yourdomain.com/api/webhooks/archidep/health
```

## 📞 Support

For integration support:
- **Documentation**: https://docs.lumina.tech/webhooks
- **API Reference**: http://yourdomain.com/api/webhooks/archidep/webhook-info
- **Support Email**: support@lumina.tech

---

**🤖 The M2M webhook system is now ready for Archidep integration!**
