'use client'

import React from 'react'
import Link from 'next/link'
import {
  ArrowUpRight,
  Bell,
  Clock3,
  Globe2,
  Layers3,
  MapPin,
  Search,
  ShieldCheck,
  Sparkles,
  Target,
  TrendingUp,
  Users,
} from 'lucide-react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'

type MetricProps = {
  label: string
  value: string
  delta: string
  tone?: 'emerald' | 'zinc' | 'amber' | 'blue'
}

function MetricCard({ label, value, delta, tone = 'emerald' }: MetricProps) {
  const toneClass = {
    emerald: 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400',
    zinc: 'border-zinc-700 bg-zinc-900 text-zinc-200',
    amber: 'border-amber-500/20 bg-amber-500/5 text-amber-400',
    blue: 'border-sky-500/20 bg-sky-500/5 text-sky-400',
  }[tone]

  return (
    <Card className={cn('rounded-xl border shadow-[0_0_0_1px_rgba(39,39,42,0.7)]', toneClass)}>
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-[11px] uppercase tracking-[0.18em] text-zinc-500">{label}</div>
            <div className="mt-2 text-2xl font-semibold text-zinc-100">{value}</div>
          </div>
          <div className="rounded-full border border-white/10 bg-black/30 p-2">
            <ArrowUpRight className="h-4 w-4 text-emerald-400" />
          </div>
        </div>
        <div className="mt-3 text-xs text-zinc-500">{delta}</div>
      </CardContent>
    </Card>
  )
}

function GeoCanvas() {
  const markers = [
    { top: '24%', left: '19%', label: 'JKT', size: 'h-2 w-2' },
    { top: '38%', left: '51%', label: 'SG', size: 'h-2.5 w-2.5' },
    { top: '54%', left: '63%', label: 'MY', size: 'h-2 w-2' },
    { top: '63%', left: '77%', label: 'ID', size: 'h-3 w-3' },
    { top: '33%', left: '84%', label: 'AU', size: 'h-2 w-2' },
  ]

  return (
    <Card className="relative overflow-hidden border-emerald-500/15 bg-zinc-950/90 shadow-[0_0_30px_rgba(16,185,129,0.08)]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_45%),linear-gradient(180deg,rgba(255,255,255,0.02),transparent)]" />
      <CardHeader className="relative">
        <CardDescription className="flex items-center gap-2 text-zinc-400">
          <Globe2 className="h-4 w-4 text-emerald-400" />
          Geo intelligence
        </CardDescription>
        <CardTitle className="text-xl text-zinc-100">Tracked demand by region</CardTitle>
      </CardHeader>
      <CardContent className="relative">
        <div className="relative h-[360px] overflow-hidden rounded-xl border border-zinc-800 bg-[linear-gradient(rgba(16,185,129,0.06)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.06)_1px,transparent_1px)] bg-[size:42px_42px]">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.16),transparent_35%)]" />
          <div
            className="absolute inset-0 opacity-30"
            style={{
              backgroundImage:
                'linear-gradient(transparent 48%, rgba(16,185,129,0.35) 49%, rgba(16,185,129,0.35) 51%, transparent 52%)',
              backgroundSize: '100% 24%',
            }}
          />
          <div className="absolute left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 rounded-full border border-emerald-500/20 bg-emerald-500/5 blur-0 shadow-[0_0_100px_rgba(16,185,129,0.12)]" />
          <div className="absolute left-1/2 top-1/2 h-56 w-56 -translate-x-1/2 -translate-y-1/2 rounded-full border border-zinc-700/70 bg-black/40" />
          <div className="absolute left-1/2 top-1/2 h-40 w-72 -translate-x-1/2 -translate-y-1/2 rounded-[50%] border border-emerald-500/20 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.18),rgba(0,0,0,0.6)_72%)]" />
          {markers.map(marker => (
            <div
              key={marker.label}
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ top: marker.top, left: marker.left }}
            >
              <div className="relative">
                <div
                  className={cn('rounded-full bg-emerald-400 shadow-[0_0_14px_rgba(52,211,153,0.9)]', marker.size)}
                />
                <div className="absolute -inset-2 rounded-full border border-emerald-400/40" />
              </div>
              <div className="mt-2 text-[10px] font-medium tracking-[0.22em] text-emerald-300">{marker.label}</div>
            </div>
          ))}
          <div className="absolute bottom-4 left-4 right-4 grid grid-cols-3 gap-2 text-xs">
            <div className="rounded-lg border border-zinc-800 bg-black/60 p-3">
              <div className="text-zinc-500">Active regions</div>
              <div className="mt-1 text-base font-semibold text-zinc-100">12</div>
            </div>
            <div className="rounded-lg border border-zinc-800 bg-black/60 p-3">
              <div className="text-zinc-500">Geo hits</div>
              <div className="mt-1 text-base font-semibold text-zinc-100">248</div>
            </div>
            <div className="rounded-lg border border-zinc-800 bg-black/60 p-3">
              <div className="text-zinc-500">Risk score</div>
              <div className="mt-1 text-base font-semibold text-emerald-400">Low</div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default function DashboardWorkspace() {
  const modules = [
    {
      title: 'Live Radar',
      description: 'Active prospect scan across regions',
      icon: Target,
      href: '/geo-intel',
      badge: 'LIVE',
    },
    { title: 'Inbox Queue', description: 'Messages waiting for response', icon: Bell, href: '/inbox', badge: '14' },
    {
      title: 'Growth Engine',
      description: 'Campaign and conversion tracking',
      icon: TrendingUp,
      href: '/growth',
      badge: '+18%',
    },
    {
      title: 'Governance',
      description: 'Compliance, logs, and control',
      icon: ShieldCheck,
      href: '/governance',
      badge: 'SECURE',
    },
  ]

  const activity = [
    ['Lead #1842', 'Jakarta', 'Hot', '2m ago'],
    ['Lead #1731', 'Surabaya', 'Warm', '12m ago'],
    ['Lead #1670', 'Bandung', 'Cold', '28m ago'],
    ['Lead #1612', 'Singapore', 'Hot', '41m ago'],
  ]

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.14),transparent_38%),linear-gradient(180deg,#020617_0%,#09090b_35%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />

          <main className="min-w-0 flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-[1600px] space-y-6">
              <section className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
                <Card className="overflow-hidden border-emerald-500/15 bg-zinc-950/90 shadow-[0_0_30px_rgba(16,185,129,0.06)]">
                  <CardContent className="p-6 sm:p-8">
                    <div className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.22em] text-zinc-500">
                      <Sparkles className="h-4 w-4 text-emerald-400" />
                      Tactical intelligence workspace
                    </div>
                    <h1 className="mt-4 max-w-3xl text-3xl font-semibold tracking-tight text-zinc-50 sm:text-4xl">
                      Command panel for leads, geo-tracking, and conversion flow.
                    </h1>
                    <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">
                      A dark tactical enterprise surface built around the same language as the auth page: clean, secure,
                      high contrast, and focused on operational signals.
                    </p>

                    <div className="mt-6 flex flex-wrap gap-3">
                      <div className="flex min-w-[240px] flex-1 items-center gap-3 rounded-xl border border-zinc-800 bg-black/40 px-4 py-3">
                        <Search className="h-4 w-4 text-zinc-500" />
                        <Input
                          aria-label="Search intelligence"
                          placeholder="Search leads, regions, campaigns..."
                          className="h-8 border-0 bg-transparent p-0 text-zinc-100 placeholder:text-zinc-600 focus-visible:ring-0"
                        />
                      </div>
                      <Button className="h-12 bg-emerald-500 px-5 font-semibold text-black hover:bg-emerald-400">
                        Open scanner
                      </Button>
                      <Button
                        variant="outline"
                        className="h-12 border-zinc-700 bg-zinc-900/70 px-5 text-zinc-100 hover:bg-zinc-800"
                      >
                        Export report
                      </Button>
                    </div>

                    <div className="mt-6 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                      <MetricCard label="Total leads" value="1,284" delta="+12% from last week" />
                      <MetricCard label="Hot prospects" value="214" delta="+34 new this cycle" tone="amber" />
                      <MetricCard
                        label="Geo coverage"
                        value="18 regions"
                        delta="Indonesia, SEA, and APAC"
                        tone="blue"
                      />
                      <MetricCard label="Close rate" value="27.4%" delta="+4.1 points" tone="zinc" />
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="flex items-center gap-2 text-zinc-400">
                      <Clock3 className="h-4 w-4 text-emerald-400" />
                      Live activity
                    </CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Recent operations</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {activity.map(([lead, region, status, time]) => (
                      <div
                        key={`${lead}-${time}`}
                        className="flex items-center justify-between rounded-xl border border-zinc-800 bg-black/40 px-4 py-3"
                      >
                        <div>
                          <div className="text-sm font-medium text-zinc-100">{lead}</div>
                          <div className="text-xs text-zinc-500">{region}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs uppercase tracking-[0.2em] text-emerald-400">{status}</div>
                          <div className="text-xs text-zinc-500">{time}</div>
                        </div>
                      </div>
                    ))}
                    <div className="rounded-xl border border-emerald-500/15 bg-emerald-500/5 p-4">
                      <div className="text-xs uppercase tracking-[0.2em] text-emerald-300">System status</div>
                      <div className="mt-2 flex items-center justify-between">
                        <div>
                          <div className="text-lg font-semibold text-zinc-100">Online</div>
                          <div className="text-xs text-zinc-500">All core services responsive</div>
                        </div>
                        <div className="rounded-full border border-emerald-400/30 px-3 py-1 text-xs text-emerald-300">
                          Stable
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </section>

              <section className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
                <GeoCanvas />

                <div className="space-y-6">
                  <Card className="border-zinc-800 bg-zinc-950/90">
                    <CardHeader>
                      <CardDescription className="text-zinc-400">Modules</CardDescription>
                      <CardTitle className="text-xl text-zinc-100">Primary workspaces</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {modules.map(item => {
                        const Icon = item.icon
                        return (
                          <Link
                            key={item.title}
                            href={item.href}
                            className="flex items-center justify-between rounded-xl border border-zinc-800 bg-black/35 px-4 py-3 transition-colors hover:border-emerald-500/30 hover:bg-zinc-900/70"
                          >
                            <div className="flex items-center gap-3">
                              <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-2">
                                <Icon className="h-4 w-4 text-emerald-400" />
                              </div>
                              <div>
                                <div className="text-sm font-medium text-zinc-100">{item.title}</div>
                                <div className="text-xs text-zinc-500">{item.description}</div>
                              </div>
                            </div>
                            <span className="rounded-full border border-emerald-500/20 bg-emerald-500/5 px-2.5 py-1 text-[11px] uppercase tracking-[0.18em] text-emerald-300">
                              {item.badge}
                            </span>
                          </Link>
                        )
                      })}
                    </CardContent>
                  </Card>

                  <Card className="border-zinc-800 bg-zinc-950/90">
                    <CardHeader>
                      <CardDescription className="text-zinc-400">Signal queue</CardDescription>
                      <CardTitle className="text-xl text-zinc-100">Lead status by region</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {[
                        { region: 'Jakarta', count: 382, fill: 'w-[78%]' },
                        { region: 'West Java', count: 241, fill: 'w-[61%]' },
                        { region: 'East Java', count: 173, fill: 'w-[47%]' },
                        { region: 'Overseas', count: 96, fill: 'w-[28%]' },
                      ].map(row => (
                        <div key={row.region} className="space-y-2 rounded-xl border border-zinc-800 bg-black/35 p-4">
                          <div className="flex items-center justify-between text-sm">
                            <span className="text-zinc-200">{row.region}</span>
                            <span className="text-zinc-500">{row.count} signals</span>
                          </div>
                          <div className="h-2 overflow-hidden rounded-full bg-zinc-800">
                            <div
                              className={cn(
                                'h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-300',
                                row.fill
                              )}
                            />
                          </div>
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                </div>
              </section>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
