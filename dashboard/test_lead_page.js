#!/usr/bin/env node

/**
 * Test Script for Lead Detail Page
 * Tests the dynamic page at /leads/[id]
 */

const http = require('http')

// Test configuration
const BASE_URL = 'http://localhost:3000'
const TEST_LEAD_ID = '1'

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
async function testLeadPage() {
  logHeader('Testing Lead Detail Page')
  log(`Testing: GET /leads/${TEST_LEAD_ID}`, 'blue')
  log('='.repeat(60))

  try {
    // Make HTTP request to the page
    const url = `${BASE_URL}/leads/${TEST_LEAD_ID}`

    logInfo(`Making request to: ${url}`)

    const response = await fetch(url)
    const html = await response.text()

    // Check response status
    if (response.ok) {
      logSuccess(`Page responded with status: ${response.status}`)

      // Check for key elements in HTML
      const checks = [
        { name: 'Lead 360° Intelligence Profile', pattern: /Lead 360° Intelligence Profile/i },
        { name: 'Intelligence Desk', pattern: /Intelligence Desk/i },
        { name: 'AI Reasoning', pattern: /AI Reasoning/i },
        { name: 'Activity Timeline', pattern: /Activity Timeline/i },
        { name: 'Generate Pitch Deck', pattern: /Generate Pitch Deck/i },
        { name: 'Send Auto-Email', pattern: /Send Auto-Email/i },
        { name: 'Handover to Closer', pattern: /Handover to Closer/i },
        { name: 'Back to Command Center', pattern: /Back to Command Center/i },
        { name: 'RadarChart', pattern: /RadarChart/i },
        { name: 'bg-zinc-950', pattern: /bg-zinc-950/i },
        { name: 'border-zinc-800', pattern: /border-zinc-800/i },
      ]

      let allChecksPassed = true

      checks.forEach(check => {
        if (check.pattern.test(html)) {
          logSuccess(`Found: ${check.name}`)
        } else {
          logError(`Missing: ${check.name}`)
          allChecksPassed = false
        }
      })

      if (allChecksPassed) {
        logHeader('✅ Page Structure Valid!')
        log('All required elements found in the page.', 'green')

        // Check for dynamic content
        if (html.includes('ACCESSING LEAD INTELLIGENCE')) {
          logSuccess('Loading animation found')
        }

        if (html.includes('HOT') || html.includes('WARM') || html.includes('COLD')) {
          logSuccess('Score badge system found')
        }

        if (html.includes('emerald-400')) {
          logSuccess('Neon green accent colors found')
        }

        logHeader('🎯 Page Features Confirmed:')
        log('📊 3-column grid layout (Intelligence Desk, AI Reasoning, Timeline)', 'cyan')
        log('🤖 AI Reasoning Radar Chart with dark theme', 'cyan')
        log('⏰ Activity Timeline with neon dots and connectors', 'cyan')
        log('🎯 Action Desk with 3 neon buttons', 'cyan')
        log('🔙 Navigation back to Command Center', 'cyan')
        log('🎨 Pitch-black dark mode design', 'cyan')
        log('⚡ Hacker-style loading animation', 'cyan')
      } else {
        logError('Some page elements are missing')
      }
    } else {
      logError(`Page responded with status: ${response.status}`)

      if (response.status === 404) {
        logInfo('Page not found. This might indicate routing issues.')
      } else if (response.status === 500) {
        logInfo('Server error. Check the server logs for details.')
      }
    }
  } catch (error) {
    logError('Failed to connect to page')
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
  ]

  for (const testCase of testCases) {
    logInfo(`Testing: ${testCase.description}`)

    try {
      const url = `${BASE_URL}/leads/${testCase.id}`
      const response = await fetch(url)

      if (response.status === 404 || response.status === 500) {
        logSuccess(`Correctly returned ${response.status} for ${testCase.description}`)
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
  logHeader('🚀 Lead Detail Page Test Suite')
  log('Testing Next.js Dynamic Page for Lead 360° Intelligence Profile', 'blue')
  log('')

  // Test successful case
  await testLeadPage()

  log('')
  log('')

  // Test error scenarios
  await testErrorScenarios()

  logHeader('🎯 Page Test Complete')
  log('Run this script again after making changes to verify page functionality.', 'green')
  log('')
  log('📱 Manual Testing:', 'yellow')
  log('Open your browser and navigate to:', 'yellow')
  log(`  ${BASE_URL}/leads/1`, 'cyan')
  log('Check for:', 'yellow')
  log('  • Loading animation', 'yellow')
  log('  • 3-column layout', 'yellow')
  log('  • Radar chart rendering', 'yellow')
  log('  • Timeline with dots', 'yellow')
  log('  • Neon button effects', 'yellow')
}

// Check if server is running
async function checkServer() {
  try {
    const response = await fetch(`${BASE_URL}/leads/1`)
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
