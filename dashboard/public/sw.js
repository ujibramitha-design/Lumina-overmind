/**
 * LUMINA OVERMIND SYSTEM - Service Worker
 * 
 * Provides offline capabilities and caching for enterprise-grade resilience
 * Ensures system functionality during network interruptions
 */

const CACHE_NAME = 'lumina-overmind-v1'
const STATIC_CACHE = 'lumina-static-v1'
const API_CACHE = 'lumina-api-v1'

// Critical assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/dashboard',
  '/api/system/status',
  '/manifest.json'
]

// API endpoints to cache with network-first strategy
const API_ENDPOINTS = [
  '/api/system/status',
  '/api/runners/status',
  '/api/intelligence/leads'
]

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('🚀 LUMINA OVERMIND SW: Installing')
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('✅ Caching static assets')
        return cache.addAll(STATIC_ASSETS)
      })
      .then(() => self.skipWaiting())
  )
})

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('⚡ LUMINA OVERMIND SW: Activating')
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => 
              name !== STATIC_CACHE && 
              name !== API_CACHE &&
              name !== CACHE_NAME
            )
            .map((name) => {
              console.log('🗑️ Deleting old cache:', name)
              return caches.delete(name)
            })
        )
      })
      .then(() => self.clients.claim())
  )
})

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Skip non-GET requests and external resources
  if (request.method !== 'GET' || url.origin !== location.origin) {
    return
  }

  // API endpoints - Network first, fallback to cache
  if (API_ENDPOINTS.some(endpoint => url.pathname.startsWith(endpoint))) {
    event.respondWith(networkFirst(request))
    return
  }

  // Static assets - Cache first
  if (STATIC_ASSETS.some(asset => url.pathname === asset)) {
    event.respondWith(cacheFirst(request))
    return
  }

  // Dynamic content - Network with cache fallback
  event.respondWith(networkFirst(request))
})

// Network-first strategy for API calls
async function networkFirst(request) {
  try {
    // Try network first
    const response = await fetch(request)
    
    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(API_CACHE)
      cache.put(request, response.clone())
    }
    
    return response
  } catch (error) {
    console.log('🌐 Network failed, trying cache:', request.url)
    
    // Fallback to cache
    const cachedResponse = await caches.match(request)
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Return offline fallback for critical endpoints
    if (request.url.includes('/api/system/status')) {
      return new Response(JSON.stringify({
        runners: [],
        systemMetrics: {
          systemLoad: 0,
          activeRunners: 0,
          totalRunners: 6,
          apiRateLimit: 'Offline'
        },
        lastSync: new Date().toISOString(),
        offline: true
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }
    
    throw error
  }
}

// Cache-first strategy for static assets
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request)
  
  if (cachedResponse) {
    return cachedResponse
  }
  
  try {
    const response = await fetch(request)
    
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE)
      cache.put(request, response.clone())
    }
    
    return response
  } catch (error) {
    console.log('❌ Failed to fetch:', request.url)
    throw error
  }
}

// Background sync for offline actions
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync())
  }
})

async function doBackgroundSync() {
  console.log('🔄 Performing background sync')
  
  try {
    // Sync any queued offline actions
    const response = await fetch('/api/sync/offline-actions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (response.ok) {
      console.log('✅ Background sync completed')
    }
  } catch (error) {
    console.error('❌ Background sync failed:', error)
  }
}

// Push notifications
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json()
    
    event.waitUntil(
      self.registration.showNotification('LUMINA OVERMIND', {
        body: data.message,
        icon: '/icon-192x192.png',
        badge: '/badge-72x72.png',
        tag: 'lumina-notification',
        requireInteraction: data.urgent || false,
        actions: [
          {
            action: 'view',
            title: 'View Details'
          },
          {
            action: 'dismiss',
            title: 'Dismiss'
          }
        ]
      })
    )
  }
})

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/dashboard')
    )
  }
})

console.log('🎯 LUMINA OVERMIND Service Worker Loaded')
