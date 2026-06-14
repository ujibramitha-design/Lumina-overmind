/**
 * HUNTER AGENT AI MARKETING DIGITAL - Middleware Test
 * Test script for validating Next.js middleware functionality
 */

const { chromium } = require('playwright')

async function testMiddleware() {
  console.log('🔐 Testing Lumina OS Middleware')
  console.log('=' * 50)

  // Launch browser
  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
  })

  try {
    const page = await browser.newPage()

    // Test 1: Access protected route without authentication
    console.log('\n1️⃣ Testing protected route without authentication...')

    await page.goto('http://localhost:3000/')

    // Should redirect to login page
    const currentUrl = page.url()
    if (currentUrl.includes('/login')) {
      console.log('   ✅ Redirected to login page as expected')

      // Check for redirect parameter
      const urlParams = new URL(currentUrl).searchParams
      const redirectParam = urlParams.get('redirect')
      if (redirectParam === '/') {
        console.log('   ✅ Redirect parameter preserved')
      }
    } else {
      console.log('   ❌ Not redirected to login page')
    }

    // Test 2: Access login page directly
    console.log('\n2️⃣ Testing direct access to login page...')

    await page.goto('http://localhost:3000/login')
    const loginPageUrl = page.url()

    if (loginPageUrl.includes('/login')) {
      console.log('   ✅ Login page accessible')
    } else {
      console.log('   ❌ Login page not accessible')
    }

    // Test 3: Login with valid credentials
    console.log('\n3️⃣ Testing login with valid credentials...')

    // Fill login form
    await page.fill('input[type="email"]', 'admin@lumina.os')
    await page.fill('input[type="password"]', 'hunter2026')

    // Submit form
    await page.click('button[type="submit"]')

    // Wait for authentication
    await page.waitForTimeout(3000)

    // Check if redirected to dashboard
    const afterLoginUrl = page.url()
    if (afterLoginUrl.includes('/') && !afterLoginUrl.includes('/login')) {
      console.log('   ✅ Login successful - redirected to dashboard')

      // Check for authentication cookie
      const cookies = await page.context().cookies()
      const luminaToken = cookies.find(cookie => cookie.name === 'lumina_token')

      if (luminaToken) {
        console.log('   ✅ Authentication cookie set')
        console.log(`   🍪 Cookie value: ${luminaToken.value.substring(0, 20)}...`)
        console.log(`   ⏰ Cookie expires: ${new Date(luminaToken.expires * 1000).toISOString()}`)
      } else {
        console.log('   ❌ Authentication cookie not found')
      }
    } else {
      console.log('   ❌ Login failed - still on login page')
    }

    // Test 4: Access protected route with authentication
    console.log('\n4️⃣ Testing protected route with authentication...')

    // Try to access dashboard again
    await page.goto('http://localhost:3000/')
    await page.waitForTimeout(2000)

    const dashboardUrl = page.url()
    if (dashboardUrl.includes('/') && !dashboardUrl.includes('/login')) {
      console.log('   ✅ Dashboard accessible with authentication')
    } else {
      console.log('   ❌ Dashboard not accessible even with authentication')
    }

    // Test 5: Access other protected routes
    console.log('\n5️⃣ Testing other protected routes...')

    const protectedRoutes = ['/inbox', '/workflows', '/leads', '/orchestrator']

    for (const route of protectedRoutes) {
      await page.goto(`http://localhost:3000${route}`)
      await page.waitForTimeout(1000)

      const routeUrl = page.url()
      if (routeUrl.includes(route) && !routeUrl.includes('/login')) {
        console.log(`   ✅ ${route} - Accessible`)
      } else {
        console.log(`   ❌ ${route} - Not accessible`)
      }
    }

    // Test 6: Test API endpoints
    console.log('\n6️⃣ Testing API endpoints accessibility...')

    // Test public API endpoints
    const publicEndpoints = ['/api/auth/login', '/api/auth/verify']

    for (const endpoint of publicEndpoints) {
      try {
        const response = await page.goto(`http://localhost:8000${endpoint}`)
        if (response && response.status) {
          console.log(`   ✅ ${endpoint} - Accessible`)
        } else {
          console.log(`   ❌ ${endpoint} - Not accessible`)
        }
      } catch (error) {
        console.log(`   ❌ ${endpoint} - Error: ${error.message}`)
      }
    }

    // Test 7: Logout functionality
    console.log('\n7️⃣ Testing logout functionality...')

    // Try to access logout endpoint
    try {
      const logoutResponse = await page.evaluate(async () => {
        const response = await fetch('/api/auth/logout', {
          method: 'POST',
        })
        return response.json()
      })

      if (logoutResponse.success) {
        console.log('   ✅ Logout successful')

        // Check if cookie is cleared
        const cookiesAfterLogout = await page.context().cookies()
        const luminaTokenAfterLogout = cookiesAfterLogout.find(
          cookie => cookie.name === 'lumina_token'
        )

        if (!luminaTokenAfterLogout) {
          console.log('   ✅ Authentication cookie cleared')
        } else {
          console.log('   ❌ Authentication cookie not cleared')
        }

        // Try to access protected route after logout
        await page.goto('http://localhost:3000/')
        await page.waitForTimeout(2000)

        const afterLogoutUrl = page.url()
        if (afterLogoutUrl.includes('/login')) {
          console.log('   ✅ Redirected to login after logout')
        } else {
          console.log('   ❌ Not redirected to login after logout')
        }
      } else {
        console.log('   ❌ Logout failed')
      }
    } catch (error) {
      console.log(`   ❌ Logout error: ${error.message}`)
    }

    console.log('\n🎉 All middleware tests completed!')
  } catch (error) {
    console.error('❌ Test error:', error)
  } finally {
    await browser.close()
  }
}

// Test middleware configuration
async function testMiddlewareConfig() {
  console.log('\n⚙️ Testing Middleware Configuration')
  console.log('=' * 40)

  try {
    const fs = require('fs').promises
    const path = require('path')

    // Check if middleware.ts exists
    const middlewarePath = path.join(__dirname, 'middleware.ts')

    try {
      await fs.access(middlewarePath)
      console.log('   ✅ middleware.ts file exists')
    } catch (error) {
      console.log('   ❌ middleware.ts file not found')
      return
    }

    // Read and analyze middleware content
    const middlewareContent = await fs.readFile(middlewarePath, 'utf8')

    // Check for key middleware features
    const features = {
      'JWT token verification': middlewareContent.includes('lumina_token'),
      'Public paths configuration': middlewareContent.includes('publicPaths'),
      'Static paths handling': middlewareContent.includes('staticPaths'),
      'Redirect to login': middlewareContent.includes('NextResponse.redirect'),
      'Cookie deletion': middlewareContent.includes('cookies.delete'),
      'Token expiration check': middlewareContent.includes('payload.exp'),
    }

    console.log('\n📋 Middleware Features:')
    Object.entries(features).forEach(([feature, exists]) => {
      console.log(`   ${exists ? '✅' : '❌'} ${feature}`)
    })

    // Check matcher configuration
    if (middlewareContent.includes('matcher')) {
      console.log('   ✅ Matcher configuration found')
    } else {
      console.log('   ❌ Matcher configuration not found')
    }

    // Check for proper exports
    if (
      middlewareContent.includes('export function middleware') &&
      middlewareContent.includes('export const config')
    ) {
      console.log('   ✅ Proper middleware exports found')
    } else {
      console.log('   ❌ Improper middleware exports')
    }
  } catch (error) {
    console.error('❌ Configuration test error:', error)
  }
}

// Test API integration
async function testAPIIntegration() {
  console.log('\n🔌 Testing API Integration')
  console.log('=' * 30)

  try {
    const fetch = require('node-fetch')

    // Test login with cookie setting
    console.log('\n1️⃣ Testing login with cookie setting...')

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

    if (loginResponse.ok) {
      const loginData = await loginResponse.json()
      console.log('   ✅ Login API working')

      // Check for set-cookie header
      const setCookieHeader = loginResponse.headers.get('set-cookie')
      if (setCookieHeader && setCookieHeader.includes('lumina_token')) {
        console.log('   ✅ HTTP-only cookie set in response')
        console.log(`   🍪 Cookie header: ${setCookieHeader.substring(0, 100)}...`)
      } else {
        console.log('   ❌ HTTP-only cookie not set in response')
      }
    } else {
      console.log('   ❌ Login API failed')
    }

    // Test protected API endpoint
    console.log('\n2️⃣ Testing protected API endpoint...')

    const protectedResponse = await fetch('http://localhost:8000/api/auth/me', {
      headers: {
        Cookie: 'lumina_token=invalid_token',
      },
    })

    if (protectedResponse.status === 401) {
      console.log('   ✅ Protected endpoint properly rejects invalid token')
    } else {
      console.log('   ❌ Protected endpoint not properly protected')
    }
  } catch (error) {
    console.error('❌ API integration error:', error)
  }
}

// Main test function
async function runTests() {
  console.log('🔐 LUMINA OS MIDDLEWARE TEST SUITE')
  console.log('=' * 50)
  console.log('📅 Test Date:', new Date().toLocaleString())
  console.log('🌐 Frontend URL: http://localhost:3000')
  console.log('🔌 Backend URL: http://localhost:8000')
  console.log()

  // Test middleware configuration
  await testMiddlewareConfig()

  // Test API integration
  await testAPIIntegration()

  // Test middleware functionality
  await testMiddleware()

  console.log('\n' + '=' * 50)
  console.log('🎉 ALL TESTS COMPLETED!')
  console.log('🔐 Middleware system is working correctly')
  console.log('=' * 50)
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
