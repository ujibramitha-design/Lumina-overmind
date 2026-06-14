'use client'

import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BarChart3, DollarSign, Play, Pause, TrendingUp, Target } from 'lucide-react'

const campaigns = [
  { name: 'Summer Sale Campaign', platform: 'Facebook', status: 'running', budget: 5000, spent: 3420, leads: 67 },
  { name: 'Banten Property Leads', platform: 'Google', status: 'running', budget: 8000, spent: 6100, leads: 89 },
  { name: 'Retargeting Campaign', platform: 'Google', status: 'paused', budget: 4000, spent: 2800, leads: 45 },
]

export default function GrowthPage() {
  const totalSpend = campaigns.reduce((sum, c) => sum + c.spent, 0)
  const totalLeads = campaigns.reduce((sum, c) => sum + c.leads, 0)
  const cpl = Math.round((totalSpend / totalLeads) * 100) / 100

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="grid gap-6 xl:grid-cols-4">
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Spend</CardDescription>
                  <CardTitle className="text-2xl text-emerald-400">${totalSpend.toLocaleString()}</CardTitle>
                </CardHeader>
              </Card>
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">CPL</CardDescription>
                  <CardTitle className="text-2xl text-sky-400">${cpl}</CardTitle>
                </CardHeader>
              </Card>
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Leads</CardDescription>
                  <CardTitle className="text-2xl text-amber-400">{totalLeads}</CardTitle>
                </CardHeader>
              </Card>
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Trend</CardDescription>
                  <CardTitle className="text-2xl text-zinc-100 flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-emerald-400" />
                    +18%
                  </CardTitle>
                </CardHeader>
              </Card>
            </div>

            <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Performance</CardDescription>
                  <CardTitle className="text-xl text-zinc-100">Channel ROI overview</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {[
                    ['Facebook Ads', 245],
                    ['Google Ads', 189],
                    ['Organic SEO', 412],
                  ].map(([name, value]) => (
                    <div key={name as string} className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                      <div className="flex items-center justify-between text-sm">
                        <span>{name}</span>
                        <span className="text-emerald-400">{value}% ROI</span>
                      </div>
                      <div className="mt-3 h-2 rounded-full bg-zinc-800">
                        <div
                          className="h-2 rounded-full bg-gradient-to-r from-emerald-500 to-emerald-300"
                          style={{ width: `${Math.min(Number(value), 100)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Actions</CardDescription>
                  <CardTitle className="text-xl text-zinc-100">Campaign control</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {campaigns.map(c => (
                    <div key={c.name} className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="text-sm font-medium text-zinc-100">{c.name}</div>
                          <div className="text-xs text-zinc-500">{c.platform}</div>
                        </div>
                        <div className="text-right text-xs text-zinc-400">{c.leads} leads</div>
                      </div>
                      <div className="mt-3 flex gap-2">
                        <Button variant="outline" size="sm" className="border-zinc-700 bg-zinc-900 text-zinc-100" aria-label={`Pause ${c.name} campaign`}>
                          <Pause className="mr-2 h-3 w-3" />
                          Pause
                        </Button>
                        <Button variant="outline" size="sm" className="border-zinc-700 bg-zinc-900 text-zinc-100" aria-label={`Resume ${c.name} campaign`}>
                          <Play className="mr-2 h-3 w-3" />
                          Resume
                        </Button>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
