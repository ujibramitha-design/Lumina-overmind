'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Activity, Clock, TrendingUp, Command } from 'lucide-react'

interface AnalyticsData {
  usage_stats: {
    total_commands: number
    chat_sessions: number
    voice_commands: number
    system_commands: number
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

export default function JarvisAnalyticsCharts() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
    const interval = setInterval(fetchAnalytics, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/jarvis/analytics')
      if (response.ok) {
        const data = await response.json()
        setAnalytics(data)
      }
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading || !analytics) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="border-zinc-800 bg-black/35">
            <CardContent className="p-6">
              <div className="animate-pulse space-y-3">
                <div className="h-4 bg-zinc-800 rounded w-1/3" />
                <div className="h-32 bg-zinc-800 rounded" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  // Prepare chart data
  const commandDistribution = [
    { name: 'Chat', value: analytics.usage_stats.chat_sessions, color: '#10b981' },
    { name: 'Voice', value: analytics.usage_stats.voice_commands, color: '#3b82f6' },
    { name: 'System', value: analytics.usage_stats.system_commands, color: '#f59e0b' },
    { name: 'Errors', value: analytics.usage_stats.errors, color: '#ef4444' },
  ]

  const popularCommandsData = analytics.popular_commands.slice(0, 5).map(cmd => ({
    name: cmd.command.substring(0, 20) + '...',
    usage: cmd.usage,
  }))

  const performanceData = [
    { name: 'Response Time', value: analytics.performance_metrics.avg_response_time * 1000, unit: 'ms' },
    { name: 'Success Rate', value: analytics.performance_metrics.success_rate, unit: '%' },
    { name: 'Error Rate', value: analytics.performance_metrics.error_rate, unit: '%' },
  ]

  const commandHistoryData = [
    { time: '00:00', commands: 12 },
    { time: '04:00', commands: 8 },
    { time: '08:00', commands: 25 },
    { time: '12:00', commands: 42 },
    { time: '16:00', commands: 38 },
    { time: '20:00', commands: 55 },
  ]

  return (
    <div className="space-y-4">
      {/* Command Distribution Pie Chart */}
      <Card className="border-zinc-800 bg-black/35">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-zinc-100">
            <Command className="h-4 w-4 text-emerald-400" />
            Distribusi Perintah
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={commandDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {commandDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Popular Commands Bar Chart */}
      <Card className="border-zinc-800 bg-black/35">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-zinc-100">
            <TrendingUp className="h-4 w-4 text-emerald-400" />
            Perintah Populer
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={popularCommandsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" />
              <XAxis dataKey="name" stroke="#71717a" tick={{ fontSize: 12 }} />
              <YAxis stroke="#71717a" />
              <Tooltip
                contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46' }}
                itemStyle={{ color: '#a1a1aa' }}
              />
              <Bar dataKey="usage" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      <Card className="border-zinc-800 bg-black/35">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-zinc-100">
            <Clock className="h-4 w-4 text-emerald-400" />
            Metrik Performa
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={performanceData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" />
              <XAxis type="number" stroke="#71717a" />
              <YAxis dataKey="name" type="category" stroke="#71717a" tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46' }}
                itemStyle={{ color: '#a1a1aa' }}
                formatter={(value, name, props) => [`${value} ${props.payload.unit}`, name]}
              />
              <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Command History Line Chart */}
      <Card className="border-zinc-800 bg-black/35">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-zinc-100">
            <Activity className="h-4 w-4 text-emerald-400" />
            Riwayat Perintah (24 Jam)
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={commandHistoryData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" />
              <XAxis dataKey="time" stroke="#71717a" />
              <YAxis stroke="#71717a" />
              <Tooltip
                contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46' }}
                itemStyle={{ color: '#a1a1aa' }}
              />
              <Line
                type="monotone"
                dataKey="commands"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ fill: '#10b981', strokeWidth: 2 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
