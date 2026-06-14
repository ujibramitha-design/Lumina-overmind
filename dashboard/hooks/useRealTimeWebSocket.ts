/**
 * LUMINA OVERMIND SYSTEM - Real-Time WebSocket Hook
 *
 * Replaces polling with persistent WebSocket connections for real-time updates
 * Provides automatic reconnection, backoff, and state management
 */

import { useEffect, useRef, useState, useCallback } from 'react'
import { useAppStore } from '@/lib/store'

interface WebSocketMessage {
  type: 'system_status' | 'runner_update' | 'notification' | 'error'
  data: any
  timestamp: string
}

interface UseWebSocketOptions {
  reconnectInterval?: number
  maxRetries?: number
  enableReconnect?: boolean
}

interface WebSocketState {
  isConnected: boolean
  isConnecting: boolean
  error: string | null
  lastMessage: WebSocketMessage | null
  retryCount: number
}

export const useRealTimeWebSocket = (options: UseWebSocketOptions = {}) => {
  const { reconnectInterval = 5000, maxRetries = 5, enableReconnect = true } = options

  const [state, setState] = useState<WebSocketState>({
    isConnected: false,
    isConnecting: false,
    error: null,
    lastMessage: null,
    retryCount: 0,
  })

  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const { setRunners, setSystemMetrics, setApiError } = useAppStore()

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    setState(prev => ({ ...prev, isConnecting: true, error: null }))

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws'
    const ws = new WebSocket(`${wsUrl}/system`)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('🔌 WebSocket connected')
      setState(prev => ({
        ...prev,
        isConnected: true,
        isConnecting: false,
        error: null,
        retryCount: 0,
      }))

      // Request initial status
      ws.send(
        JSON.stringify({
          type: 'subscribe',
          channels: ['system_status', 'runner_updates', 'notifications'],
        })
      )
    }

    ws.onmessage = event => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)

        setState(prev => ({ ...prev, lastMessage: message }))

        // Handle different message types
        switch (message.type) {
          case 'system_status':
            if (message.data.metrics) {
              setSystemMetrics(message.data.metrics)
            }
            break

          case 'runner_update':
            if (message.data.runners) {
              setRunners(message.data.runners)
            }
            break

          case 'notification':
            // Handle notifications
            console.log('🔔 Notification:', message.data)
            break

          case 'error':
            setApiError(message.data.message)
            break
        }
      } catch (error) {
        console.error('❌ Error parsing WebSocket message:', error)
      }
    }

    ws.onclose = event => {
      console.log('🔌 WebSocket disconnected:', event.code, event.reason)

      setState(prev => ({
        ...prev,
        isConnected: false,
        isConnecting: false,
      }))

      // Auto-reconnect if enabled and not manually closed
      if (enableReconnect && event.code !== 1000 && state.retryCount < maxRetries) {
        const nextRetryCount = state.retryCount + 1
        const backoffDelay = reconnectInterval * Math.pow(2, nextRetryCount - 1)

        console.log(
          `🔄 Reconnecting in ${backoffDelay}ms (attempt ${nextRetryCount}/${maxRetries})`
        )

        reconnectTimeoutRef.current = setTimeout(() => {
          setState(prev => ({ ...prev, retryCount: nextRetryCount }))
          connect()
        }, backoffDelay)
      } else if (state.retryCount >= maxRetries) {
        setState(prev => ({
          ...prev,
          error: 'Max reconnection attempts reached',
        }))
      }
    }

    ws.onerror = error => {
      console.error('❌ WebSocket error:', error)
      setState(prev => ({
        ...prev,
        error: 'WebSocket connection error',
      }))
    }
  }, [
    enableReconnect,
    maxRetries,
    reconnectInterval,
    state.retryCount,
    setRunners,
    setSystemMetrics,
    setApiError,
  ])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }

    if (wsRef.current) {
      wsRef.current.close(1000, 'Manual disconnect')
      wsRef.current = null
    }

    setState(prev => ({
      ...prev,
      isConnected: false,
      isConnecting: false,
      error: null,
      retryCount: 0,
    }))
  }, [])

  const sendMessage = useCallback((message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message))
      return true
    } else {
      console.warn('⚠️ Cannot send message - WebSocket not connected')
      return false
    }
  }, [])

  // Auto-connect on mount
  useEffect(() => {
    connect()

    return () => {
      disconnect()
    }
  }, [connect, disconnect])

  return {
    ...state,
    connect,
    disconnect,
    sendMessage,
  }
}

// Hook for specific data subscriptions
export const useSystemStatusWebSocket = () => {
  const { isConnected, lastMessage, sendMessage, ...rest } = useRealTimeWebSocket()

  const requestStatusUpdate = useCallback(() => {
    sendMessage({
      type: 'request',
      data: { endpoint: 'system_status' },
    })
  }, [sendMessage])

  return {
    isConnected,
    lastMessage,
    requestStatusUpdate,
    sendMessage,
    ...rest,
  }
}

export default useRealTimeWebSocket
