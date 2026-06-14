'use client'

import React, { useState, useEffect, useRef } from 'react'
import {
  Brain,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Power,
  PowerOff,
  MessageSquare,
  Settings,
  Activity,
  Zap,
  Shield,
  AlertCircle,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useToast } from '@/hooks/use-toast'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface JarvisMessage {
  id: string
  type: 'user' | 'jarvis'
  content: string
  timestamp: string
  platform: string
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

export default function JarvisAssistant() {
  const [isActive, setIsActive] = useState(true)
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [messages, setMessages] = useState<JarvisMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [jarvisStatus, setJarvisStatus] = useState<JarvisStatus | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [isMinimized, setIsMinimized] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Fetch J.A.R.V.I.S. status on mount
  useEffect(() => {
    fetchJarvisStatus()
    const interval = setInterval(fetchJarvisStatus, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  // Listen for quick commands from floating button
  useEffect(() => {
    const handleQuickCommand = (event: CustomEvent) => {
      const command = event.detail
      if (command && isActive) {
        sendMessage(command, 'quick-action')
      }
    }

    window.addEventListener('jarvis-command', handleQuickCommand as EventListener)
    return () => window.removeEventListener('jarvis-command', handleQuickCommand as EventListener)
  }, [isActive])

  const fetchJarvisStatus = async () => {
    try {
      const response = await fetch('/api/jarvis/status')
      if (response.ok) {
        const status = await response.json()
        setJarvisStatus(status)
        setIsActive(status.is_active)
      }
    } catch (error) {
      console.error('Error fetching J.A.R.V.I.S. status:', error)
    }
  }

  const toggleJarvis = async () => {
    try {
      const response = await fetch('/api/jarvis/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })

      if (response.ok) {
        const result = await response.json()
        setIsActive(result.is_active)
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
    }
  }

  const sendMessage = async (message: string, platform: string = 'dashboard') => {
    if (!message.trim() || !isActive) return

    const userMessage: JarvisMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: message,
      timestamp: new Date().toISOString(),
      platform,
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch('/api/jarvis/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          platform,
          project_type: 'KOMERSIL', // TODO: Get from current project
        }),
      })

      if (response.ok) {
        const result = await response.json()

        const jarvisMessage: JarvisMessage = {
          id: (Date.now() + 1).toString(),
          type: 'jarvis',
          content: result.response,
          timestamp: result.timestamp,
          platform: result.platform,
        }

        setMessages(prev => [...prev, jarvisMessage])

        // Auto-speak response if voice is enabled
        if (isSpeaking) {
          speakText(result.response)
        }
      } else {
        throw new Error('Failed to send message')
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to communicate with J.A.R.V.I.S.',
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  const startListening = () => {
    if (!isActive || (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window))) {
      toast({
        title: 'Voice Recognition Not Available',
        description: "Your browser doesn't support voice recognition",
        variant: 'destructive',
      })
      return
    }

    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'id-ID'

    recognition.onstart = () => {
      setIsListening(true)
    }

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript
      sendMessage(transcript, 'voice')
    }

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error)
      setIsListening(false)
      toast({
        title: 'Voice Recognition Error',
        description: 'Failed to recognize speech. Please try again.',
        variant: 'destructive',
      })
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognition.start()
  }

  const stopListening = () => {
    setIsListening(false)
    // Speech recognition will stop automatically
  }

  const speakText = (text: string) => {
    if (!('speechSynthesis' in window)) return

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'id-ID'
    utterance.rate = 0.9
    utterance.pitch = 0.8

    utterance.onstart = () => {
      setIsSpeaking(true)
    }

    utterance.onend = () => {
      setIsSpeaking(false)
    }

    window.speechSynthesis.speak(utterance)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(inputMessage)
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

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          onClick={() => setIsMinimized(false)}
          className="bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700 text-white rounded-full p-4 shadow-lg"
        >
          <Brain className="h-6 w-6" />
          {isActive && <div className="absolute -top-1 -right-1 h-3 w-3 bg-green-400 rounded-full animate-pulse"></div>}
        </Button>
      </div>
    )
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 w-96 h-[600px]">
      <Card className="h-full bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 border-emerald-500/50 shadow-2xl">
        {/* Header */}
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="h-6 w-6 text-emerald-400" />
              <CardTitle className="text-lg text-white">J.A.R.V.I.S.</CardTitle>
              {isActive && <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>}
            </div>

            <div className="flex items-center gap-2">
              {/* Voice Toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsSpeaking(!isSpeaking)}
                className="text-gray-400 hover:text-white"
                disabled={!isActive}
              >
                {isSpeaking ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
              </Button>

              {/* Settings */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSettings(!showSettings)}
                className="text-gray-400 hover:text-white"
              >
                <Settings className="h-4 w-4" />
              </Button>

              {/* Minimize */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMinimized(true)}
                className="text-gray-400 hover:text-white"
              >
                −
              </Button>

              {/* Power Toggle */}
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleJarvis}
                className={`${isActive ? 'text-red-400 hover:text-red-300' : 'text-green-400 hover:text-green-300'}`}
              >
                {isActive ? <PowerOff className="h-4 w-4" /> : <Power className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          {/* Status Bar */}
          {jarvisStatus && (
            <div className="flex items-center gap-2 text-xs">
              <Badge className={getStatusColor(jarvisStatus.status)}>{jarvisStatus.status}</Badge>
              <Badge className={getProviderColor(jarvisStatus.provider)}>{jarvisStatus.provider}</Badge>
              <span className="text-gray-400">{jarvisStatus.capabilities.length} capabilities</span>
            </div>
          )}
        </CardHeader>

        <CardContent className="flex flex-col h-full p-0">
          {/* Settings Panel */}
          {showSettings && (
            <div className="p-4 border-b border-slate-700">
              <h4 className="text-white font-medium mb-3">J.A.R.V.I.S. Settings</h4>

              {jarvisStatus && (
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Database Status:</span>
                    <span
                      className={`text-${jarvisStatus.system_health.database_status === 'online' ? 'green' : 'red'}-400`}
                    >
                      {jarvisStatus.system_health.database_status}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">API Status:</span>
                    <span
                      className={`text-${jarvisStatus.system_health.api_status === 'online' ? 'green' : 'red'}-400`}
                    >
                      {jarvisStatus.system_health.api_status}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Memory Usage:</span>
                    <span className="text-gray-300">{jarvisStatus.system_health.memory_usage}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">CPU Usage:</span>
                    <span className="text-gray-300">{jarvisStatus.system_health.cpu_usage}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Last Activity:</span>
                    <span className="text-gray-300">{new Date(jarvisStatus.last_activity).toLocaleTimeString()}</span>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Messages Area */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-3">
              {messages.length === 0 && (
                <div className="text-center text-gray-400 py-8">
                  <Brain className="h-12 w-12 mx-auto mb-4 text-emerald-400" />
                  <p className="text-sm">J.A.R.V.I.S. is ready to assist you, Komandan.</p>
                  <p className="text-xs mt-2">Try commands like:</p>
                  <div className="text-xs mt-1 space-y-1">
                    <p>• "Berikan saya statistik sistem"</p>
                    <p>• "Deploy hunter agent ke Serang"</p>
                    <p>• "Buat presentasi untuk Budi"</p>
                  </div>
                </div>
              )}

              {messages.map(message => (
                <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                        : 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      {message.type === 'user' ? <MessageSquare className="h-3 w-3" /> : <Brain className="h-3 w-3" />}
                      <span className="text-xs opacity-70">{message.type === 'user' ? 'You' : 'J.A.R.V.I.S.'}</span>
                      <span className="text-xs opacity-50">{new Date(message.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-blue-600/20 text-blue-400 border border-blue-500/30 p-3 rounded-lg">
                    <div className="flex items-center gap-2">
                      <Brain className="h-3 w-3 animate-pulse" />
                      <span className="text-sm">J.A.R.V.I.S. is processing...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div ref={messagesEndRef} />
          </ScrollArea>

          {/* Input Area */}
          <div className="p-4 border-t border-slate-700">
            {!isActive && (
              <Alert className="mb-3 bg-red-500/20 border-red-500/30">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  J.A.R.V.I.S. is currently deactivated. Click the power button to activate.
                </AlertDescription>
              </Alert>
            )}

            <div className="flex gap-2">
              <Input
                value={inputMessage}
                onChange={e => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your command or use voice..."
                disabled={!isActive || isLoading}
                className="flex-1 bg-slate-800/50 border-slate-600 text-white placeholder-gray-400"
              />

              {/* Voice Button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={isListening ? stopListening : startListening}
                disabled={!isActive || isLoading}
                className={`${isListening ? 'bg-red-600/20 text-red-400' : 'bg-emerald-600/20 text-emerald-400'} hover:bg-emerald-600/30`}
              >
                {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
              </Button>

              {/* Send Button */}
              <Button
                onClick={() => sendMessage(inputMessage)}
                disabled={!isActive || isLoading || !inputMessage.trim()}
                className="bg-emerald-600 hover:bg-emerald-700 text-white"
              >
                <Zap className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
