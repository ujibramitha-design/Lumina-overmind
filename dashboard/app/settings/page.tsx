'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Cpu, AlertTriangle, Zap, Database, RefreshCw } from 'lucide-react'

export default function SettingsPage() {
  const [warmKeywords, setWarmKeywords] = useState('KPR, cicilan, survei, harga, lokasi, beli, booking, DP')
  const [coldKeywords, setColdKeywords] = useState('tanya, info, detail, spek, fasilitas, kapan, nanti, cek')

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="flex items-center gap-2 text-zinc-400">
                    <Cpu className="h-4 w-4 text-emerald-400" />
                    AI controls
                  </CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                    <div className="mb-2 text-sm text-zinc-300">Warm keywords</div>
                    <Textarea
                      value={warmKeywords}
                      onChange={e => setWarmKeywords(e.target.value)}
                      className="min-h-[110px] border-zinc-700 bg-zinc-900 text-zinc-100"
                    />
                  </div>
                  <div className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                    <div className="mb-2 text-sm text-zinc-300">Cold keywords</div>
                    <Textarea
                      value={coldKeywords}
                      onChange={e => setColdKeywords(e.target.value)}
                      className="min-h-[110px] border-zinc-700 bg-zinc-900 text-zinc-100"
                    />
                  </div>
                </CardContent>
              </Card>

              <div className="space-y-6">
                <Card className="border-red-500/20 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="flex items-center gap-2 text-zinc-400">
                      <AlertTriangle className="h-4 w-4 text-red-400" />
                      Danger zone
                    </CardDescription>
                    <CardTitle className="text-xl text-zinc-100">System actions</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <Button
                      variant="outline"
                      className="w-full justify-start border-red-500/30 bg-red-500/5 text-red-300 hover:bg-red-500/10"
                      aria-label="Purge system cache"
                    >
                      <RefreshCw className="mr-2 h-4 w-4" />
                      Purge cache
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start border-red-500/30 bg-red-500/5 text-red-300 hover:bg-red-500/10"
                      aria-label="Reset database to initial state"
                    >
                      <Database className="mr-2 h-4 w-4" />
                      Reset database
                    </Button>
                  </CardContent>
                </Card>

                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">Deploy</CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Publish configuration</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button className="w-full bg-emerald-500 text-black hover:bg-emerald-400" aria-label="Deploy new AI configuration">
                      <Zap className="mr-2 h-4 w-4" />
                      Deploy new AI config
                    </Button>
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Badge className="bg-emerald-500/15 text-emerald-300">System online</Badge>
                      <Badge className="bg-zinc-800 text-zinc-300">Cache active</Badge>
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
