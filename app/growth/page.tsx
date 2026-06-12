'use client'

/**
 * LUMINA OS - Growth Analytics Dashboard
 * ========================================
 * 
 * Advanced growth analytics with shadow network monitoring
 * Meta Conversions API integration and retargeting visualization
 */

import { useState, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import { 
  TrendingUp, 
  Users, 
  Target, 
  Activity, 
  Globe, 
  Shield, 
  Zap, 
  Eye,
  Network,
  Database,
  AlertCircle,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  ArrowUp,
  ArrowDown,
  RefreshCw,
  Settings,
  Download,
  Upload,
  Wifi,
  Radio,
  Monitor,
  Smartphone,
  Phone
} from 'lucide-react'

interface ShadowNetworkStats {
  status: 'active' | 'inactive' | 'error'
  totalRetargeted: number
  successRate: number
  hashRate: number
  lastSync: string
  pixelId: string
  eventsSent: number
  eventsFailed: number
  leadsHashed: number
}

interface GrowthMetrics {
  totalLeads: number
  newLeadsToday: number
  conversionRate: number
  avgScore: number
  topLocations: string[]
  trendingKeywords: string[]
}

interface NetworkActivity {
  timestamp: string
  event: string
  status: 'success' | 'failed'
  dataType: 'email' | 'phone' | 'both'
  hashed: boolean
}

export default function GrowthAnalytics() {
  const [shadowStats, setShadowStats] = useState<ShadowNetworkStats>({
    status: 'active',
    totalRetargeted: 1204,
    successRate: 98.5,
    hashRate: 87.3,
    lastSync: new Date().toISOString(),
    pixelId: '1234567890123456',
    eventsSent: 1456,
    eventsFailed: 22,
    leadsHashed: 1278
  })

  const [growthMetrics, setGrowthMetrics] = useState<GrowthMetrics>({
    totalLeads: 8456,
    newLeadsToday: 127,
    conversionRate: 12.4,
    avgScore: 6.8,
    topLocations: ['Serang', 'Tangerang', 'Jakarta', 'Bogor', 'Bandung'],
    trendingKeywords: ['KPR', 'cicilan', 'DP', 'promo', 'cluster']
  })

  const [networkActivity, setNetworkActivity] = useState<NetworkActivity[]>([
    {
      timestamp: new Date(Date.now() - 300000).toISOString(),
      event: 'LeadGeneration',
      status: 'success',
      dataType: 'both',
      hashed: true
    },
    {
      timestamp: new Date(Date.now() - 600000).toISOString(),
      event: 'TelegramConversation',
      status: 'success',
      dataType: 'email',
      hashed: true
    },
    {
      timestamp: new Date(Date.now() - 900000).toISOString(),
      event: 'LeadGeneration',
      status: 'failed',
      dataType: 'phone',
      hashed: false
    },
    {
      timestamp: new Date(Date.now() - 1200000).toISOString(),
      event: 'WebinarRegistration',
      status: 'success',
      dataType: 'both',
      hashed: true
    }
  ])

  const [isRefreshing, setIsRefreshing] = useState(false)

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setShadowStats(prev => ({
        ...prev,
        lastSync: new Date().toISOString(),
        eventsSent: prev.eventsSent + Math.floor(Math.random() * 3),
        totalRetargeted: prev.totalRetargeted + Math.floor(Math.random() * 2),
        successRate: Math.min(99.9, prev.successRate + (Math.random() - 0.5) * 0.1)
      }))

      setNetworkActivity(prev => {
        const newActivity: NetworkActivity = {
          timestamp: new Date().toISOString(),
          event: ['LeadGeneration', 'TelegramConversation', 'WebinarRegistration'][Math.floor(Math.random() * 3)],
          status: Math.random() > 0.1 ? 'success' : 'failed',
          dataType: ['email', 'phone', 'both'][Math.floor(Math.random() * 3)] as 'email' | 'phone' | 'both',
          hashed: Math.random() > 0.2
        }
        return [newActivity, ...prev].slice(0, 10)
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const handleRefresh = async () => {
    setIsRefreshing(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    setIsRefreshing(false)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-500'
      case 'inactive': return 'text-yellow-500'
      case 'error': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="w-4 h-4" />
      case 'inactive': return <Clock className="w-4 h-4" />
      case 'error': return <AlertCircle className="w-4 h-4" />
      default: return <Activity className="w-4 h-4" />
    }
  }

  return (
    <>
      <Head>
        <title>Growth Analytics - Lumina OS</title>
        <meta name="description" content="Advanced growth analytics and shadow network monitoring" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-black text-white">
        {/* Header */}
        <header className="bg-gradient-to-r from-emerald-500/10 to-green-600/10 border-b border-emerald-500/20">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-emerald-500 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-black" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold">Growth Analytics</h1>
                  <p className="text-gray-400 text-sm">Shadow Network & Performance Monitoring</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleRefresh}
                  disabled={isRefreshing}
                  className="flex items-center space-x-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-lg hover:bg-emerald-500/20 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  <span>Refresh</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-lg hover:bg-blue-500/20 transition-colors">
                  <Download className="w-4 h-4" />
                  <span>Export</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="container mx-auto px-4 py-8">
          {/* Shadow Network Status Panel */}
          <div className="mb-8">
            <div className="bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-emerald-500/30 rounded-2xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-emerald-500 rounded-lg flex items-center justify-center">
                    <Network className="w-6 h-6 text-black" />
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-emerald-400">SHADOW NETWORK STATUS</h2>
                    <p className="text-gray-400 text-sm">Meta Conversions API Retargeting Engine</p>
                  </div>
                </div>
                <div className={`flex items-center space-x-2 ${getStatusColor(shadowStats.status)}`}>
                  {getStatusIcon(shadowStats.status)}
                  <span className="font-semibold uppercase">{shadowStats.status}</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-black/50 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400 text-sm">META CAPI</span>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                  <div className="text-2xl font-bold text-green-400">ACTIVE</div>
                  <div className="text-xs text-gray-500">Pixel ID: {shadowStats.pixelId}</div>
                </div>

                <div className="bg-black/50 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400 text-sm">Total Target</span>
                    <Target className="w-4 h-4 text-emerald-400" />
                  </div>
                  <div className="text-2xl font-bold text-emerald-400">{shadowStats.totalRetargeted.toLocaleString()}</div>
                  <div className="text-xs text-gray-500">Leads Retargeted</div>
                </div>

                <div className="bg-black/50 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400 text-sm">Success Rate</span>
                    <ArrowUp className="w-4 h-4 text-green-400" />
                  </div>
                  <div className="text-2xl font-bold text-green-400">{shadowStats.successRate.toFixed(1)}%</div>
                  <div className="text-xs text-gray-500">Events Delivered</div>
                </div>

                <div className="bg-black/50 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-gray-400 text-sm">Hash Rate</span>
                    <Shield className="w-4 h-4 text-blue-400" />
                  </div>
                  <div className="text-2xl font-bold text-blue-400">{shadowStats.hashRate.toFixed(1)}%</div>
                  <div className="text-xs text-gray-500">Data Hashed</div>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Events Sent</span>
                    <Upload className="w-4 h-4 text-emerald-400" />
                  </div>
                  <div className="text-xl font-bold text-emerald-400">{shadowStats.eventsSent.toLocaleString()}</div>
                </div>

                <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Events Failed</span>
                    <AlertCircle className="w-4 h-4 text-red-400" />
                  </div>
                  <div className="text-xl font-bold text-red-400">{shadowStats.eventsFailed}</div>
                </div>

                <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Leads Hashed</span>
                    <Database className="w-4 h-4 text-blue-400" />
                  </div>
                  <div className="text-xl font-bold text-blue-400">{shadowStats.leadsHashed.toLocaleString()}</div>
                </div>
              </div>

              <div className="mt-4 text-center">
                <div className="text-xs text-gray-500">
                  Last Sync: {new Date(shadowStats.lastSync).toLocaleString()}
                </div>
              </div>
            </div>
          </div>

          {/* Growth Metrics */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-emerald-400" />
                Growth Metrics
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-gray-700">
                  <div>
                    <div className="text-gray-400 text-sm">Total Leads</div>
                    <div className="text-2xl font-bold">{growthMetrics.totalLeads.toLocaleString()}</div>
                  </div>
                  <Users className="w-8 h-8 text-emerald-400" />
                </div>

                <div className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-gray-700">
                  <div>
                    <div className="text-gray-400 text-sm">New Leads Today</div>
                    <div className="text-2xl font-bold text-green-400">{growthMetrics.newLeadsToday}</div>
                  </div>
                  <TrendingUp className="w-8 h-8 text-green-400" />
                </div>

                <div className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-gray-700">
                  <div>
                    <div className="text-gray-400 text-sm">Conversion Rate</div>
                    <div className="text-2xl font-bold text-blue-400">{growthMetrics.conversionRate}%</div>
                  </div>
                  <PieChart className="w-8 h-8 text-blue-400" />
                </div>

                <div className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-gray-700">
                  <div>
                    <div className="text-gray-400 text-sm">Average Score</div>
                    <div className="text-2xl font-bold text-yellow-400">{growthMetrics.avgScore}/10</div>
                  </div>
                  <Activity className="w-8 h-8 text-yellow-400" />
                </div>
              </div>
            </div>

            <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <Globe className="w-5 h-5 mr-2 text-emerald-400" />
                Top Locations & Keywords
              </h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-sm text-gray-400 mb-3">Top Locations</h4>
                  <div className="space-y-2">
                    {growthMetrics.topLocations.map((location, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-black/50 rounded-lg border border-gray-700">
                        <span className="text-sm">{location}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 bg-gray-700 rounded-full h-2">
                            <div 
                              className="bg-emerald-500 h-2 rounded-full" 
                              style={{ width: `${100 - (index * 15)}%` }}
                            ></div>
                          </div>
                          <span className="text-xs text-gray-400">{100 - (index * 15)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm text-gray-400 mb-3">Trending Keywords</h4>
                  <div className="flex flex-wrap gap-2">
                    {growthMetrics.trendingKeywords.map((keyword, index) => (
                      <span 
                        key={index} 
                        className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-xs text-emerald-400"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Network Activity */}
          <div className="bg-gray-900 rounded-2xl p-6 border border-gray-700">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-emerald-400" />
              Recent Network Activity
            </h3>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="text-left py-3 px-4 text-gray-400 text-sm">Timestamp</th>
                    <th className="text-left py-3 px-4 text-gray-400 text-sm">Event</th>
                    <th className="text-left py-3 px-4 text-gray-400 text-sm">Data Type</th>
                    <th className="text-left py-3 px-4 text-gray-400 text-sm">Hashed</th>
                    <th className="text-left py-3 px-4 text-gray-400 text-sm">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {networkActivity.map((activity, index) => (
                    <tr key={index} className="border-b border-gray-800">
                      <td className="py-3 px-4 text-sm">
                        {new Date(activity.timestamp).toLocaleString()}
                      </td>
                      <td className="py-3 px-4 text-sm">{activity.event}</td>
                      <td className="py-3 px-4 text-sm">
                        <div className="flex items-center space-x-2">
                          {activity.dataType === 'email' && <Smartphone className="w-4 h-4 text-blue-400" />}
                          {activity.dataType === 'phone' && <Phone className="w-4 h-4 text-green-400" />}
                          {activity.dataType === 'both' && <Globe className="w-4 h-4 text-emerald-400" />}
                          <span>{activity.dataType}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-sm">
                        <div className="flex items-center space-x-2">
                          {activity.hashed ? (
                            <>
                              <Shield className="w-4 h-4 text-blue-400" />
                              <span className="text-blue-400">Yes</span>
                            </>
                          ) : (
                            <>
                              <AlertCircle className="w-4 h-4 text-yellow-400" />
                              <span className="text-yellow-400">No</span>
                            </>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-sm">
                        <div className="flex items-center space-x-2">
                          {activity.status === 'success' ? (
                            <>
                              <CheckCircle className="w-4 h-4 text-green-400" />
                              <span className="text-green-400">Success</span>
                            </>
                          ) : (
                            <>
                              <AlertCircle className="w-4 h-4 text-red-400" />
                              <span className="text-red-400">Failed</span>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
