'use client'

import React, { useState, useEffect, useRef } from 'react'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Shield, AlertTriangle, CheckCircle, Info, Activity, Wifi, WifiOff } from 'lucide-react'

interface LogEntry {
  id: string
  timestamp: string
  level: 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS'
  category: string
  message: string
  source: string
}

export function TerminalLogs() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>(
    'connecting'
  )
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollElement = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]')
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight
      }
    }
  }, [logs])

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      setConnectionStatus('connecting')

      try {
        const ws = new WebSocket('ws://localhost:8000/api/ws/logs')
        wsRef.current = ws

        ws.onopen = () => {
          setIsConnected(true)
          setConnectionStatus('connected')
          console.log('WebSocket connected to logs endpoint')
        }

        ws.onmessage = event => {
          try {
            const logEntry: LogEntry = JSON.parse(event.data)
            setLogs(prev => [logEntry, ...prev].slice(0, 100)) // Keep last 100 logs
          } catch (error) {
            console.error('Error parsing log message:', error)
          }
        }

        ws.onclose = () => {
          setIsConnected(false)
          setConnectionStatus('disconnected')
          console.log('WebSocket disconnected')

          // Attempt to reconnect after 3 seconds
          setTimeout(() => {
            if (!wsRef.current || wsRef.current.readyState === WebSocket.CLOSED) {
              connectWebSocket()
            }
          }, 3000)
        }

        ws.onerror = error => {
          console.error('WebSocket error:', error)
          setConnectionStatus('error')
          setIsConnected(false)
        }
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error)
        setConnectionStatus('error')
        setIsConnected(false)
      }
    }

    connectWebSocket()

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
    }
  }, [])

  const getLogColor = (level: LogEntry['level']) => {
    switch (level) {
      case 'INFO':
        return 'text-zinc-400'
      case 'SUCCESS':
        return 'text-emerald-500'
      case 'WARNING':
        return 'text-yellow-500'
      case 'ERROR':
        return 'text-red-500'
      default:
        return 'text-zinc-400'
    }
  }

  const getLogIcon = (level: LogEntry['level']) => {
    switch (level) {
      case 'INFO':
        return <Info className="h-3 w-3" />
      case 'SUCCESS':
        return <CheckCircle className="h-3 w-3" />
      case 'WARNING':
        return <AlertTriangle className="h-3 w-3" />
      case 'ERROR':
        return <Shield className="h-3 w-3" />
      default:
        return <Activity className="h-3 w-3" />
    }
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  }

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connecting':
        return 'text-yellow-500'
      case 'connected':
        return 'text-emerald-500'
      case 'disconnected':
        return 'text-zinc-500'
      case 'error':
        return 'text-red-500'
      default:
        return 'text-zinc-500'
    }
  }

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connecting':
        return <Wifi className="h-3 w-3 animate-pulse" />
      case 'connected':
        return <Wifi className="h-3 w-3" />
      case 'disconnected':
        return <WifiOff className="h-3 w-3" />
      case 'error':
        return <AlertTriangle className="h-3 w-3" />
      default:
        return <WifiOff className="h-3 w-3" />
    }
  }

  return (
    <div className="bg-black border-2 border-zinc-800 rounded-lg p-4 h-full">
      {/* Terminal Header */}
      <div className="flex items-center justify-between mb-4 border-b border-zinc-800 pb-3">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="ml-3 text-zinc-400 font-mono text-sm">terminal://governance-system</span>
        </div>
        <div className="flex items-center gap-4">
          <div className={`flex items-center gap-1 text-xs ${getConnectionStatusColor()}`}>
            {getConnectionStatusIcon()}
            <span>{connectionStatus.toUpperCase()}</span>
          </div>
          <div className="text-zinc-500 font-mono text-xs">{logs.length} entries</div>
        </div>
      </div>

      {/* Terminal Content */}
      <ScrollArea className="h-[400px] w-full" ref={scrollAreaRef}>
        <div className="font-mono text-sm space-y-1">
          {logs.map((log: LogEntry) => (
            <div
              key={log.id}
              className="flex items-start gap-3 py-1 px-2 hover:bg-zinc-900/50 rounded transition-colors"
            >
              {/* Timestamp */}
              <span className="text-zinc-600 text-xs flex-shrink-0">{formatTimestamp(log.timestamp)}</span>

              {/* Icon */}
              <span className={`flex-shrink-0 ${getLogColor(log.level)}`}>{getLogIcon(log.level)}</span>

              {/* Message */}
              <span className={`${getLogColor(log.level)} break-words`}>{log.message}</span>
            </div>
          ))}

          {logs.length === 0 && (
            <div className="text-zinc-600 text-center py-8">
              {connectionStatus === 'connecting'
                ? '🔌 Connecting to log stream...'
                : connectionStatus === 'disconnected' || connectionStatus === 'error'
                  ? '🔌 Disconnected from log stream'
                  : '🔌 Waiting for logs...'}
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Terminal Footer */}
      <div className="mt-4 pt-3 border-t border-zinc-800">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-xs text-zinc-500">
            <span className={`flex items-center gap-1 ${getConnectionStatusColor()}`}>
              <div
                className={`w-2 h-2 ${connectionStatus === 'connected' ? 'bg-emerald-500' : 'bg-zinc-500'} rounded-full ${connectionStatus === 'connected' ? 'animate-pulse' : ''}`}
              ></div>
              {connectionStatus === 'connected' ? 'System Active' : 'System Offline'}
            </span>
            <span>CPU: 42%</span>
            <span>Memory: 8.2GB</span>
          </div>
          <div className="text-zinc-600 font-mono text-xs">$ ./governance --monitor --realtime</div>
        </div>
      </div>
    </div>
  )
}
