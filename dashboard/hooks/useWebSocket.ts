'use client'

import { useEffect, useRef, useState } from 'react'
import { io, Socket } from 'socket.io-client'

interface WebSocketMessage {
  type: 'runners_status' | 'system_status' | 'runner_update' | 'error'
  data: any
  timestamp: string
}

interface UseWebSocketReturn {
  socket: Socket | null
  isConnected: boolean
  error: string | null
  lastMessage: WebSocketMessage | null
  sendMessage: (type: string, data: any) => void
}

export function useWebSocket(serverUrl?: string): UseWebSocketReturn {
  const defaultUrl = process.env.NEXT_PUBLIC_API_URL || ''
  const finalUrl =
    serverUrl || defaultUrl || (typeof window !== 'undefined' ? window.location.origin : '')
  const [socket, setSocket] = useState<Socket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const maxReconnectAttempts = 5
  const reconnectAttempts = useRef(0)

  const connect = () => {
    try {
      const newSocket = io(finalUrl, {
        transports: ['websocket', 'polling'],
        timeout: 10000,
        reconnection: true,
        reconnectionAttempts: maxReconnectAttempts,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
      })

      newSocket.on('connect', () => {
        console.log('✅ WebSocket connected')
        setIsConnected(true)
        setError(null)
        reconnectAttempts.current = 0

        // Request initial data
        newSocket.emit('get_runners_status')
        newSocket.emit('get_system_status')
      })

      newSocket.on('disconnect', reason => {
        console.log('❌ WebSocket disconnected:', reason)
        setIsConnected(false)

        if (reason === 'io server disconnect') {
          // Server initiated disconnect, don't reconnect automatically
          return
        }
      })

      newSocket.on('connect_error', err => {
        console.error('❌ WebSocket connection error:', err)
        setError(err.message)
        reconnectAttempts.current++

        if (reconnectAttempts.current >= maxReconnectAttempts) {
          console.error('❌ Max reconnect attempts reached')
          setError('Connection failed. Please refresh the page.')
        }
      })

      newSocket.on('runners_status', data => {
        console.log('📊 Received runners status:', data)
        setLastMessage({
          type: 'runners_status',
          data,
          timestamp: new Date().toISOString(),
        })
      })

      newSocket.on('system_status', data => {
        console.log('🖥️ Received system status:', data)
        setLastMessage({
          type: 'system_status',
          data,
          timestamp: new Date().toISOString(),
        })
      })

      newSocket.on('runner_update', data => {
        console.log('🔄 Received runner update:', data)
        setLastMessage({
          type: 'runner_update',
          data,
          timestamp: new Date().toISOString(),
        })
      })

      newSocket.on('error', data => {
        console.error('❌ WebSocket error:', data)
        setLastMessage({
          type: 'error',
          data,
          timestamp: new Date().toISOString(),
        })
      })

      setSocket(newSocket)
    } catch (err) {
      console.error('❌ Failed to create WebSocket connection:', err)
      setError('Failed to initialize WebSocket connection')
    }
  }

  const disconnect = () => {
    if (socket) {
      socket.disconnect()
      setSocket(null)
      setIsConnected(false)
    }

    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
  }

  const sendMessage = (type: string, data: any) => {
    if (socket && isConnected) {
      socket.emit(type, data)
    } else {
      console.warn('⚠️ Cannot send message - WebSocket not connected')
    }
  }

  useEffect(() => {
    connect()

    return () => {
      disconnect()
    }
  }, [serverUrl])

  return {
    socket,
    isConnected,
    error,
    lastMessage,
    sendMessage,
  }
}
