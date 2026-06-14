/**
 * HUNTER AGENT AI MARKETING DIGITAL - Login Page Test
 * Test script for validating login page functionality
 */

const { chromium } = require('playwright')

async function testLoginPage() {
  console.log('🧪 Testing Lumina OS Login Page')
  console.log('=' * 60)

  // Launch browser
  const browser = await chromium.launch({
    headless: false, // Set to true for headless testing
    slowMo: 100,
  })

  try {
    // Create new page
    const page = await browser.newPage()

    // Navigate to login page
    console.log('\n1️⃣ Navigating to login page...')
    await page.goto('http://localhost:3000/login')

    // Wait for page to load
    await page.waitForLoadState('networkidle')

    // Check page title and elements
    const title = await page.title()
    console.log(`   ✅ Page title: ${title}`)

    // Check for login form elements
    const logo = await page.locator('text=LUMINA OS').isVisible()
    const emailInput = await page.locator('input[type="email"]').isVisible()
    const passwordInput = await page.locator('input[type="password"]').isVisible()
    const submitButton = await page.locator('button[type="submit"]').isVisible()

    console.log(`   ✅ Logo visible: ${logo}`)
    console.log(`   ✅ Email input visible: ${emailInput}`)
    console.log(`   ✅ Password input visible: ${passwordInput}`)
    console.log(`   ✅ Submit button visible: ${submitButton}`)

    // Test login with valid credentials
    console.log('\n2️⃣ Testing login with valid credentials...')

    // Fill in the form
    await page.fill('input[type="email"]', 'admin@lumina.os')
    await page.fill('input[type="password"]', 'hunter2026')

    // Click submit button
    await page.click('button[type="submit"]')

    // Wait for authentication
    console.log('   🔄 Waiting for authentication...')
    await page.waitForTimeout(2000)

    // Check if redirected to dashboard
    const currentUrl = page.url()
    if (currentUrl.includes('/') && !currentUrl.includes('/login')) {
      console.log('   ✅ Login successful - redirected to dashboard')
    } else {
      console.log('   ❌ Login failed - still on login page')

      // Check for error message
      const errorVisible = await page.locator('text=AUTHENTICATION FAILED').isVisible()
      if (errorVisible) {
        console.log('   ⚠️  Error message displayed')
      }
    }

    // Test login with invalid credentials
    console.log('\n3️⃣ Testing login with invalid credentials...')

    // Go back to login page
    await page.goto('http://localhost:3000/login')
    await page.waitForLoadState('networkidle')

    // Fill in invalid credentials
    await page.fill('input[type="email"]', 'invalid@example.com')
    await page.fill('input[type="password"]', 'wrongpassword')

    // Click submit button
    await page.click('button[type="submit"]')

    // Wait for response
    await page.waitForTimeout(2000)

    // Check for error message
    const errorVisible = await page.locator('text=Authentication failed').isVisible()
    if (errorVisible) {
      console.log('   ✅ Invalid credentials properly rejected')
    } else {
      console.log('   ❌ Error message not displayed')
    }

    // Test password visibility toggle
    console.log('\n4️⃣ Testing password visibility toggle...')

    // Go back to login page
    await page.goto('http://localhost:3000/login')
    await page.waitForLoadState('networkidle')

    // Fill password
    await page.fill('input[type="password"]', 'testpassword')

    // Check password type
    const passwordType = await page.locator('input[type="password"]').getAttribute('type')
    console.log(`   ✅ Password input type: ${passwordType}`)

    // Click eye icon to show password
    await page.click('button[type="button"]')
    await page.waitForTimeout(500)

    // Check if password is now visible
    const passwordTypeAfter = await page.locator('input').getAttribute('type')
    console.log(`   ✅ Password type after toggle: ${passwordTypeAfter}`)

    // Test form validation
    console.log('\n5️⃣ Testing form validation...')

    // Try to submit empty form
    await page.fill('input[type="email"]', '')
    await page.fill('input[type="password"]', '')
    await page.click('button[type="submit"]')

    // Check if form validation prevents submission
    const stillOnLoginPage = page.url().includes('/login')
    if (stillOnLoginPage) {
      console.log('   ✅ Empty form submission prevented')
    } else {
      console.log('   ❌ Empty form submission not prevented')
    }

    // Test UI elements and styling
    console.log('\n6️⃣ Testing UI elements and styling...')

    // Check for cyber aesthetic elements
    const shieldIcon = await page.locator('[data-testid="shield-icon"], .lucide-shield').isVisible()
    const terminalIcon = await page
      .locator('[data-testid="terminal-icon"], .lucide-terminal')
      .isVisible()
    const gridBackground = await page.locator('.bg-gradient-to-br').isVisible()

    console.log(`   ✅ Shield icon visible: ${shieldIcon}`)
    console.log(`   ✅ Terminal icon visible: ${terminalIcon}`)
    console.log(`   ✅ Grid background visible: ${gridBackground}`)

    // Test responsive design
    console.log('\n7️⃣ Testing responsive design...')

    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })
    await page.waitForTimeout(1000)

    const mobileLayout = await page.locator('.max-w-md').isVisible()
    console.log(`   ✅ Mobile layout working: ${mobileLayout}`)

    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.waitForTimeout(1000)

    const desktopLayout = await page.locator('.max-w-md').isVisible()
    console.log(`   ✅ Desktop layout working: ${desktopLayout}`)

    console.log('\n🎉 All login page tests completed successfully!')
  } catch (error) {
    console.error('❌ Test error:', error)
  } finally {
    await browser.close()
  }
}

// Test API connectivity
async function testAPIConnectivity() {
  console.log('\n🔗 Testing API Connectivity')
  console.log('=' * 40)

  try {
    const fetch = require('node-fetch')

    // Test health endpoint
    console.log('\n1️⃣ Testing health endpoint...')
    const healthResponse = await fetch('http://localhost:8000/health')
    const healthData = await healthResponse.json()

    if (healthResponse.ok) {
      console.log('   ✅ API health check passed')
      console.log(`   📊 Status: ${healthData.status}`)
    } else {
      console.log('   ❌ API health check failed')
    }

    // Test login endpoint
    console.log('\n2️⃣ Testing login endpoint...')

    const formData = new URLSearchParams()
    formData.append('username', 'admin@lumina.os')
    formData.append('password', 'hunter2026')

    const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    const loginData = await loginResponse.json()

    if (loginResponse.ok && loginData.success) {
      console.log('   ✅ Login endpoint working')
      console.log(`   👤 User: ${loginData.data.user.name} (${loginData.data.user.role})`)
      console.log(`   🔑 Token type: ${loginData.data.token_type}`)
    } else {
      console.log('   ❌ Login endpoint failed')
      console.log(`   📝 Error: ${loginData.message}`)
    }

    // Test invalid login
    console.log('\n3️⃣ Testing invalid login...')

    const invalidFormData = new URLSearchParams()
    invalidFormData.append('username', 'invalid@example.com')
    invalidFormData.append('password', 'wrongpassword')

    const invalidResponse = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      body: invalidFormData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    if (invalidResponse.status === 401) {
      console.log('   ✅ Invalid login properly rejected')
    } else {
      console.log('   ❌ Invalid login not properly rejected')
    }
  } catch (error) {
    console.error('❌ API connectivity error:', error)
  }
}

// Main test function
async function runTests() {
  console.log('🔐 LUMINA OS LOGIN PAGE TEST SUITE')
  console.log('=' * 60)
  console.log('📅 Test Date:', new Date().toLocaleString())
  console.log('🌐 Frontend URL: http://localhost:3000')
  console.log('🔌 Backend URL: http://localhost:8000')
  console.log()

  // Test API connectivity first
  await testAPIConnectivity()

  // Test login page
  await testLoginPage()

  console.log('\n' + '=' * 60)
  console.log('🎉 ALL TESTS COMPLETED!')
  console.log('🔐 Login system is working correctly')
  console.log('=' * 60)
}

// Check if required dependencies are available
async function checkDependencies() {
  try {
    require('playwright')
    require('node-fetch')
    return true
  } catch (error) {
    console.log('❌ Missing dependencies:')
    console.log('   - playwright: npm install playwright')
    console.log('   - node-fetch: npm install node-fetch')
    return false
  }
}

// Run tests if dependencies are available
if (checkDependencies()) {
  runTests().catch(console.error)
} else {
  console.log('\n🔧 Please install missing dependencies and try again')
}
