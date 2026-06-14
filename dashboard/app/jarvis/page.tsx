'use client'

import { useState } from 'react'
import JarvisControlPanel from '@/components/JarvisControlPanel'
import JarvisAssistant from '@/components/JarvisAssistant'
import JarvisAnalyticsCharts from '@/components/JarvisAnalyticsCharts'
import JarvisNotifications from '@/components/JarvisNotifications'
import CommandHistory from '@/components/CommandHistory'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Brain, Mic, Activity, Zap, Shield, Database, Volume2, MessageSquare, ChevronDown, ChevronUp, BarChart3, Clock } from 'lucide-react'

const quickCards = [
  { title: 'Voice Commands', icon: Mic, text: 'Natural language control and command execution.' },
  { title: 'System Analytics', icon: Activity, text: 'Real-time performance and usage metrics.' },
  { title: 'AI Capabilities', icon: Zap, text: 'Function calling and system orchestration.' },
  { title: 'System Health', icon: Shield, text: 'Database, API, and resource monitoring.' },
]

const interactiveCommands = [
  { command: 'Berikan saya statistik sistem', icon: Activity },
  { command: 'Deploy hunter agent ke Serang', icon: Mic },
  { command: 'Berikan intelijen pasar', icon: Database },
  { command: 'Buat presentasi untuk Budi', icon: Volume2 },
]

export default function JarvisPage() {
  const [showChat, setShowChat] = useState(true)
  const [showCommands, setShowCommands] = useState(true)
  const [activeTab, setActiveTab] = useState('control')

  const handleQuickCommand = (command: string) => {
    // Dispatch custom event for JarvisAssistant to handle
    const event = new CustomEvent('jarvis-command', { detail: command })
    window.dispatchEvent(event)
  }

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
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Brain className="h-10 w-10 text-emerald-400" />
                    <div>
                      <CardTitle className="text-3xl text-zinc-100">J.A.R.V.I.S. Control Center</CardTitle>
                      <p className="text-sm text-zinc-500">Super Admin Voice Assistant</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <JarvisNotifications />
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setShowChat(!showChat)}
                      className="border-emerald-500/50 text-emerald-400 hover:bg-emerald-500/10"
                    >
                      <MessageSquare className="h-4 w-4 mr-2" />
                      {showChat ? 'Sembunyikan Chat' : 'Tampilkan Chat'}
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                  <TabsList className="grid w-full grid-cols-4 bg-zinc-900/50 border-zinc-800">
                    <TabsTrigger value="control" className="data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-400">
                      <Shield className="h-4 w-4 mr-2" />
                      Kontrol
                    </TabsTrigger>
                    <TabsTrigger value="analytics" className="data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-400">
                      <BarChart3 className="h-4 w-4 mr-2" />
                      Analytics
                    </TabsTrigger>
                    <TabsTrigger value="commands" className="data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-400">
                      <Volume2 className="h-4 w-4 mr-2" />
                      Perintah
                    </TabsTrigger>
                    <TabsTrigger value="history" className="data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-400">
                      <Clock className="h-4 w-4 mr-2" />
                      Riwayat
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="control" className="space-y-6 mt-6">
                    <JarvisControlPanel />
                    
                    {/* Interactive Chat Interface */}
                    {showChat && (
                      <div className="border-t border-zinc-800 pt-6">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-lg font-semibold text-zinc-100 flex items-center gap-2">
                            <MessageSquare className="h-5 w-5 text-emerald-400" />
                            Chat Interaktif
                          </h3>
                        </div>
                        <div className="h-[400px] border border-zinc-800 rounded-lg bg-black/35 overflow-hidden">
                          <JarvisAssistant />
                        </div>
                      </div>
                    )}
                    
                    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                      {quickCards.map(item => {
                        const Icon = item.icon
                        return (
                          <Card key={item.title} className="border-zinc-800 bg-black/35 hover:border-emerald-500/30 transition-colors cursor-pointer">
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
                  </TabsContent>

                  <TabsContent value="analytics" className="mt-6">
                    <JarvisAnalyticsCharts />
                  </TabsContent>

                  <TabsContent value="commands" className="space-y-6 mt-6">
                    <div className="grid gap-6 lg:grid-cols-2">
                      {/* Interactive Quick Commands */}
                      <Card className="border-zinc-800 bg-black/35">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <CardTitle className="flex items-center gap-2 text-zinc-100">
                              <Volume2 className="h-4 w-4 text-emerald-400" />
                              Perintah Cepat
                            </CardTitle>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => setShowCommands(!showCommands)}
                              className="text-zinc-400 hover:text-zinc-100"
                            >
                              {showCommands ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                            </Button>
                          </div>
                        </CardHeader>
                        {showCommands && (
                          <CardContent className="space-y-2">
                            {interactiveCommands.map((item, index) => {
                              const Icon = item.icon
                              return (
                                <Button
                                  key={index}
                                  variant="outline"
                                  className="w-full justify-start border-zinc-700 bg-black/35 text-zinc-300 hover:text-zinc-100 hover:border-emerald-500/50 hover:bg-emerald-500/10 transition-all"
                                  onClick={() => handleQuickCommand(item.command)}
                                >
                                  <Icon className="h-4 w-4 mr-2 text-emerald-400" />
                                  <span className="text-sm">{item.command}</span>
                                </Button>
                              )
                            })}
                          </CardContent>
                        )}
                      </Card>

                      {/* Database Intelligence */}
                      <Card className="border-zinc-800 bg-black/35">
                        <CardHeader>
                          <CardTitle className="flex items-center gap-2 text-zinc-100">
                            <Database className="h-4 w-4 text-emerald-400" />
                            Intelijen Database
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="text-sm text-zinc-400">
                          Statistik lead, analisis, dan monitoring kesehatan database.
                        </CardContent>
                      </Card>

                      {/* System Status */}
                      <Card className="border-zinc-800 bg-black/35">
                        <CardHeader>
                          <CardTitle className="flex items-center gap-2 text-zinc-100">
                            <Shield className="h-4 w-4 text-emerald-400" />
                            Status Sistem
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3 text-sm">
                          <div className="flex items-center justify-between">
                            <span className="text-zinc-400">Database</span>
                            <span className="text-emerald-400">Online</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-zinc-400">API</span>
                            <span className="text-emerald-400">Online</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-zinc-400">Memory</span>
                            <span className="text-blue-400">Normal</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-zinc-400">CPU</span>
                            <span className="text-blue-400">Normal</span>
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </TabsContent>

                  <TabsContent value="history" className="mt-6">
                    <CommandHistory />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </div>
  )
}
