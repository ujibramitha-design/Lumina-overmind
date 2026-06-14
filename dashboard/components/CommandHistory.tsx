'use client'

import { useState, useEffect } from 'react'
import { Search, Clock, Filter, Trash2, Download } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'

interface Command {
  id: string
  command: string
  platform: 'chat' | 'voice' | 'system'
  timestamp: Date
  status: 'success' | 'error' | 'pending'
  response?: string
}

export default function CommandHistory() {
  const [commands, setCommands] = useState<Command[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filterPlatform, setFilterPlatform] = useState<'all' | 'chat' | 'voice' | 'system'>('all')
  const [filterStatus, setFilterStatus] = useState<'all' | 'success' | 'error' | 'pending'>('all')

  useEffect(() => {
    // Simulate fetching command history
    const mockCommands: Command[] = [
      {
        id: '1',
        command: 'Berikan saya statistik sistem',
        platform: 'voice',
        timestamp: new Date(Date.now() - 1000 * 60 * 5),
        status: 'success',
        response: 'Sistem berjalan normal dengan 95% success rate',
      },
      {
        id: '2',
        command: 'Deploy hunter agent ke Serang',
        platform: 'chat',
        timestamp: new Date(Date.now() - 1000 * 60 * 15),
        status: 'success',
        response: 'Hunter agent berhasil dideploy ke lokasi Serang',
      },
      {
        id: '3',
        command: 'get_system_stats',
        platform: 'system',
        timestamp: new Date(Date.now() - 1000 * 60 * 30),
        status: 'success',
        response: 'CPU: 45%, Memory: 60%, Disk: 30%',
      },
      {
        id: '4',
        command: 'Buat presentasi untuk Budi',
        platform: 'chat',
        timestamp: new Date(Date.now() - 1000 * 60 * 45),
        status: 'error',
        response: 'Lead Budi tidak ditemukan dalam database',
      },
      {
        id: '5',
        command: 'Berikan intelijen pasar',
        platform: 'voice',
        timestamp: new Date(Date.now() - 1000 * 60 * 60),
        status: 'success',
        response: 'Tren pasar menunjukkan peningkatan 15% di sektor properti',
      },
    ]
    setCommands(mockCommands)
  }, [])

  const filteredCommands = commands.filter(cmd => {
    const matchesSearch = cmd.command.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (cmd.response && cmd.response.toLowerCase().includes(searchQuery.toLowerCase()))
    const matchesPlatform = filterPlatform === 'all' || cmd.platform === filterPlatform
    const matchesStatus = filterStatus === 'all' || cmd.status === filterStatus
    return matchesSearch && matchesPlatform && matchesStatus
  })

  const getStatusColor = (status: Command['status']) => {
    switch (status) {
      case 'success':
        return 'text-emerald-400 bg-emerald-500/20'
      case 'error':
        return 'text-red-400 bg-red-500/20'
      case 'pending':
        return 'text-yellow-400 bg-yellow-500/20'
    }
  }

  const getPlatformIcon = (platform: Command['platform']) => {
    switch (platform) {
      case 'chat':
        return '💬'
      case 'voice':
        return '🎤'
      case 'system':
        return '⚙️'
    }
  }

  const exportHistory = () => {
    const csvContent = [
      ['Timestamp', 'Platform', 'Command', 'Status', 'Response'],
      ...filteredCommands.map(cmd => [
        cmd.timestamp.toISOString(),
        cmd.platform,
        cmd.command,
        cmd.status,
        cmd.response || '',
      ]),
    ]
      .map(row => row.join(','))
      .join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `jarvis-command-history-${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const clearHistory = () => {
    setCommands([])
  }

  return (
    <Card className="border-zinc-800 bg-black/35">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-zinc-100">
            <Clock className="h-4 w-4 text-emerald-400" />
            Riwayat Perintah
          </CardTitle>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={exportHistory}
              className="border-zinc-700 text-zinc-300 hover:text-zinc-100"
            >
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={clearHistory}
              className="border-zinc-700 text-zinc-300 hover:text-zinc-100"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Hapus
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Search and Filters */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-zinc-500" />
            <Input
              placeholder="Cari perintah..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 bg-zinc-900/50 border-zinc-700 text-zinc-100 placeholder:text-zinc-500"
            />
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setFilterPlatform(filterPlatform === 'all' ? 'chat' : 'all')}
            className="border-zinc-700 text-zinc-300 hover:text-zinc-100"
          >
            <Filter className="h-4 w-4 mr-2" />
            {filterPlatform === 'all' ? 'Semua' : filterPlatform}
          </Button>
        </div>

        {/* Command List */}
        <ScrollArea className="h-[400px]">
          {filteredCommands.length === 0 ? (
            <div className="text-center py-8 text-zinc-500">
              <Clock className="h-12 w-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">Tidak ada riwayat perintah</p>
            </div>
          ) : (
            <div className="space-y-2">
              {filteredCommands.map(cmd => (
                <div
                  key={cmd.id}
                  className="p-3 rounded-lg border border-zinc-800 bg-zinc-900/30 hover:bg-zinc-800/50 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-lg">{getPlatformIcon(cmd.platform)}</span>
                        <p className="text-sm font-medium text-zinc-100 truncate">{cmd.command}</p>
                      </div>
                      <p className="text-xs text-zinc-400 mb-2">{cmd.response}</p>
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full ${getStatusColor(cmd.status)}`}>
                          {cmd.status}
                        </span>
                        <span className="text-[10px] text-zinc-500">
                          {cmd.timestamp.toLocaleString('id-ID')}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
