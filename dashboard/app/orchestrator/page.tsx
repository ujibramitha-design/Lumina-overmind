'use client'

import React, { useState, useEffect } from 'react'
import {
  Server,
  Cpu,
  Activity,
  Zap,
  Globe,
  Shield,
  TrendingUp,
  Users,
  Home,
  CheckCircle,
  AlertCircle,
  Loader2,
  Play,
  Square,
  Radio,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { useWebSocket } from '@/hooks/useWebSocket'

interface RunnerCard {
  id: string
  runnerId: string
  name: string
  description: string
  icon: React.ElementType
  status: 'running' | 'idle'
  lastScan: string
  systemLoad: number
  successRate: number
  pid?: number
  cpuPercent?: number
  memoryPercent?: number
}

interface ApiResponse {
  success: boolean
  data: {
    runners: Record<
      string,
      {
        status: string
        pid?: number
        cpu_percent?: number
        memory_percent?: number
        start_time?: string
        message?: string
      }
    >
    total_running: number
    timestamp: string
  }
  timestamp: string
}

interface SystemStatusResponse {
  success: boolean
  system_status: {
    lumina_os: string
    database: string
    runners: string
    uptime: string
    memory: string
    cpu: string
    disk: string
    is_hunting: boolean
    hunt_duration: string
    last_status_check: string
    timestamp: string
  }
  timestamp: string
}

interface HunterResponse {
  success: boolean
  is_hunting: boolean
  hunt_start_time?: string
  hunt_end_time?: string
  hunt_duration?: string
  telegram_notification?: boolean
  message: string
  timestamp: string
}

export default function SystemOrchestrator() {
  const { toast } = useToast()
  const { isConnected, error: wsError, lastMessage, sendMessage } = useWebSocket()

  const [systemMetrics, setSystemMetrics] = useState({
    systemLoad: 45,
    activeRunners: 6,
    totalRunners: 12,
    apiRateLimit: 'Normal',
  })

  const [systemStatus, setSystemStatus] = useState({
    lumina_os: 'ONLINE',
    database: 'CONNECTED',
    runners: 'ACTIVE',
    uptime: '2h 15m 30s',
    memory: '45.2%',
    cpu: '12.8%',
    disk: '67.3%',
    is_hunting: false,
    hunt_duration: 'Not active',
    last_status_check: new Date().toISOString(),
  })

  const [isHunting, setIsHunting] = useState(false)
  const [systemControlLoading, setSystemControlLoading] = useState(false)
  const [systemError, setSystemError] = useState<string | null>(null)

  const [runners, setRunners] = useState<RunnerCard[]>([
    {
      id: 'lead-gen',
      runnerId: 'lead_generation',
      name: 'Lead Generation Engine',
      description: 'Multi-engine lead acquisition and validation system',
      icon: Users,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 94.2,
    },
    {
      id: 'banten-intel',
      runnerId: 'banten_government',
      name: 'Banten Government Intel',
      description: 'Government office mapping and PNS/P3K market analysis',
      icon: Shield,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 89.7,
    },
    {
      id: 'ride-hailing',
      runnerId: 'ride_hailing',
      name: 'Ride Hailing Intelligence',
      description: 'Transportation pattern analysis and market insights',
      icon: Globe,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 91.3,
    },
    {
      id: 'property-scraper',
      runnerId: 'property_scraper',
      name: 'Property Market Scraper',
      description: 'Real estate data extraction and price monitoring',
      icon: Home,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 96.8,
    },
    {
      id: 'social-proof',
      runnerId: 'social_verifier',
      name: 'Social Proof Verifier',
      description: 'Social media sentiment and credibility analysis',
      icon: CheckCircle,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 87.4,
    },
    {
      id: 'behavioral-tester',
      runnerId: 'behavioral_tester',
      name: 'Behavioral Velocity Tester',
      description: 'User behavior patterns and conversion velocity tracking',
      icon: TrendingUp,
      status: 'idle',
      lastScan: 'Last scan 1 hour ago',
      systemLoad: 0,
      successRate: 92.1,
    },
  ])

  const [loadingStates, setLoadingStates] = useState<Record<string, boolean>>({})
  const [apiError, setApiError] = useState<string | null>(null)
  const [lastSync, setLastSync] = useState<Date>(new Date())

  // System Control API Functions
  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/api/system-control/status')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: SystemStatusResponse = await response.json()

      if (data.success) {
        setSystemStatus(data.system_status)
        setIsHunting(data.system_status.is_hunting)
        setSystemError(null)
      }
    } catch (error) {
      console.error('Failed to fetch system status:', error)
      setSystemError('Failed to connect to system control API')
    }
  }

  const startHunter = async () => {
    if (isHunting) {
      toast({
        title: 'Hunter Already Active',
        description: 'Hunter protocol is already running',
        variant: 'destructive',
      })
      return
    }

    setSystemControlLoading(true)
    try {
      const response = await fetch('/api/system-control/start-hunter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result: HunterResponse = await response.json()

      if (result.success) {
        setIsHunting(true)
        setSystemStatus(prev => ({
          ...prev,
          is_hunting: true,
          hunt_duration: result.hunt_duration || 'Starting...',
        }))

        toast({
          title: 'Hunter Protocol Initiated',
          description: result.message,
          variant: 'default',
        })

        // Refresh system status
        await fetchSystemStatus()
      } else {
        throw new Error(result.message || 'Failed to start hunter')
      }
    } catch (error) {
      console.error('Failed to start hunter:', error)
      toast({
        title: 'Failed to Start Hunter',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    } finally {
      setSystemControlLoading(false)
    }
  }

  const stopHunter = async () => {
    if (!isHunting) {
      toast({
        title: 'Hunter Not Active',
        description: 'Hunter protocol is not currently running',
        variant: 'destructive',
      })
      return
    }

    setSystemControlLoading(true)
    try {
      const response = await fetch('/api/system-control/stop-hunter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result: HunterResponse = await response.json()

      if (result.success) {
        setIsHunting(false)
        setSystemStatus(prev => ({
          ...prev,
          is_hunting: false,
          hunt_duration: 'Not active',
        }))

        toast({
          title: 'Hunter Protocol Aborted',
          description: result.message,
          variant: 'default',
        })

        // Refresh system status
        await fetchSystemStatus()
      } else {
        throw new Error(result.message || 'Failed to stop hunter')
      }
    } catch (error) {
      console.error('Failed to stop hunter:', error)
      toast({
        title: 'Failed to Stop Hunter',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    } finally {
      setSystemControlLoading(false)
    }
  }

  const emergencyStopAll = async () => {
    setSystemControlLoading(true)
    try {
      const response = await fetch('/api/system-control/emergency-stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()

      if (result.success) {
        setIsHunting(false)
        setSystemStatus(prev => ({
          ...prev,
          is_hunting: false,
          hunt_duration: 'Not active',
        }))

        toast({
          title: 'Emergency Stop Activated',
          description: result.message,
          variant: 'destructive',
        })

        // Refresh all status
        await fetchSystemStatus()
        await fetchRunnersStatus()
      } else {
        throw new Error(result.message || 'Failed to execute emergency stop')
      }
    } catch (error) {
      console.error('Failed to execute emergency stop:', error)
      toast({
        title: 'Emergency Stop Failed',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    } finally {
      setSystemControlLoading(false)
    }
  }

  // Fetch runners status from API
  const fetchRunnersStatus = async () => {
    try {
      const response = await fetch('/api/runners')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const apiResponse: ApiResponse = await response.json()

      if (apiResponse.success) {
        const runnersData = apiResponse.data.runners

        setRunners(prev =>
          prev.map(runner => {
            const runnerStatus = runnersData[runner.runnerId]
            const isRunning = runnerStatus?.status === 'Running'

            return {
              ...runner,
              status: isRunning ? 'running' : 'idle',
              pid: runnerStatus?.pid,
              cpuPercent: runnerStatus?.cpu_percent,
              memoryPercent: runnerStatus?.memory_percent,
              systemLoad: runnerStatus?.cpu_percent ? Math.round(runnerStatus.cpu_percent) : 0,
              lastScan: isRunning ? 'Last scan 1 min ago' : 'Last scan 1 hour ago',
            }
          })
        )

        // Update system metrics
        const activeCount = apiResponse.data.total_running
        setSystemMetrics(prev => ({
          ...prev,
          activeRunners: activeCount,
          totalRunners: 6,
        }))

        setLastSync(new Date())
        setApiError(null)
      }
    } catch (error) {
      console.error('Failed to fetch runners status:', error)
      setApiError('Failed to connect to API server')
    }
  }

  // WebSocket message handling
  useEffect(() => {
    if (!lastMessage) return

    switch (lastMessage.type) {
      case 'runners_status':
        const runnersData = lastMessage.data.data || lastMessage.data
        if (runnersData.runners) {
          setRunners(prev =>
            prev.map(runner => {
              const runnerStatus = runnersData.runners[runner.runnerId]
              const isRunning = runnerStatus?.status === 'running'

              return {
                ...runner,
                status: isRunning ? 'running' : 'idle',
                task_id: runnerStatus?.task_id,
                cpuPercent: runnerStatus?.cpu_percent,
                memoryPercent: runnerStatus?.memory_percent,
                systemLoad: runnerStatus?.cpu_percent ? Math.round(runnerStatus.cpu_percent) : 0,
                lastScan: isRunning ? 'Last scan 1 min ago' : 'Last scan 1 hour ago',
              }
            })
          )

          // Update system metrics
          const activeCount = runnersData.total_running || 0
          setSystemMetrics(prev => ({
            ...prev,
            activeRunners: activeCount,
            totalRunners: 6,
          }))
        }
        setLastSync(new Date())
        setApiError(null)
        break

      case 'system_status':
        if (lastMessage.data.system_status) {
          setSystemStatus(lastMessage.data.system_status)
          setIsHunting(lastMessage.data.system_status.is_hunting)
        }
        break

      case 'runner_update':
        const updateData = lastMessage.data
        if (updateData.runner_id && updateData.status) {
          setRunners(prev =>
            prev.map(runner => {
              if (runner.runnerId === updateData.runner_id) {
                return {
                  ...runner,
                  status: updateData.status === 'running' ? 'running' : 'idle',
                  cpuPercent: updateData.cpu_percent,
                  memoryPercent: updateData.memory_percent,
                  systemLoad: updateData.cpu_percent ? Math.round(updateData.cpu_percent) : 0,
                  lastScan: updateData.status === 'running' ? 'Last scan 1 min ago' : 'Last scan 1 hour ago',
                }
              }
              return runner
            })
          )
        }
        break

      case 'error':
        setApiError(lastMessage.data.message || 'Unknown error')
        break
    }
  }, [lastMessage])

  // WebSocket connection status handling
  useEffect(() => {
    if (wsError) {
      setSystemError(`WebSocket connection failed: ${wsError}`)
    } else if (isConnected) {
      setSystemError(null)
    }
  }, [wsError, isConnected])

  const handleToggleRunner = async (runnerId: string, runnerBackendId: string) => {
    const runner = runners.find(r => r.id === runnerId)
    if (!runner) return

    const isStarting = runner.status === 'idle'
    const endpoint = isStarting ? `/api/runners/${runnerBackendId}/start` : `/api/runners/${runnerBackendId}/stop`

    // Set loading state
    setLoadingStates(prev => ({ ...prev, [runnerId]: true }))

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const result = await response.json()

      if (result.success) {
        // Update local state immediately
        setRunners(prev =>
          prev.map(r => {
            if (r.id === runnerId) {
              return {
                ...r,
                status: isStarting ? 'running' : 'idle',
                systemLoad: isStarting ? Math.floor(Math.random() * 40) + 40 : 0,
                lastScan: isStarting ? 'Last scan 1 min ago' : 'Last scan 1 hour ago',
                pid: result.data?.pid,
              }
            }
            return r
          })
        )

        // Update active runners count
        setRunners(prev => {
          const activeCount = prev.filter(r => r.status === 'running').length
          setSystemMetrics(metrics => ({
            ...metrics,
            activeRunners: activeCount,
          }))
          return prev
        })

        setApiError(null)
      } else {
        throw new Error(result.detail || 'Operation failed')
      }
    } catch (error) {
      console.error(`Failed to ${isStarting ? 'start' : 'stop'} runner:`, error)
      setApiError(
        `Failed to ${isStarting ? 'start' : 'stop'} ${runner.name}: ${error instanceof Error ? error.message : 'Unknown error'}`
      )

      // Revert state on error
      setTimeout(() => {
        fetchRunnersStatus()
      }, 2000)
    } finally {
      // Clear loading state
      setLoadingStates(prev => ({ ...prev, [runnerId]: false }))
    }
  }

  const getRateLimitColor = (status: string) => {
    switch (status) {
      case 'Normal':
        return 'text-emerald-500'
      case 'Warning':
        return 'text-amber-500'
      case 'Critical':
        return 'text-red-500'
      default:
        return 'text-zinc-500'
    }
  }

  const getSystemLoadColor = (load: number) => {
    if (load < 50) return 'text-emerald-500'
    if (load < 75) return 'text-amber-500'
    return 'text-red-500'
  }

  return (
    <div className="min-h-screen bg-black p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Server className="h-8 w-8 text-emerald-500" />
          <h1 className="text-4xl font-bold text-zinc-100">System Orchestrator & Core Runners</h1>
        </div>
        <p className="text-lg text-zinc-400">Master control panel for production runners and automated systems</p>
      </div>

      {/* System Control Section */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Radio className="h-6 w-6 text-emerald-500" />
          <h2 className="text-2xl font-bold text-zinc-100">System Control Interface</h2>
        </div>
        <p className="text-zinc-400 mb-6">Advanced control system for Lumina OS operations via Web Dashboard</p>

        {/* System Status Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">Lumina OS</CardTitle>
              <Server className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-emerald-500">{systemStatus.lumina_os}</div>
              <p className="text-xs text-zinc-500 mt-1">Core System</p>
            </CardContent>
          </Card>

          <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">Database</CardTitle>
              <Globe className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-emerald-500">{systemStatus.database}</div>
              <p className="text-xs text-zinc-500 mt-1">Cloud Storage</p>
            </CardContent>
          </Card>

          <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">Hunter Status</CardTitle>
              <Activity className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-emerald-500">{systemStatus.hunt_duration}</div>
              <p className="text-xs text-zinc-500 mt-1">Mission Duration</p>
            </CardContent>
          </Card>

          <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-zinc-400">System Load</CardTitle>
              <Cpu className="h-4 w-4 text-emerald-500" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-emerald-500">{systemStatus.cpu}</div>
              <p className="text-xs text-zinc-500 mt-1">CPU Usage</p>
            </CardContent>
          </Card>
        </div>

        {/* Control Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button
            onClick={startHunter}
            disabled={isHunting || systemControlLoading}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-6 px-8 text-lg border-emerald-500/50 backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div className="flex items-center gap-3">
              {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Play className="h-5 w-5" />}
              <span>INITIATE HUNTER PROTOCOL</span>
            </div>
          </Button>

          <Button
            onClick={stopHunter}
            disabled={!isHunting || systemControlLoading}
            variant="outline"
            className="border-amber-500/50 text-amber-500 hover:bg-amber-500/10 font-bold py-6 px-8 text-lg backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div className="flex items-center gap-3">
              {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Square className="h-5 w-5" />}
              <span>ABORT MISSION</span>
            </div>
          </Button>

          <Button
            onClick={emergencyStopAll}
            disabled={systemControlLoading}
            variant="outline"
            className="border-red-500/50 text-red-500 hover:bg-red-500/10 font-bold py-6 px-8 text-lg backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div className="flex items-center gap-3">
              {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Shield className="h-5 w-5" />}
              <span>EMERGENCY STOP</span>
            </div>
          </Button>
        </div>

        {systemError && (
          <div className="mt-4 p-4 bg-red-900/20 border border-red-500/50 rounded-lg">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-red-500" />
              <span className="text-red-500 text-sm">System Control Error: {systemError}</span>
            </div>
          </div>
        )}
      </div>

      {/* System Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* System Load Card */}
        <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">System Load</CardTitle>
            <Cpu className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={getSystemLoadColor(systemMetrics.systemLoad)}>{systemMetrics.systemLoad}%</span>
            </div>
            <p className="text-xs text-zinc-500 mt-1">CPU & Memory Usage</p>
            <div className="mt-2 w-full bg-zinc-800 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${
                  systemMetrics.systemLoad < 50
                    ? 'bg-emerald-500'
                    : systemMetrics.systemLoad < 75
                      ? 'bg-amber-500'
                      : 'bg-red-500'
                }`}
                style={{ width: `${systemMetrics.systemLoad}%` }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Active Runners Card */}
        <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Active Runners</CardTitle>
            <Activity className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-500">
              {systemMetrics.activeRunners}/{systemMetrics.totalRunners}
            </div>
            <p className="text-xs text-zinc-500 mt-1">Production Systems Online</p>
            <div className="mt-2 flex gap-1">
              {Array.from({ length: systemMetrics.totalRunners }).map((_, i) => (
                <div
                  key={i}
                  className={`h-2 w-2 rounded-full ${
                    i < systemMetrics.activeRunners ? 'bg-emerald-500' : 'bg-zinc-700'
                  }`}
                />
              ))}
            </div>
          </CardContent>
        </Card>

        {/* API Rate Limit Card */}
        <Card className="bg-zinc-950/50 border-zinc-800 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">API Rate Limit</CardTitle>
            <Zap className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getRateLimitColor(systemMetrics.apiRateLimit)}`}>
              {systemMetrics.apiRateLimit}
            </div>
            <p className="text-xs text-zinc-500 mt-1">External API Status</p>
            <Badge
              variant="outline"
              className={`mt-2 ${
                systemMetrics.apiRateLimit === 'Normal'
                  ? 'border-emerald-500 text-emerald-500'
                  : systemMetrics.apiRateLimit === 'Warning'
                    ? 'border-amber-500 text-amber-500'
                    : 'border-red-500 text-red-500'
              }`}
            >
              {systemMetrics.apiRateLimit}
            </Badge>
          </CardContent>
        </Card>
      </div>

      {/* Runners Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {runners.map(runner => {
          const IconComponent = runner.icon
          return (
            <Card
              key={runner.id}
              className={`bg-zinc-950/50 border backdrop-blur-sm transition-all duration-300 ${
                runner.status === 'running'
                  ? 'border-emerald-500/50 shadow-lg shadow-emerald-500/20'
                  : 'border-zinc-800'
              }`}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div
                      className={`p-2 rounded-lg ${
                        runner.status === 'running' ? 'bg-emerald-500/20 text-emerald-500' : 'bg-zinc-800 text-zinc-500'
                      }`}
                    >
                      <IconComponent className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-sm font-semibold text-zinc-100">{runner.name}</CardTitle>
                      <p className="text-xs text-zinc-500 mt-1 max-w-xs">{runner.description}</p>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Status Toggle */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="relative">
                      <Switch
                        checked={runner.status === 'running'}
                        onCheckedChange={() => handleToggleRunner(runner.id, runner.runnerId)}
                        disabled={loadingStates[runner.id]}
                        className={runner.status === 'running' ? 'data-[state=checked]:bg-emerald-500' : ''}
                      />
                      {loadingStates[runner.id] && (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <Loader2 className="h-3 w-3 animate-spin text-zinc-400" />
                        </div>
                      )}
                    </div>
                    <span
                      className={`text-sm font-medium ${
                        runner.status === 'running' ? 'text-emerald-500' : 'text-zinc-500'
                      }`}
                    >
                      Status: {runner.status === 'running' ? 'Running' : 'Idle'}
                    </span>
                  </div>
                  <div
                    className={`w-2 h-2 rounded-full ${
                      runner.status === 'running' ? 'bg-emerald-500 animate-pulse' : 'bg-zinc-600'
                    }`}
                  />
                </div>

                {/* System Load Bar */}
                {runner.status === 'running' && (
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-zinc-500">System Load</span>
                      <span className={`text-xs font-medium ${getSystemLoadColor(runner.systemLoad)}`}>
                        {runner.systemLoad}%
                      </span>
                    </div>
                    <div className="w-full bg-zinc-800 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full transition-all duration-500 ${
                          runner.systemLoad < 50
                            ? 'bg-emerald-500'
                            : runner.systemLoad < 75
                              ? 'bg-amber-500'
                              : 'bg-red-500'
                        }`}
                        style={{ width: `${runner.systemLoad}%` }}
                      />
                    </div>
                  </div>
                )}

                {/* Success Rate */}
                {runner.status === 'running' && (
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-zinc-500">Success Rate</span>
                    <span className="text-xs font-medium text-emerald-500">{runner.successRate}%</span>
                  </div>
                )}

                {/* Last Log */}
                <div className="pt-2 border-t border-zinc-800">
                  <div className="flex items-center gap-2">
                    <AlertCircle className="h-3 w-3 text-zinc-500" />
                    <span className="text-xs text-zinc-400">{runner.lastScan}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* System Status Footer */}
      <div className="mt-8 p-4 bg-zinc-950/50 border border-zinc-800 rounded-lg backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${apiError ? 'bg-red-500' : 'bg-emerald-500 animate-pulse'}`} />
            <span className="text-sm text-zinc-400">Master Orchestrator {apiError ? 'Offline' : 'Online'}</span>
            {apiError && <span className="text-xs text-red-500 ml-2">{apiError}</span>}
          </div>
          <div className="flex items-center gap-4 text-xs text-zinc-500">
            <span>Last sync: {lastSync.toLocaleTimeString()}</span>
            <span>•</span>
            <span>Uptime: 4d 12h 23m</span>
            <span>•</span>
            <span>Version: 2.1.0</span>
          </div>
        </div>
      </div>
    </div>
  )
}
