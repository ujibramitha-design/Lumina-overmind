'use client'

import React from 'react'

interface SystemStatusFooterProps {
  apiError: string | null
  lastSync: Date
}

export function SystemStatusFooter({ apiError, lastSync }: SystemStatusFooterProps) {
  return (
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
  )
}
