'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import {
  ArrowLeft,
  Phone,
  Mail,
  MapPin,
  Globe,
  Clock,
  FileText,
  Send,
  Users,
  Activity,
  Target,
  TrendingUp,
  AlertCircle,
} from 'lucide-react'
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'

// Types
interface Lead {
  id: number
  business_name: string
  contact: string
  phone?: string
  email?: string
  url?: string
  keywords?: string
  source?: string
  score?: number
  location?: string
  city?: string
  status?: string
  priority?: string
  property_type?: string
  price_range?: string
  bedrooms?: number
  bathrooms?: number
  land_size?: number
  building_size?: number
  year_built?: number
  description?: string
  date_found?: string
  last_contacted?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

interface AIReasoning {
  intent: number
  budget: number
  urgency: number
  fit: number
  authority: number
}

interface TimelineActivity {
  id: string
  activity: string
  timestamp: string
  type: 'discovery' | 'validation' | 'extraction' | 'analysis' | 'contact'
  details?: string
}

interface LeadDetailResponse {
  success: boolean
  data: Lead & {
    ai_reasoning: AIReasoning
    timeline: TimelineActivity[]
  }
  message?: string
}

// Loading Animation Component
const HackerLoading = () => {
  const [dots, setDots] = useState('')

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => (prev.length >= 3 ? '' : prev + '.'))
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="text-center">
        <div className="mb-8">
          <div className="w-16 h-16 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
        </div>
        <div className="text-emerald-400 font-mono text-lg">ACCESSING LEAD INTELLIGENCE{dots}</div>
        <div className="text-zinc-500 font-mono text-sm mt-2">Decrypting 360° profile data...</div>
      </div>
    </div>
  )
}

// Score Badge Component
const ScoreBadge = ({ score }: { score?: number }) => {
  if (!score) return null

  let color = 'bg-zinc-800 text-zinc-300'
  let label = 'Unknown'

  if (score >= 8) {
    color = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
    label = 'HOT'
  } else if (score >= 6) {
    color = 'bg-amber-500/20 text-amber-400 border-amber-500/30'
    label = 'WARM'
  } else {
    color = 'bg-blue-500/20 text-blue-400 border-blue-500/30'
    label = 'COLD'
  }

  return (
    <div className={`px-3 py-1 rounded-full border text-xs font-bold ${color}`}>
      {label} • {score.toFixed(1)}/10
    </div>
  )
}

// Timeline Item Component
const TimelineItem = ({ activity, timestamp, type }: TimelineActivity) => {
  const getActivityIcon = () => {
    switch (type) {
      case 'discovery':
        return <Target className="w-4 h-4" />
      case 'validation':
        return <AlertCircle className="w-4 h-4" />
      case 'extraction':
        return <FileText className="w-4 h-4" />
      case 'analysis':
        return <TrendingUp className="w-4 h-4" />
      case 'contact':
        return <Send className="w-4 h-4" />
      default:
        return <Activity className="w-4 h-4" />
    }
  }

  return (
    <div className="relative pl-6 pb-6 last:pb-0">
      {/* Vertical line */}
      <div className="absolute left-2 top-6 bottom-0 w-px border-l border-zinc-800"></div>

      {/* Dot */}
      <div className="absolute left-0 top-2 w-4 h-4 bg-emerald-500 rounded-full flex items-center justify-center">
        <div className="w-2 h-2 bg-black rounded-full"></div>
      </div>

      {/* Content */}
      <div className="ml-6">
        <div className="flex items-center gap-2 mb-1">
          <div className="text-emerald-400">{getActivityIcon()}</div>
          <div className="text-zinc-100 font-medium">{activity}</div>
        </div>
        <div className="text-zinc-500 text-sm">
          {new Date(timestamp).toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
          })}
        </div>
      </div>
    </div>
  )
}

// Main Component
export default function LeadDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [lead, setLead] = useState<LeadDetailResponse['data'] | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchLead() {
      try {
        const response = await fetch(`/api/leads/${params.id}`)
        const data: LeadDetailResponse = await response.json()

        if (data.success) {
          setLead(data.data)
        } else {
          setError(data.message || 'Failed to load lead data')
        }
      } catch (err) {
        setError('Network error occurred')
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchLead()
    }
  }, [params.id])

  if (loading) {
    return <HackerLoading />
  }

  if (error || !lead) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">⚠️ Intelligence Access Failed</div>
          <div className="text-zinc-400 mb-6">{error}</div>
          <Link href="/" className="text-emerald-400 hover:text-emerald-300 transition-colors">
            ← Back to Command Center
          </Link>
        </div>
      </div>
    )
  }

  // Prepare radar chart data
  const radarData = [
    { subject: 'Intent', value: lead.ai_reasoning.intent, fullMark: 100 },
    { subject: 'Budget', value: lead.ai_reasoning.budget, fullMark: 100 },
    { subject: 'Urgency', value: lead.ai_reasoning.urgency, fullMark: 100 },
    { subject: 'Fit', value: lead.ai_reasoning.fit, fullMark: 100 },
    { subject: 'Authority', value: lead.ai_reasoning.authority, fullMark: 100 },
  ]

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="border-b border-zinc-800 bg-zinc-950/50">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="flex items-center gap-2 text-zinc-400 hover:text-emerald-400 transition-colors">
                <ArrowLeft className="w-4 h-4" />
                Back to Command Center
              </Link>
            </div>

            <div className="flex items-center gap-4">
              <div>
                <h1 className="text-2xl font-bold text-zinc-100">{lead.business_name}</h1>
                <div className="flex items-center gap-2 mt-1">
                  <ScoreBadge score={lead.score} />
                  <span className="text-zinc-500 text-sm">ID: #{lead.id}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left Column - Intelligence Desk */}
          <div className="space-y-6">
            {/* Contact Details */}
            <div className="bg-zinc-950/50 border border-zinc-800 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Users className="w-5 h-5 text-emerald-400" />
                <h2 className="text-lg font-semibold text-zinc-100">Intelligence Desk</h2>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <Phone className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Phone</div>
                    <div className="text-zinc-100 text-sm">{lead.phone || 'N/A'}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <Mail className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Email</div>
                    <div className="text-zinc-100 text-sm">{lead.email || 'N/A'}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <MapPin className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Location</div>
                    <div className="text-zinc-100 text-sm">{lead.location || 'N/A'}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <Globe className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Source</div>
                    <div className="text-zinc-100 text-sm">{lead.source || 'N/A'}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <Target className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Property Type</div>
                    <div className="text-zinc-100 text-sm">{lead.property_type || 'N/A'}</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-zinc-800 rounded flex items-center justify-center">
                    <TrendingUp className="w-4 h-4 text-zinc-400" />
                  </div>
                  <div>
                    <div className="text-zinc-500 text-xs">Price Range</div>
                    <div className="text-zinc-100 text-sm">{lead.price_range || 'N/A'}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Desk */}
            <div className="bg-zinc-950/50 border border-zinc-800 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-4">
                <Activity className="w-5 h-5 text-emerald-400" />
                <h2 className="text-lg font-semibold text-zinc-100">Action Desk</h2>
              </div>

              <div className="space-y-3">
                <button className="w-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 py-3 px-4 rounded-lg hover:bg-emerald-500/20 transition-colors flex items-center justify-center gap-2">
                  <FileText className="w-4 h-4" />
                  Generate Pitch Deck
                </button>

                <button className="w-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 py-3 px-4 rounded-lg hover:bg-emerald-500/20 transition-colors flex items-center justify-center gap-2">
                  <Send className="w-4 h-4" />
                  Send Auto-Email
                </button>

                <button className="w-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 py-3 px-4 rounded-lg hover:bg-emerald-500/20 transition-colors flex items-center justify-center gap-2">
                  <Users className="w-4 h-4" />
                  Handover to Closer
                </button>
              </div>
            </div>
          </div>

          {/* Middle Column - AI Reasoning */}
          <div className="space-y-6">
            <div className="bg-zinc-950/50 border border-zinc-800 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-6">
                <Target className="w-5 h-5 text-emerald-400" />
                <h2 className="text-lg font-semibold text-zinc-100">AI Reasoning</h2>
              </div>

              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#27272a" strokeDasharray="3 3" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#71717a', fontSize: 12 }} />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#52525b', fontSize: 10 }} />
                    <Radar
                      name="Score"
                      dataKey="value"
                      stroke="#10b981"
                      fill="#10b981"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              {/* AI Metrics */}
              <div className="grid grid-cols-2 gap-4 mt-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-400">{lead.ai_reasoning.intent}</div>
                  <div className="text-xs text-zinc-500">Intent</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-400">{lead.ai_reasoning.budget}</div>
                  <div className="text-xs text-zinc-500">Budget</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-400">{lead.ai_reasoning.urgency}</div>
                  <div className="text-xs text-zinc-500">Urgency</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-400">{lead.ai_reasoning.fit}</div>
                  <div className="text-xs text-zinc-500">Fit</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Activity Timeline */}
          <div className="space-y-6">
            <div className="bg-zinc-950/50 border border-zinc-800 rounded-lg p-6">
              <div className="flex items-center gap-2 mb-6">
                <Clock className="w-5 h-5 text-emerald-400" />
                <h2 className="text-lg font-semibold text-zinc-100">Activity Timeline</h2>
              </div>

              <div className="space-y-2">
                {lead.timeline.map(activity => (
                  <TimelineItem key={activity.id} {...activity} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
