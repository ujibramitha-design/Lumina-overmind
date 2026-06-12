#!/bin/bash

# LUMINA OS - Archidep Webhook Test Script
# Test the M2M webhook integration with Archidep system

echo "🤖 Testing Archidep M2M Webhook Integration"
echo "=============================================="

# Configuration
WEBHOOK_URL="http://localhost:8000/api/webhooks/archidep/receive-siteplan"
API_KEY="Lumina-Archidep-Secret-X99"
TEST_FILE="/tmp/test_siteplan.obj"

# Create test file
echo "📁 Creating test file..."
cat > "$TEST_FILE" << 'EOF'
# Test OBJ file for webhook testing
# This is a simulated 3D model file
v 0.0.0 obj
# Test siteplan data
g siteplan_test
# End of test file
EOF

# Test 1: Webhook Info
echo ""
echo "📋 Test 1: Getting webhook info..."
curl -s "$WEBHOOK_URL/../webhook-info" | python3 -m json.tool || echo "❌ Failed to get webhook info"

# Test 2: JSON Webhook
echo ""
echo "📋 Test 2: JSON webhook..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Test Project JSON",
    "file_url": "https://example.com/test.obj",
    "file_type": "3D_MODEL",
    "metadata": {
      "test_mode": true,
      "timestamp": "'$(date -I)'"
    }
  }' | python3 -m json.tool || echo "❌ JSON webhook failed"

# Test 3: File Upload Webhook
echo ""
echo "📋 Test 3: File upload webhook..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "X-API-KEY: $API_KEY" \
  -F "project_name=Test Project File" \
  -F "file=@$TEST_FILE" \
  -F "file_type=3D_MODEL" \
  -F 'metadata={"test_mode": true, "upload_type": "file"}' | python3 -m json.tool || echo "❌ File upload webhook failed"

# Test 4: Status Update
echo ""
echo "📋 Test 4: Status update..."
curl -s -X POST "$WEBHOOK_URL/../status-update" \
  -H "X-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "siteplan_id": "test-siteplan-id",
    "status": "RENDERING"
  }' | python3 -m json.tool || echo "❌ Status update failed"

# Test 5: Health Check
echo ""
echo "📋 Test 5: Webhook health check..."
curl -s "$WEBHOOK_URL/../health" | python3 -m json.tool || echo "❌ Health check failed"

# Test 6: Invalid API Key
echo ""
echo "📋 Test 6: Invalid API key (should fail)..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "X-API-KEY: invalid-key" \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Test", "file_url": "https://example.com/test.obj"}' | python3 -m json.tool || echo "❌ Invalid key test failed (expected)"

# Cleanup
echo ""
echo "🧹 Cleaning up test files..."
rm -f "$TEST_FILE"

echo ""
echo "✅ Webhook tests completed!"
echo ""
echo "📊 Test Summary:"
echo "  - Webhook info: Check endpoint configuration"
echo "  - JSON webhook: Test JSON payload handling"
echo "  - File upload: Test multipart file upload"
echo "  - Status update: Test status update webhook"
echo "  - Health check: Verify system health"
echo "  - Invalid key: Test authentication"
echo ""
echo "🚀 Ready for Archidep integration!"
