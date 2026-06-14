'use client'

import React, { useState } from 'react'
import { Brain, MessageSquare, X, ChevronUp } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'

interface JarvisFloatingButtonProps {
  isActive: boolean
  onToggle: () => void
  unreadCount?: number
}

export default function JarvisFloatingButton({ isActive, onToggle, unreadCount = 0 }: JarvisFloatingButtonProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const { toast } = useToast()

  const handleQuickActions = () => {
    setIsExpanded(!isExpanded)
  }

  const quickCommands = [
    {
      icon: <Brain className="h-4 w-4" />,
      label: 'System Stats',
      command: 'Berikan saya statistik sistem',
    },
    {
      icon: <MessageSquare className="h-4 w-4" />,
      label: 'Deploy Hunter',
      command: 'Deploy hunter agent ke Serang',
    },
    {
      icon: <Brain className="h-4 w-4" />,
      label: 'Market Intel',
      command: 'Berikan intelijen pasar',
    },
  ]

  const handleQuickCommand = (command: string) => {
    // Send command to J.A.R.V.I.S. via global event or state
    const event = new CustomEvent('jarvis-command', { detail: command })
    window.dispatchEvent(event)

    toast({
      title: 'Quick Command Sent',
      description: `Command: "${command}"`,
    })

    setIsExpanded(false)
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end gap-2">
      {/* Quick Actions Panel */}
      {isExpanded && (
        <div className="bg-slate-900/95 backdrop-blur-sm border border-slate-700 rounded-lg p-2 mb-2 shadow-2xl">
          <div className="space-y-2">
            <div className="text-xs text-gray-400 px-2 py-1 font-medium">Quick Commands</div>
            {quickCommands.map((cmd, idx) => (
              <Button
                key={idx}
                variant="ghost"
                size="sm"
                onClick={() => handleQuickCommand(cmd.command)}
                className="w-full justify-start text-gray-300 hover:text-white hover:bg-slate-800"
              >
                <span className="mr-2 text-emerald-400">{cmd.icon}</span>
                <span className="text-sm">{cmd.label}</span>
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Main Floating Button */}
      <div className="relative">
        {/* Unread Badge */}
        {unreadCount > 0 && (
          <Badge className="absolute -top-2 -right-2 bg-red-500 text-white text-xs px-1.5 py-0.5 min-w-[20px] h-5 flex items-center justify-center">
            {unreadCount}
          </Badge>
        )}

        {/* Main Button */}
        <Button
          onClick={onToggle}
          className={`relative w-14 h-14 rounded-full shadow-lg transition-all duration-300 ${
            isActive
              ? 'bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700'
              : 'bg-slate-700 hover:bg-slate-600'
          } text-white border-2 ${isActive ? 'border-emerald-400/50' : 'border-slate-600'}`}
        >
          <Brain className={`h-6 w-6 transition-transform ${isActive ? 'animate-pulse' : ''}`} />

          {/* Active Indicator */}
          {isActive && <div className="absolute inset-0 rounded-full bg-emerald-400/20 animate-ping"></div>}
        </Button>

        {/* Quick Actions Toggle */}
        <Button
          onClick={handleQuickActions}
          variant="ghost"
          size="sm"
          className={`absolute -bottom-8 left-1/2 transform -translate-x-1/2 text-xs px-2 py-1 rounded-full transition-all duration-300 ${
            isExpanded ? 'bg-slate-700 text-white' : 'bg-slate-800/70 text-gray-400 hover:text-white'
          }`}
        >
          <ChevronUp className={`h-3 w-3 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
        </Button>
      </div>
    </div>
  )
}
