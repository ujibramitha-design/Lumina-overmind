#!/usr/bin/env node

/**
 * Test Script for Lead Detail API Route
 * Tests the dynamic API route at /api/leads/[id]
 */

const http = require('http')

// Test configuration
const BASE_URL = 'http://localhost:3000'
const TEST_LEAD_ID = '1' // Assuming we have at least one lead with ID 1

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m',
  reset: '\x1b[0m',
}

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`)
}

function logSuccess(message) {
  log(`✅ ${message}`, 'green')
}

function logError(message) {
  log(`❌ ${message}`, 'red')
}

function logInfo(message) {
  log(`ℹ️  ${message}`, 'blue')
}

function logHeader(message) {
  log(`🔧 ${message}`, 'bold cyan')
}

// Test function
async function testLeadAPI() {
  logHeader('Testing Lead Detail API Route')
  log(`Testing: GET /api/leads/${TEST_LEAD_ID}`, 'blue')
  log('='.repeat(60))

  try {
    // Make HTTP request to the API
    const url = `${BASE_URL}/api/leads/${TEST_LEAD_ID}`

    logInfo(`Making request to: ${url}`)

    const response = await fetch(url)
    const data = await response.json()

    // Check response status
    if (response.ok) {
      logSuccess(`API responded with status: ${response.status}`)

      // Validate response structure
      if (data.success) {
        logSuccess('Response structure is valid')

        const lead = data.data

        // Check required fields
        const requiredFields = ['id', 'business_name', 'contact', 'ai_reasoning', 'timeline']
        let allFieldsPresent = true

        requiredFields.forEach(field => {
          if (lead[field] === undefined) {
            logError(`Missing required field: ${field}`)
            allFieldsPresent = false
          } else {
            logSuccess(`Field present: ${field}`)
          }
        })

        if (allFieldsPresent) {
          logHeader('Lead Data Summary:')
          log(`📋 Business: ${lead.business_name}`, 'yellow')
          log(`👤 Contact: ${lead.contact}`, 'yellow')
          log(`📍 Location: ${lead.location || 'N/A'}`, 'yellow')
          log(`⭐ Score: ${lead.score || 'N/A'}`, 'yellow')
          log(`📊 Status: ${lead.status || 'N/A'}`, 'yellow')

          // Check AI Reasoning (Radar Chart)
          if (lead.ai_reasoning) {
            logHeader('AI Reasoning (Radar Chart):')
            const ai = lead.ai_reasoning
            log(`🎯 Intent: ${ai.intent}`, 'cyan')
            log(`💰 Budget: ${ai.budget}`, 'cyan')
            log(`⚡ Urgency: ${ai.urgency}`, 'cyan')
            log(`🔧 Fit: ${ai.fit}`, 'cyan')
            log(`👑 Authority: ${ai.authority}`, 'cyan')
          }

          // Check Timeline
          if (lead.timeline && Array.isArray(lead.timeline)) {
            logHeader(`Timeline Activities (${lead.timeline.length}):`)
            lead.timeline.forEach((activity, index) => {
              log(`${index + 1}. ${activity.activity}`, 'cyan')
              log(`   📅 ${new Date(activity.timestamp).toLocaleString()}`, 'blue')
              log(`   🏷️  Type: ${activity.type}`, 'blue')
              if (activity.details) {
                log(`   📝 Details: ${activity.details}`, 'blue')
              }
              log('')
            })
          }

          logHeader('✅ API Test Successful!')
          log('The lead detail API route is working correctly with all required data.', 'green')
        }
      } else {
        logError('Response success flag is false')
        log(`Message: ${data.message || 'Unknown error'}`, 'red')
      }
    } else {
      logError(`API responded with status: ${response.status}`)

      if (response.status === 404) {
        logInfo('Lead not found. This might be expected if database is empty.')
        logInfo('Try running: python data/database_forge.py to populate sample data.')
      } else {
        logError(`Error message: ${data.message || 'Unknown error'}`)
      }
    }
  } catch (error) {
    logError('Failed to connect to API')
    logError(`Error: ${error.message}`)

    if (error.code === 'ECONNREFUSED') {
      logInfo('Make sure the Next.js development server is running:')
      logInfo('  npm run dev', 'yellow')
      logInfo('Then run this test again.', 'yellow')
    }
  }
}

// Test different scenarios
async function testErrorScenarios() {
  logHeader('Testing Error Scenarios')
  log('='.repeat(60))

  const testCases = [
    { id: '999999', description: 'Non-existent lead ID' },
    { id: 'invalid', description: 'Invalid ID format' },
    { id: '', description: 'Empty ID' },
  ]

  for (const testCase of testCases) {
    logInfo(`Testing: ${testCase.description}`)

    try {
      const url = `${BASE_URL}/api/leads/${testCase.id}`
      const response = await fetch(url)
      const data = await response.json()

      if (!response.ok) {
        logSuccess(`Correctly returned ${response.status} for ${testCase.description}`)
        log(`Message: ${data.message}`, 'blue')
      } else {
        logError(`Expected error but got ${response.status} for ${testCase.description}`)
      }
    } catch (error) {
      logError(`Failed to test ${testCase.description}: ${error.message}`)
    }

    log('')
  }
}

// Main execution
async function main() {
  logHeader('🚀 Lead Detail API Route Test Suite')
  log('Testing Next.js Dynamic API Route for Lead Details', 'blue')
  log('')

  // Test successful case
  await testLeadAPI()

  log('')
  log('')

  // Test error scenarios
  await testErrorScenarios()

  logHeader('🎯 Test Suite Complete')
  log('Run this script again after making changes to verify API functionality.', 'green')
}

// Check if server is running
async function checkServer() {
  try {
    const response = await fetch(`${BASE_URL}/api/leads/1`)
    return true
  } catch (error) {
    return false
  }
}

// Run tests if server is available
async function runIfServerAvailable() {
  const serverRunning = await checkServer()

  if (!serverRunning) {
    logError('Next.js development server is not running!')
    logInfo('Please start the server with:', 'yellow')
    logInfo('  npm run dev', 'yellow')
    logInfo('Then run this test script again.', 'yellow')
    process.exit(1)
  }

  await main()
}

// Execute
runIfServerAvailable().catch(console.error)
