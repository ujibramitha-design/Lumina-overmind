'use client'

import JarvisControlPanel from '@/components/JarvisControlPanel'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, Mic, Activity, Zap, Shield, Database, Volume2 } from 'lucide-react'

const quickCards = [
  { title: 'Voice Commands', icon: Mic, text: 'Natural language control and command execution.' },
  { title: 'System Analytics', icon: Activity, text: 'Real-time performance and usage metrics.' },
  { title: 'AI Capabilities', icon: Zap, text: 'Function calling and system orchestration.' },
  { title: 'System Health', icon: Shield, text: 'Database, API, and resource monitoring.' },
]

export default function JarvisPage() {
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
              <CardHeader className="space-y-2">
                <div className="flex items-center gap-3">
                  <Brain className="h-10 w-10 text-emerald-400" />
                  <div>
                    <CardTitle className="text-3xl text-zinc-100">J.A.R.V.I.S. Control Center</CardTitle>
                    <p className="text-sm text-zinc-500">Super Admin Voice Assistant</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <JarvisControlPanel />
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                  {quickCards.map(item => {
                    const Icon = item.icon
                    return (
                      <Card key={item.title} className="border-zinc-800 bg-black/35">
                        <CardHeader className="pb-3">
                          <CardTitle className="flex items-center gap-2 text-lg text-zinc-100">
                            <Icon className="h-5 w-5 text-emerald-400" />
                            {item.title}
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="text-sm text-zinc-400">{item.text}</CardContent>
                      </Card>
                    )
                  })}
                </div>
                <div className="grid gap-4 xl:grid-cols-2">
                  <Card className="border-zinc-800 bg-black/35">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-zinc-100">
                        <Database className="h-4 w-4 text-emerald-400" />
                        Database intelligence
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="text-sm text-zinc-400">
                      Lead statistics, analysis, and database health monitoring.
                    </CardContent>
                  </Card>
                  <Card className="border-zinc-800 bg-black/35">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2 text-zinc-100">
                        <Volume2 className="h-4 w-4 text-emerald-400" />
                        Command examples
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm text-zinc-400">
                      <div>"Berikan saya statistik sistem"</div>
                      <div>"Deploy hunter agent ke Serang"</div>
                      <div>"Buat presentasi untuk Budi"</div>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </div>
  )
}
