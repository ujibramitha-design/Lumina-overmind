'use client'

import { useMemo, useState } from 'react'
import { Bot, Send, MessageCircle, Search, Sparkles, Phone, TrendingUp } from 'lucide-react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'

const leads = [
  {
    id: 1,
    business_name: 'Grand Serang Residence',
    location: 'Serang',
    score: 92,
    status: 'Hot',
    contact: 'Phone: 628123456789',
    message: 'Follow up tonight with a soft close.',
  },
  {
    id: 2,
    business_name: 'Banten Hills',
    location: 'Tangerang',
    score: 78,
    status: 'Warm',
    contact: 'Phone: 628111222333',
    message: 'Send brochure and ask for budget range.',
  },
  {
    id: 3,
    business_name: 'Citra Indah',
    location: 'Bandung',
    score: 61,
    status: 'Cold',
    contact: 'Phone: 628222333444',
    message: 'Nurture and wait for interest signal.',
  },
]

export default function InboxPage() {
  const [selectedId, setSelectedId] = useState(1)
  const [draft, setDraft] = useState(leads[0].message)
  const selectedLead = useMemo(() => leads.find(lead => lead.id === selectedId) || leads[0], [selectedId])

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="grid h-[calc(100vh-8rem)] grid-cols-12 gap-6">
              <Card className="col-span-12 xl:col-span-3 border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="flex items-center gap-2 text-zinc-400">
                    <Search className="h-4 w-4 text-emerald-400" />
                    Lead queue
                  </CardDescription>
                  <CardTitle className="text-xl text-zinc-100">AI drafts</CardTitle>
                </CardHeader>
                <CardContent className="p-0">
                  <ScrollArea className="h-[calc(100vh-15rem)]">
                    <div className="space-y-2 p-4">
                      {leads.map(lead => (
                        <button
                          key={lead.id}
                          onClick={() => {
                            setSelectedId(lead.id)
                            setDraft(lead.message)
                          }}
                          className={`w-full rounded-xl border p-4 text-left transition-colors ${selectedId === lead.id ? 'border-emerald-500 bg-emerald-500/10' : 'border-zinc-800 bg-black/35 hover:border-zinc-700'}`}
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div>
                              <div className="text-sm font-medium text-zinc-100">{lead.business_name}</div>
                              <div className="text-xs text-zinc-500">{lead.location}</div>
                            </div>
                            <Badge className="bg-emerald-500/15 text-emerald-300">{lead.status}</Badge>
                          </div>
                          <div className="mt-3 text-xs text-zinc-500">Score {lead.score}</div>
                        </button>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>

              <Card className="col-span-12 xl:col-span-6 border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Review desk</CardDescription>
                  <CardTitle className="text-xl text-zinc-100">{selectedLead.business_name}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="rounded-xl border border-zinc-800 bg-black/35 p-4">
                    <textarea
                      value={draft}
                      onChange={e => setDraft(e.target.value)}
                      className="min-h-[340px] w-full resize-none bg-transparent text-sm text-zinc-100 outline-none placeholder:text-zinc-600"
                    />
                  </div>
                  <div className="flex gap-3">
                    <Button className="h-12 flex-1 bg-emerald-500 text-black hover:bg-emerald-400">
                      <Send className="mr-2 h-4 w-4" />
                      Approve & send
                    </Button>
                    <Button
                      variant="outline"
                      className="h-12 border-zinc-700 bg-zinc-900 text-zinc-100 hover:bg-zinc-800"
                    >
                      Shorten
                    </Button>
                    <Button
                      variant="outline"
                      className="h-12 border-zinc-700 bg-zinc-900 text-zinc-100 hover:bg-zinc-800"
                    >
                      Soften
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <div className="col-span-12 xl:col-span-3 space-y-6">
                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">Context</CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Lead intelligence</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3 text-sm text-zinc-400">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-emerald-400" />
                      Score {selectedLead.score}
                    </div>
                    <div className="flex items-center gap-2">
                      <Phone className="h-4 w-4 text-emerald-400" />
                      {selectedLead.contact}
                    </div>
                    <div className="flex items-center gap-2">
                      <Bot className="h-4 w-4 text-emerald-400" />
                      AI draft ready
                    </div>
                  </CardContent>
                </Card>
                <Card className="border-zinc-800 bg-zinc-950/90">
                  <CardHeader>
                    <CardDescription className="text-zinc-400">Actions</CardDescription>
                    <CardTitle className="text-xl text-zinc-100">Quick adjustments</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <Button
                      variant="outline"
                      className="w-full justify-start border-zinc-700 bg-black/35 text-zinc-100 hover:bg-zinc-800"
                    >
                      <Sparkles className="mr-2 h-4 w-4 text-emerald-400" />
                      Make shorter
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start border-zinc-700 bg-black/35 text-zinc-100 hover:bg-zinc-800"
                    >
                      <MessageCircle className="mr-2 h-4 w-4 text-emerald-400" />
                      Make softer
                    </Button>
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
