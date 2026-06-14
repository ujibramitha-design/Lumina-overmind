'use client'

import { Globe, MapPin, Activity, TrendingUp, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { cn } from '@/lib/utils'

const areas = [
  { name: 'Serpong', score: 95, status: 'hot', leads: 342, growth: 23.5, left: '65%', top: '35%' },
  { name: 'Banten Pusat', score: 88, status: 'hot', leads: 289, growth: 18.2, left: '45%', top: '55%' },
  { name: 'Cipocok Jaya', score: 76, status: 'warm', leads: 198, growth: 12.8, left: '25%', top: '40%' },
  { name: 'Pakuhaji', score: 62, status: 'warm', leads: 145, growth: 8.4, left: '75%', top: '70%' },
]

export default function GeoIntelPage() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
              <Card className="overflow-hidden border-emerald-500/15 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="flex items-center gap-2 text-zinc-400">
                    <Globe className="h-4 w-4 text-emerald-400" />
                    Geo intelligence
                  </CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">Regional hot zone analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="relative h-[580px] overflow-hidden rounded-xl border border-zinc-800 bg-[linear-gradient(rgba(16,185,129,0.06)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.06)_1px,transparent_1px)] bg-[size:44px_44px]">
                    <div className="absolute left-1/2 top-1/2 h-80 w-80 -translate-x-1/2 -translate-y-1/2 rounded-full border border-emerald-500/20 bg-emerald-500/5" />
                    <div className="absolute left-1/2 top-1/2 h-56 w-72 -translate-x-1/2 -translate-y-1/2 rounded-[50%] border border-zinc-700 bg-black/40" />
                    {areas.map(area => (
                      <div
                        key={area.name}
                        className="absolute -translate-x-1/2 -translate-y-1/2"
                        style={{ left: area.left, top: area.top }}
                      >
                        <div
                          className={cn(
                            'h-3 w-3 rounded-full shadow-[0_0_14px_rgba(52,211,153,0.8)]',
                            area.status === 'hot' ? 'bg-emerald-400' : 'bg-amber-400'
                          )}
                        />
                        <div className="mt-2 rounded-lg border border-zinc-800 bg-black/70 px-2 py-1 text-[11px]">
                          <div className="text-zinc-100">{area.name}</div>
                          <div className="text-zinc-500">Score {area.score}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <div className="space-y-6">
                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">Top areas</CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Signal ranking</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {areas.map(area => (
                      <div key={area.name} className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="text-sm font-medium text-zinc-100">{area.name}</div>
                            <div className="text-xs text-zinc-500">{area.leads} leads</div>
                          </div>
                          <div className="text-right">
                            <div className="text-lg font-semibold text-emerald-400">{area.score}</div>
                            <div className="text-xs text-zinc-500">+{area.growth}%</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>

                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">Legend</CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Classification</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2 text-sm text-zinc-400">
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-emerald-400" />
                      Hot zone
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-amber-400" />
                      Warm zone
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-zinc-500" />
                      Cold zone
                    </div>
                    <div className="mt-4 rounded-xl border border-emerald-500/15 bg-emerald-500/5 p-4">
                      <div className="flex items-center gap-2 text-emerald-300">
                        <MapPin className="h-4 w-4" />
                        Tracking active
                      </div>
                      <div className="mt-2 text-xs text-zinc-500">
                        Geographic signals update in real time across tracked territories.
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
