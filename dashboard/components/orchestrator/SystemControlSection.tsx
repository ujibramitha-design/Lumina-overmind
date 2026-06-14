'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Server, Globe, Activity, Cpu, Radio, Play, Square, Shield, Loader2 } from 'lucide-react'

interface SystemStatus {
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

interface SystemControlSectionProps {
  systemStatus: SystemStatus
  isHunting: boolean
  systemControlLoading: boolean
  systemError: string | null
  onStartHunter: () => void
  onStopHunter: () => void
  onEmergencyStop: () => void
}

export function SystemControlSection({
  systemStatus,
  isHunting,
  systemControlLoading,
  systemError,
  onStartHunter,
  onStopHunter,
  onEmergencyStop,
}: SystemControlSectionProps) {
  return (
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
          onClick={onStartHunter}
          disabled={isHunting || systemControlLoading}
          className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-6 px-8 text-lg border-emerald-500/50 backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Initiate hunter protocol"
        >
          <div className="flex items-center gap-3">
            {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Play className="h-5 w-5" />}
            <span>INITIATE HUNTER PROTOCOL</span>
          </div>
        </Button>

        <Button
          onClick={onStopHunter}
          disabled={!isHunting || systemControlLoading}
          variant="outline"
          className="border-amber-500/50 text-amber-500 hover:bg-amber-500/10 font-bold py-6 px-8 text-lg backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Abort hunter mission"
        >
          <div className="flex items-center gap-3">
            {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Square className="h-5 w-5" />}
            <span>ABORT MISSION</span>
          </div>
        </Button>

        <Button
          onClick={onEmergencyStop}
          disabled={systemControlLoading}
          variant="outline"
          className="border-red-500/50 text-red-500 hover:bg-red-500/10 font-bold py-6 px-8 text-lg backdrop-blur-sm transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Emergency stop all systems"
        >
          <div className="flex items-center gap-3">
            {systemControlLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Shield className="h-5 w-5" />}
            <span>EMERGENCY STOP</span>
          </div>
        </Button>
      </div>

      {systemError && (
        <div className="mt-4 p-4 bg-red-900/20 border border-red-500/50 rounded-lg" role="alert">
          <div className="flex items-center gap-2">
            <span className="text-red-500 text-sm">System Control Error: {systemError}</span>
          </div>
        </div>
      )}
    </div>
  )
}
