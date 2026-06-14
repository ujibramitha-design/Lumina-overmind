'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Plus, Search, Filter, Phone, MapPin, TrendingUp } from 'lucide-react'

const leads = [
  {
    id: '1',
    business_name: 'Grand Serang Residence',
    contact: '628123456789',
    location: 'Serang',
    score: 92,
    status: 'Hot',
    priority: 'high',
    source: 'Facebook',
    date: '2024-01-15',
  },
  {
    id: '2',
    business_name: 'Banten Hills',
    contact: '628111222333',
    location: 'Tangerang',
    score: 78,
    status: 'Warm',
    priority: 'medium',
    source: 'Google',
    date: '2024-01-14',
  },
  {
    id: '3',
    business_name: 'Citra Indah',
    contact: '628222333444',
    location: 'Bandung',
    score: 61,
    status: 'Cold',
    priority: 'low',
    source: 'Organic',
    date: '2024-01-13',
  },
]

export default function LeadsPage() {
  const [query, setQuery] = useState('')
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <Card className="border-zinc-800 bg-zinc-950/90">
              <CardHeader className="flex flex-row items-center justify-between gap-4">
                <div>
                  <CardDescription className="text-zinc-400">Pipeline</CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">Lead management</CardTitle>
                </div>
                <Button className="bg-emerald-500 text-black hover:bg-emerald-400">
                  <Plus className="mr-2 h-4 w-4" />
                  Add lead
                </Button>
              </CardHeader>
              <CardContent>
                <div className="mb-6 flex flex-wrap gap-3">
                  <div className="flex min-w-[260px] flex-1 items-center gap-2 rounded-xl border border-zinc-800 bg-black/35 px-4">
                    <Search className="h-4 w-4 text-zinc-500" />
                    <Input
                      value={query}
                      onChange={e => setQuery(e.target.value)}
                      className="border-0 bg-transparent px-0 text-zinc-100 focus-visible:ring-0"
                      placeholder="Search leads..."
                    />
                  </div>
                  <Button variant="outline" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                    <Filter className="mr-2 h-4 w-4" />
                    Filter
                  </Button>
                </div>

                <div className="space-y-3">
                  {leads
                    .filter(
                      l =>
                        l.business_name.toLowerCase().includes(query.toLowerCase()) ||
                        l.location.toLowerCase().includes(query.toLowerCase())
                    )
                    .map(lead => (
                      <Card key={lead.id} className="border-zinc-800 bg-black/35">
                        <CardContent className="flex items-center justify-between p-4">
                          <div className="flex items-center gap-4">
                            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10 text-emerald-400">
                              <Phone className="h-5 w-5" />
                            </div>
                            <div>
                              <div className="font-medium text-zinc-100">{lead.business_name}</div>
                              <div className="flex items-center gap-3 text-sm text-zinc-500">
                                <span className="flex items-center gap-1">
                                  <MapPin className="h-3 w-3" />
                                  {lead.location}
                                </span>
                                <span>•</span>
                                <span>{lead.source}</span>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-4">
                            <div className="text-right">
                              <div className="flex items-center gap-2 text-emerald-400">
                                <TrendingUp className="h-4 w-4" />
                                {lead.score}
                              </div>
                              <div className="text-xs text-zinc-500">{lead.date}</div>
                            </div>
                            <Badge
                              className={
                                lead.status === 'Hot'
                                  ? 'bg-red-500/15 text-red-300'
                                  : lead.status === 'Warm'
                                  ? 'bg-amber-500/15 text-amber-300'
                                  : 'bg-zinc-800 text-zinc-300'
                              }
                            >
                              {lead.status}
                            </Badge>
                            <Button variant="outline" size="sm" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                              View
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                </div>
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </div>
  )
}
