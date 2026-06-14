import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Paths that don't require authentication
const publicPaths = ['/login', '/api/auth/login', '/api/auth/login-json', '/api/auth/verify']
const staticPaths = ['/favicon.ico', '/_next/static', '/images', '/fonts']

// Admin-only paths that require special protection
const adminOnlyPaths = ['/settings/classified-vault']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow access to public paths
  if (publicPaths.some(path => pathname.startsWith(path))) {
    return NextResponse.next()
  }

  // Allow access to static assets
  if (staticPaths.some(path => pathname.startsWith(path))) {
    return NextResponse.next()
  }

  // Special protection for Classified Vault
  if (adminOnlyPaths.some(path => pathname.startsWith(path))) {
    return protectAdminRoute(request, pathname)
  }

  // Check for authentication token in HTTP-only cookie
  const token = request.cookies.get('lumina_token')?.value

  // If no token and trying to access protected route, redirect to login
  if (!token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Optional: Verify token validity (basic check)
  try {
    // Decode JWT token (basic verification)
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Math.floor(Date.now() / 1000)

    // Check if token is expired
    if (payload.exp && payload.exp < currentTime) {
      // Token expired, clear cookie and redirect to login
      const response = NextResponse.redirect(new URL('/login', request.url))
      response.cookies.delete('lumina_token')
      return response
    }

    // Token is valid, allow access
    return NextResponse.next()
  } catch (error) {
    // Invalid token, clear cookie and redirect to login
    const response = NextResponse.redirect(new URL('/login', request.url))
    response.cookies.delete('lumina_token')
    return response
  }
}

function protectAdminRoute(request: NextRequest, pathname: string) {
  // Check for authentication token
  const token = request.cookies.get('lumina_token')?.value

  if (!token) {
    // No token, redirect to login with unauthorized error
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    loginUrl.searchParams.set('error', 'unauthorized')
    return NextResponse.redirect(loginUrl)
  }

  try {
    // Decode JWT token and verify admin role
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Math.floor(Date.now() / 1000)

    // Check if token is expired
    if (payload.exp && payload.exp < currentTime) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('error', 'token_expired')
      const response = NextResponse.redirect(loginUrl)
      response.cookies.delete('lumina_token')
      return response
    }

    // Check if user has ADMIN role
    if (payload.role !== 'ADMIN') {
      // User is not admin, redirect to dashboard with unauthorized error
      const dashboardUrl = new URL('/dashboard', request.url)
      dashboardUrl.searchParams.set('error', 'unauthorized')
      dashboardUrl.searchParams.set('message', 'Admin access required for Classified Vault')
      return NextResponse.redirect(dashboardUrl)
    }

    // User is admin, allow access
    return NextResponse.next()
  } catch (error) {
    // Invalid token, redirect to login
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('error', 'invalid_token')
    const response = NextResponse.redirect(loginUrl)
    response.cookies.delete('lumina_token')
    return response
  }
}

// Configure middleware to run on specific paths
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/auth (authentication endpoints)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - login (login page)
     */
    '/((?!api/auth|_next/static|_next/image|favicon.ico|login).*)',
  ],
}
