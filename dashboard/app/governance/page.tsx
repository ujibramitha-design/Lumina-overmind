'use client'

import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ShieldAlert } from 'lucide-react'
import { TerminalLogs } from '@/components/TerminalLogs'

export default function GovernancePage() {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8 space-y-6">
            <Card className="border-zinc-800 bg-zinc-950/90">
              <CardHeader>
                <CardDescription className="flex items-center gap-2 text-zinc-400">
                  <ShieldAlert className="h-4 w-4 text-emerald-400" />
                  Security terminal
                </CardDescription>
                <CardTitle className="text-2xl text-zinc-100">Governance & security</CardTitle>
              </CardHeader>
              <CardContent>
                <TerminalLogs />
              </CardContent>
            </Card>

            <div className="grid gap-4 md:grid-cols-3">
              {[
                ['System Uptime', '14d 7h 32m', '99.8% availability'],
                ['Active Crisis Alerts', '3', '2 critical, 1 warning'],
                ['Compliance Rate', '94.2%', '+2.3% from last audit'],
              ].map(([title, value, desc]) => (
                <Card key={title} className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">{title}</CardDescription>
                    <CardTitle className="text-2xl text-zinc-100">{value}</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm text-zinc-500">{desc}</CardContent>
                </Card>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
