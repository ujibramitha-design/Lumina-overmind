/**
 * LUMINA OVERMIND SYSTEM - Store Hydration Hook
 *
 * Provides server-side data hydration for Zustand state management
 * Ensures UI state consistency across page refreshes and navigation
 */

import { useEffect } from 'react'
import { useAppStore } from '@/lib/store'

interface HydrationData {
  runners?: any[]
  systemMetrics?: any
  user?: any
  lastSync?: string
}

export const useStoreHydration = () => {
  const { setRunners, setSystemMetrics, setUser, setLastSync } = useAppStore()

  useEffect(() => {
    /**
     * Hydrate store state from server-side data
     * Called on initial page load to restore state
     */
    const hydrateStore = async () => {
      try {
        // Fetch initial data from API
        const response = await fetch('/api/system/status')

        if (response.ok) {
          const data: HydrationData = await response.json()

          // Hydrate runners state
          if (data.runners) {
            setRunners(data.runners)
          }

          // Hydrate system metrics
          if (data.systemMetrics) {
            setSystemMetrics(data.systemMetrics)
          }

          // Hydrate user state
          if (data.user) {
            setUser(data.user)
          }

          // Update last sync timestamp
          setLastSync(new Date(data.lastSync || new Date()))

          console.log('✅ Store hydrated successfully')
        } else {
          console.warn('⚠️ Store hydration failed:', response.statusText)
        }
      } catch (error) {
        console.error('❌ Store hydration error:', error)
      }
    }

    // Only hydrate on client-side
    if (typeof window !== 'undefined') {
      hydrateStore()
    }
  }, [setRunners, setSystemMetrics, setUser, setLastSync])

  return {
    /**
     * Manual hydration trigger for specific data refresh
     */
    rehydrate: async () => {
      try {
        const response = await fetch('/api/system/status')
        if (response.ok) {
          const data = await response.json()

          if (data.runners) setRunners(data.runners)
          if (data.systemMetrics) setSystemMetrics(data.systemMetrics)
          if (data.user) setUser(data.user)
          setLastSync(new Date())

          return true
        }
      } catch (error) {
        console.error('Manual rehydration failed:', error)
        return false
      }
    },
  }
}

/**
 * Error boundary for store hydration failures
 */
export class StoreHydrationError extends Error {
  constructor(
    message: string,
    public cause?: Error
  ) {
    super(message)
    this.name = 'StoreHydrationError'
  }
}

export default useStoreHydration
