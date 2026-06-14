import { useState, useCallback, useRef } from 'react'

interface UseApiRetryOptions {
  maxRetries?: number
  retryDelay?: number
  exponentialBackoff?: boolean
}

interface ApiRetryState {
  isLoading: boolean
  error: string | null
  retryCount: number
}

export const useApiRetry = <T = any>(
  apiCall: () => Promise<T>,
  options: UseApiRetryOptions = {}
) => {
  const { maxRetries = 3, retryDelay = 1000, exponentialBackoff = true } = options

  const [state, setState] = useState<ApiRetryState>({
    isLoading: false,
    error: null,
    retryCount: 0,
  })

  const abortControllerRef = useRef<AbortController | null>(null)

  const execute = useCallback(async (): Promise<T | null> => {
    // Cancel any existing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    abortControllerRef.current = new AbortController()

    setState(prev => ({
      ...prev,
      isLoading: true,
      error: null,
    }))

    let currentRetryCount = 0

    while (currentRetryCount <= maxRetries) {
      try {
        const result = await apiCall()

        setState({
          isLoading: false,
          error: null,
          retryCount: currentRetryCount,
        })

        return result
      } catch (error) {
        currentRetryCount++

        // Check if we should retry
        if (currentRetryCount > maxRetries) {
          const errorMessage = error instanceof Error ? error.message : 'Unknown error'

          setState({
            isLoading: false,
            error: `Failed after ${maxRetries} attempts: ${errorMessage}`,
            retryCount: currentRetryCount - 1,
          })

          return null
        }

        // Calculate delay for next retry
        let delay = retryDelay
        if (exponentialBackoff) {
          delay = retryDelay * Math.pow(2, currentRetryCount - 1)
        }

        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, delay))

        console.warn(`API call failed, retrying (${currentRetryCount}/${maxRetries}):`, error)
      }
    }

    return null
  }, [apiCall, maxRetries, retryDelay, exponentialBackoff])

  const reset = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }

    setState({
      isLoading: false,
      error: null,
      retryCount: 0,
    })
  }, [])

  const cancel = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }

    setState(prev => ({
      ...prev,
      isLoading: false,
    }))
  }, [])

  return {
    execute,
    reset,
    cancel,
    ...state,
  }
}

// Specific hook for API calls with timeout
export const useApiWithTimeout = <T = any>(
  apiCall: () => Promise<T>,
  timeoutMs: number = 10000,
  retryOptions: UseApiRetryOptions = {}
) => {
  const apiCallWithTimeout = useCallback(async (): Promise<T> => {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error(`Request timeout after ${timeoutMs}ms`))
      }, timeoutMs)

      apiCall()
        .then(result => {
          clearTimeout(timeout)
          resolve(result)
        })
        .catch(error => {
          clearTimeout(timeout)
          reject(error)
        })
    })
  }, [apiCall, timeoutMs])

  return useApiRetry(apiCallWithTimeout, retryOptions)
}

// Hook for fetching runners status with retry logic
export const useRunnersApi = () => {
  const fetchRunners = useCallback(async () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const response = await fetch(`${apiUrl}/api/runners`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (!result.success) {
      throw new Error(result.detail || 'API request failed')
    }

    return result.data
  }, [])

  return useApiWithTimeout(fetchRunners, 5000, {
    maxRetries: 3,
    retryDelay: 1000,
    exponentialBackoff: true,
  })
}

// Hook for runner control API calls
export const useRunnerControlApi = () => {
  const controlRunner = useCallback(async (runnerId: string, action: 'start' | 'stop') => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const endpoint = `${apiUrl}/api/runners/${runnerId}/${action}`

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    const result = await response.json()

    if (!result.success) {
      throw new Error(result.detail || 'Runner control failed')
    }

    return result.data
  }, [])

  // @ts-ignore - Function signature mismatch
  return useApiWithTimeout(controlRunner as any, 10000, {
    maxRetries: 2,
    retryDelay: 500,
    exponentialBackoff: false,
  })
}
