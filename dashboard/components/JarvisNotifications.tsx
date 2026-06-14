'use client'

import { useState, useEffect } from 'react'
import { Bell, X, CheckCircle, AlertCircle, Info, Zap } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'

interface Notification {
  id: string
  type: 'success' | 'error' | 'info' | 'activity'
  title: string
  message: string
  timestamp: Date
  read: boolean
}

export default function JarvisNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    // Listen for JARVIS events
    const handleJarvisEvent = (event: CustomEvent) => {
      const { type, title, message } = event.detail
      addNotification(type, title, message)
    }

    window.addEventListener('jarvis-notification', handleJarvisEvent as EventListener)

    // Simulate some initial notifications
    addNotification('success', 'J.A.R.V.I.S. Aktif', 'Sistem AI siap digunakan')
    addNotification('info', 'Hunter Agent Deployed', 'Agent hunter dikirim ke Serang')
    addNotification('activity', 'Command Executed', 'get_system_stats berhasil dijalankan')

    return () => {
      window.removeEventListener('jarvis-notification', handleJarvisEvent as EventListener)
    }
  }, [])

  const addNotification = (type: 'success' | 'error' | 'info' | 'activity', title: string, message: string) => {
    const newNotification: Notification = {
      id: Date.now().toString(),
      type,
      title,
      message,
      timestamp: new Date(),
      read: false,
    }

    setNotifications(prev => [newNotification, ...prev].slice(0, 50)) // Keep last 50
  }

  useEffect(() => {
    setUnreadCount(notifications.filter(n => !n.read).length)
  }, [notifications])

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(n => (n.id === id ? { ...n, read: true } : n))
    )
  }

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
  }

  const clearNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  const clearAll = () => {
    setNotifications([])
  }

  const getIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-emerald-400" />
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-400" />
      case 'info':
        return <Info className="h-4 w-4 text-blue-400" />
      case 'activity':
        return <Zap className="h-4 w-4 text-yellow-400" />
    }
  }

  const getBorderColor = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return 'border-emerald-500/30'
      case 'error':
        return 'border-red-500/30'
      case 'info':
        return 'border-blue-500/30'
      case 'activity':
        return 'border-yellow-500/30'
    }
  }

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="relative border-zinc-700 bg-black/35 text-zinc-300 hover:text-zinc-100"
      >
        <Bell className="h-4 w-4" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 h-4 w-4 bg-emerald-500 rounded-full text-[10px] flex items-center justify-center text-white">
            {unreadCount}
          </span>
        )}
      </Button>

      {isOpen && (
        <Card className="absolute right-0 top-12 w-80 border-zinc-800 bg-zinc-950/95 shadow-xl z-50">
          <CardHeader className="flex flex-row items-center justify-between pb-3 border-b border-zinc-800">
            <h3 className="text-sm font-semibold text-zinc-100">Notifikasi J.A.R.V.I.S.</h3>
            <div className="flex gap-1">
              {unreadCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={markAllAsRead}
                  className="text-xs text-zinc-400 hover:text-zinc-100"
                >
                  Tandai Semua
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={clearAll}
                className="text-xs text-zinc-400 hover:text-zinc-100"
              >
                Hapus Semua
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <ScrollArea className="h-96">
              {notifications.length === 0 ? (
                <div className="p-8 text-center text-zinc-500">
                  <Bell className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">Tidak ada notifikasi</p>
                </div>
              ) : (
                <div className="p-2 space-y-2">
                  {notifications.map(notification => (
                    <div
                      key={notification.id}
                      className={`p-3 rounded-lg border ${getBorderColor(notification.type)} bg-black/35 hover:bg-zinc-800/50 transition-colors ${!notification.read ? 'border-l-4' : ''}`}
                      onClick={() => markAsRead(notification.id)}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-start gap-2 flex-1">
                          {getIcon(notification.type)}
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-zinc-100">{notification.title}</p>
                            <p className="text-xs text-zinc-400 mt-1">{notification.message}</p>
                            <p className="text-[10px] text-zinc-500 mt-1">
                              {notification.timestamp.toLocaleTimeString('id-ID')}
                            </p>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            clearNotification(notification.id)
                          }}
                          className="h-6 w-6 p-0 text-zinc-500 hover:text-zinc-100"
                        >
                          <X className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
