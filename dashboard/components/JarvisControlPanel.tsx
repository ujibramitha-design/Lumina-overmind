'use client'

import React, { useState, useEffect } from 'react'
import {
  Brain,
  Power,
  PowerOff,
  Activity,
  Zap,
  Shield,
  AlertTriangle,
  CheckCircle,
  Settings,
  Database,
  Cpu,
  HardDrive,
  Wifi,
  WifiOff,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'

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

interface JarvisAnalytics {
  usage_stats: {
    is_active: boolean
    last_activity: string
    total_commands: number
    voice_commands: number
    system_commands: number
    chat_sessions: number
    errors: number
  }
  performance_metrics: {
    avg_response_time: number
    success_rate: number
    error_rate: number
  }
  popular_commands: Array<{
    command: string
    usage: number
  }>
}

export default function JarvisControlPanel() {
  const [jarvisStatus, setJarvisStatus] = useState<JarvisStatus | null>(null)
  const [analytics, setAnalytics] = useState<JarvisAnalytics | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    fetchJarvisStatus()
    fetchAnalytics()
    const interval = setInterval(() => {
      fetchJarvisStatus()
      fetchAnalytics()
    }, 10000) // Update every 10 seconds
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

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/jarvis/analytics')
      if (response.ok) {
        const data = await response.json()
        setAnalytics(data)
      }
    } catch (error) {
      console.error('Error fetching J.A.R.V.I.S. analytics:', error)
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

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case 'offline':
        return <WifiOff className="h-4 w-4 text-red-400" />
      default:
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
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

  return (
    <div className="space-y-6">
      {/* Main Control Card */}
      <Card className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 border-emerald-500/50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Brain className="h-8 w-8 text-emerald-400" />
              <div>
                <CardTitle className="text-xl text-white">J.A.R.V.I.S. Control</CardTitle>
                <p className="text-sm text-gray-400">Super Admin Voice Assistant</p>
              </div>
            </div>

            {/* Main Power Toggle */}
            <Button
              onClick={toggleJarvis}
              disabled={isLoading}
              size="lg"
              className={`${jarvisStatus?.is_active ? 'bg-red-600 hover:bg-red-700' : 'bg-emerald-600 hover:bg-emerald-700'} text-white px-6`}
            >
              {isLoading ? (
                <Activity className="h-5 w-5 animate-spin" />
              ) : jarvisStatus?.is_active ? (
                <>
                  <PowerOff className="h-5 w-5 mr-2" />
                  Deactivate
                </>
              ) : (
                <>
                  <Power className="h-5 w-5 mr-2" />
                  Activate
                </>
              )}
            </Button>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Status Overview */}
          {jarvisStatus && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* System Status */}
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="h-4 w-4 text-emerald-400" />
                  <span className="text-sm font-medium text-white">System Status</span>
                </div>
                <Badge className={getStatusColor(jarvisStatus.status)}>{jarvisStatus.status}</Badge>
                <p className="text-xs text-gray-400 mt-1">
                  Last activity: {new Date(jarvisStatus.last_activity).toLocaleTimeString()}
                </p>
              </div>

              {/* AI Provider */}
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="h-4 w-4 text-blue-400" />
                  <span className="text-sm font-medium text-white">AI Provider</span>
                </div>
                <Badge className={getProviderColor(jarvisStatus.provider)}>{jarvisStatus.provider}</Badge>
                <p className="text-xs text-gray-400 mt-1">{jarvisStatus.capabilities.length} capabilities</p>
              </div>

              {/* Capabilities */}
              <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="h-4 w-4 text-purple-400" />
                  <span className="text-sm font-medium text-white">Capabilities</span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {jarvisStatus.capabilities.slice(0, 3).map((cap, idx) => (
                    <Badge key={idx} variant="outline" className="text-xs">
                      {cap}
                    </Badge>
                  ))}
                  {jarvisStatus.capabilities.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{jarvisStatus.capabilities.length - 3}
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* System Health */}
          {jarvisStatus && (
            <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
              <h4 className="text-white font-medium mb-3 flex items-center gap-2">
                <Settings className="h-4 w-4" />
                System Health
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  {getHealthIcon(jarvisStatus.system_health.database_status)}
                  <div>
                    <p className="text-xs text-gray-400">Database</p>
                    <p className="text-sm text-white">{jarvisStatus.system_health.database_status}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {getHealthIcon(jarvisStatus.system_health.api_status)}
                  <div>
                    <p className="text-xs text-gray-400">API</p>
                    <p className="text-sm text-white">{jarvisStatus.system_health.api_status}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Cpu className="h-4 w-4 text-blue-400" />
                  <div>
                    <p className="text-xs text-gray-400">CPU</p>
                    <p className="text-sm text-white">{jarvisStatus.system_health.cpu_usage}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <HardDrive className="h-4 w-4 text-green-400" />
                  <div>
                    <p className="text-xs text-gray-400">Memory</p>
                    <p className="text-sm text-white">{jarvisStatus.system_health.memory_usage}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Analytics Card */}
      {analytics && (
        <Card className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 border-blue-500/50">
          <CardHeader>
            <CardTitle className="text-lg text-white flex items-center gap-2">
              <Activity className="h-5 w-5 text-blue-400" />
              Usage Analytics
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4">
            {/* Usage Stats */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-emerald-400">{analytics.usage_stats.total_commands}</p>
                <p className="text-xs text-gray-400">Total Commands</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-400">{analytics.usage_stats.chat_sessions}</p>
                <p className="text-xs text-gray-400">Chat Sessions</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-400">{analytics.usage_stats.voice_commands}</p>
                <p className="text-xs text-gray-400">Voice Commands</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-orange-400">{analytics.usage_stats.system_commands}</p>
                <p className="text-xs text-gray-400">System Commands</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-400">{analytics.performance_metrics.success_rate}%</p>
                <p className="text-xs text-gray-400">Success Rate</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-400">{analytics.usage_stats.errors}</p>
                <p className="text-xs text-gray-400">Errors</p>
              </div>
            </div>

            {/* Popular Commands */}
            <div className="bg-slate-800/30 rounded-lg p-4 border border-slate-700">
              <h4 className="text-white font-medium mb-3">Popular Commands</h4>
              <div className="space-y-2">
                {analytics.popular_commands.map((cmd, idx) => (
                  <div key={idx} className="flex items-center justify-between">
                    <span className="text-sm text-gray-300">{cmd.command}</span>
                    <div className="flex items-center gap-2">
                      <div className="h-2 bg-slate-700 rounded-full w-24">
                        <div
                          className="h-2 bg-emerald-400 rounded-full"
                          style={{ width: `${(cmd.usage / analytics.popular_commands[0].usage) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-gray-400 w-8 text-right">{cmd.usage}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
