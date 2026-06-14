'use client'

import React, { useState, useEffect } from 'react'
import { Brain, Activity, Wifi, WifiOff, Power, PowerOff } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { useToast } from '@/hooks/use-toast'

interface JarvisStatusWidgetProps {
  className?: string
}

interface JarvisStatus {
  status: string
  provider: string
  capabilities: string[]
  is_active: boolean
  last_activity: string
  system_health: {
    database_status: string
    api_status: string
    memory_usage: string
    cpu_usage: string
    last_error: string | null
  }
}

export default function JarvisStatusWidget({ className }: JarvisStatusWidgetProps) {
  const [jarvisStatus, setJarvisStatus] = useState<JarvisStatus | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    fetchJarvisStatus()
    const interval = setInterval(fetchJarvisStatus, 15000) // Update every 15 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchJarvisStatus = async () => {
    try {
      const response = await fetch('/api/jarvis/status')
      if (response.ok) {
        const status = await response.json()
        setJarvisStatus(status)
      }
    } catch (error) {
      console.error('Error fetching J.A.R.V.I.S. status:', error)
    }
  }

  const toggleJarvis = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/jarvis/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })

      if (response.ok) {
        const result = await response.json()
        setJarvisStatus(prev => (prev ? { ...prev, is_active: result.is_active } : null))

        toast({
          title: 'J.A.R.V.I.S. Status Changed',
          description: result.message,
        })
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to toggle J.A.R.V.I.S. status',
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'inactive':
        return 'bg-red-500/20 text-red-400 border-red-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const getProviderColor = (provider: string) => {
    switch (provider) {
      case 'gemini':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30'
      case 'openai':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <Wifi className="h-3 w-3 text-green-400" />
      case 'offline':
        return <WifiOff className="h-3 w-3 text-red-400" />
      default:
        return <Activity className="h-3 w-3 text-yellow-400" />
    }
  }

  if (!jarvisStatus) {
    return (
      <Card className={`bg-slate-900/50 border-slate-700 ${className}`}>
        <CardContent className="p-4">
          <div className="flex items-center gap-3">
            <Brain className="h-5 w-5 text-gray-400 animate-pulse" />
            <div className="text-sm text-gray-400">Loading J.A.R.V.I.S. status...</div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={`bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900 border-emerald-500/50 ${className}`}>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-emerald-400" />
            <span className="text-white font-medium">J.A.R.V.I.S.</span>
            {jarvisStatus.is_active && <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>}
          </div>

          <Button
            onClick={toggleJarvis}
            disabled={isLoading}
            size="sm"
            variant="ghost"
            className={`${jarvisStatus.is_active ? 'text-red-400 hover:text-red-300' : 'text-green-400 hover:text-green-300'}`}
          >
            {isLoading ? (
              <Activity className="h-4 w-4 animate-spin" />
            ) : jarvisStatus.is_active ? (
              <PowerOff className="h-4 w-4" />
            ) : (
              <Power className="h-4 w-4" />
            )}
          </Button>
        </div>

        <div className="space-y-2">
          {/* Status Row */}
          <div className="flex items-center justify-between">
            <Badge className={getStatusColor(jarvisStatus.status)} variant="outline">
              {jarvisStatus.status}
            </Badge>
            <Badge className={getProviderColor(jarvisStatus.provider)} variant="outline">
              {jarvisStatus.provider}
            </Badge>
          </div>

          {/* Health Indicators */}
          <div className="flex items-center gap-3 text-xs">
            <div className="flex items-center gap-1">
              {getHealthIcon(jarvisStatus.system_health.database_status)}
              <span className="text-gray-400">DB</span>
            </div>
            <div className="flex items-center gap-1">
              {getHealthIcon(jarvisStatus.system_health.api_status)}
              <span className="text-gray-400">API</span>
            </div>
            <div className="flex items-center gap-1">
              <Activity className="h-3 w-3 text-blue-400" />
              <span className="text-gray-400">CPU: {jarvisStatus.system_health.cpu_usage}</span>
            </div>
            <div className="flex items-center gap-1">
              <Activity className="h-3 w-3 text-green-400" />
              <span className="text-gray-400">MEM: {jarvisStatus.system_health.memory_usage}</span>
            </div>
          </div>

          {/* Last Activity */}
          <div className="text-xs text-gray-400">
            Last activity: {new Date(jarvisStatus.last_activity).toLocaleTimeString()}
          </div>

          {/* Capabilities */}
          <div className="flex flex-wrap gap-1">
            {jarvisStatus.capabilities.slice(0, 2).map((cap, idx) => (
              <Badge key={idx} variant="outline" className="text-xs">
                {cap}
              </Badge>
            ))}
            {jarvisStatus.capabilities.length > 2 && (
              <Badge variant="outline" className="text-xs">
                +{jarvisStatus.capabilities.length - 2}
              </Badge>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
