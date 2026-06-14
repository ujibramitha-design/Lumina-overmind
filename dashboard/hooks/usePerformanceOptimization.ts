/**
 * LUMINA OVERMIND SYSTEM - Performance Optimization Hooks
 *
 * Provides memoization utilities and performance optimization patterns
 * for React components to prevent unnecessary re-renders
 */

import { useMemo, useCallback, useRef, useEffect, useState } from 'react'
import { debounce, throttle } from 'lodash'

// Generic memoization hook for expensive computations
export const useMemoizedValue = <T>(factory: () => T, deps: React.DependencyList) => {
  return useMemo(factory, deps)
}

// Debounced callback hook
export const useDebouncedCallback = <T extends (...args: any[]) => any>(
  callback: T,
  delay: number,
  deps: React.DependencyList = []
) => {
  const callbackRef = useRef(callback)
  callbackRef.current = callback

  return useMemo(
    () => debounce((...args: Parameters<T>) => callbackRef.current(...args), delay),
    [delay, ...deps]
  )
}

// Throttled callback hook
export const useThrottledCallback = <T extends (...args: any[]) => any>(
  callback: T,
  delay: number,
  deps: React.DependencyList = []
) => {
  const callbackRef = useRef(callback)
  callbackRef.current = callback

  return useMemo(
    () => throttle((...args: Parameters<T>) => callbackRef.current(...args), delay),
    [delay, ...deps]
  )
}

// Memoized array operations
export const useMemoizedArray = <T>(array: T[], keyFn?: (item: T) => string | number) => {
  return useMemo(() => {
    if (!keyFn) return array

    // Create a stable array with unique keys
    const seen = new Set()
    return array.filter(item => {
      const key = keyFn(item)
      if (seen.has(key)) return false
      seen.add(key)
      return true
    })
  }, [array, keyFn])
}

// Memoized filter function
export const useMemoizedFilter = <T>(
  items: T[],
  predicate: (item: T) => boolean,
  deps: React.DependencyList = []
) => {
  return useMemo(() => items.filter(predicate), [items, ...deps])
}

// Memoized sort function
export const useMemoizedSort = <T>(
  items: T[],
  compareFn: (a: T, b: T) => number,
  deps: React.DependencyList = []
) => {
  return useMemo(() => [...items].sort(compareFn), [items, compareFn, ...deps])
}

// Memoized search function
export const useMemoizedSearch = <T>(
  items: T[],
  searchTerm: string,
  searchFields: (keyof T)[],
  deps: React.DependencyList = []
) => {
  return useMemo(() => {
    if (!searchTerm.trim()) return items

    const term = searchTerm.toLowerCase()
    return items.filter(item =>
      searchFields.some(field => String(item[field]).toLowerCase().includes(term))
    )
  }, [items, searchTerm, searchFields, ...deps])
}

// Performance monitoring hook
export const usePerformanceMonitor = (componentName: string) => {
  const renderCount = useRef(0)
  const lastRenderTime = useRef(Date.now())

  useEffect(() => {
    renderCount.current++
    const now = Date.now()
    const timeSinceLastRender = now - lastRenderTime.current
    lastRenderTime.current = now

    if (process.env.NODE_ENV === 'development') {
      console.log(
        `🔍 ${componentName} render #${renderCount.current}, time since last: ${timeSinceLastRender}ms`
      )
    }
  })

  return {
    renderCount: renderCount.current,
    lastRenderTime: lastRenderTime.current,
  }
}

// Virtual scrolling helper
export const useVirtualScroll = (
  items: any[],
  itemHeight: number,
  containerHeight: number,
  overscan: number = 5
) => {
  const [scrollTop, setScrollTop] = useState(0)

  const visibleRange = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight)
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + overscan,
      items.length - 1
    )

    return {
      startIndex: Math.max(0, startIndex - overscan),
      endIndex,
    }
  }, [scrollTop, itemHeight, containerHeight, overscan, items.length])

  const visibleItems = useMemo(() => {
    return items.slice(visibleRange.startIndex, visibleRange.endIndex + 1)
  }, [items, visibleRange])

  const totalHeight = items.length * itemHeight

  const handleScroll = useCallback((e: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(e.currentTarget.scrollTop)
  }, [])

  return {
    visibleItems,
    totalHeight,
    startIndex: visibleRange.startIndex,
    endIndex: visibleRange.endIndex,
    handleScroll,
  }
}

// Optimized pagination hook
export const useOptimizedPagination = <T>(
  items: T[],
  itemsPerPage: number,
  deps: React.DependencyList = []
) => {
  const [currentPage, setCurrentPage] = useState(1)

  const paginatedItems = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    return items.slice(startIndex, endIndex)
  }, [items, currentPage, itemsPerPage, ...deps])

  const totalPages = useMemo(
    () => Math.ceil(items.length / itemsPerPage),
    [items.length, itemsPerPage]
  )

  const goToPage = useCallback(
    (page: number) => {
      if (page >= 1 && page <= totalPages) {
        setCurrentPage(page)
      }
    },
    [totalPages]
  )

  const nextPage = useCallback(() => {
    goToPage(currentPage + 1)
  }, [currentPage, goToPage])

  const prevPage = useCallback(() => {
    goToPage(currentPage - 1)
  }, [currentPage, goToPage])

  return {
    items: paginatedItems,
    currentPage,
    totalPages,
    goToPage,
    nextPage,
    prevPage,
    hasNextPage: currentPage < totalPages,
    hasPrevPage: currentPage > 1,
  }
}

// Memoized chart data preparation
export const useMemoizedChartData = (
  rawData: any[],
  dataTransform: (data: any[]) => any[],
  deps: React.DependencyList = []
) => {
  return useMemo(() => {
    return dataTransform(rawData)
  }, [rawData, dataTransform, ...deps])
}

// Optimized event handler
export const useOptimizedEventHandler = <T extends Event>(
  handler: (event: T) => void,
  options: {
    debounce?: number
    throttle?: number
    deps?: React.DependencyList
  } = {}
) => {
  const { debounce: debounceDelay, throttle: throttleDelay, deps = [] } = options

  if (debounceDelay) {
    return useDebouncedCallback(handler, debounceDelay, deps)
  }

  if (throttleDelay) {
    return useThrottledCallback(handler, throttleDelay, deps)
  }

  return useCallback(handler, deps)
}

// Component lazy loading with error boundary
export const useLazyComponent = <T extends React.ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>,
  deps: React.DependencyList = []
) => {
  const [component, setComponent] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    let cancelled = false

    const loadComponent = async () => {
      try {
        setLoading(true)
        setError(null)

        const module = await importFunc()

        if (!cancelled) {
          setComponent(module.default)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err : new Error('Failed to load component'))
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadComponent()

    return () => {
      cancelled = true
    }
  }, deps)

  return { component, loading, error }
}

export default {
  useMemoizedValue,
  useDebouncedCallback,
  useThrottledCallback,
  useMemoizedArray,
  useMemoizedFilter,
  useMemoizedSort,
  useMemoizedSearch,
  usePerformanceMonitor,
  useVirtualScroll,
  useOptimizedPagination,
  useMemoizedChartData,
  useOptimizedEventHandler,
  useLazyComponent,
}
