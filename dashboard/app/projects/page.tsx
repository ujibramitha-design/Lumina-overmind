'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Plus, Building2, Crown, Shield, Search, Filter } from 'lucide-react'

const projects = [
  {
    id: '1',
    name: 'Grand Serang Residence',
    type: 'KOMERSIL',
    location: 'Serang',
    price: 'Rp 500.000.000',
    leads: 82,
    hot: 14,
    active: true,
  },
  {
    id: '2',
    name: 'Banten Hills',
    type: 'SUBSIDI',
    location: 'Tangerang',
    price: 'Rp 180.000.000',
    leads: 64,
    hot: 11,
    active: true,
  },
  {
    id: '3',
    name: 'Citra Indah',
    type: 'KOMERSIL',
    location: 'Bandung',
    price: 'Rp 620.000.000',
    leads: 41,
    hot: 7,
    active: false,
  },
]

export default function ProjectsPage() {
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
                  <CardDescription className="text-zinc-400">Portfolio</CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">Project management</CardTitle>
                </div>
                <Button className="bg-emerald-500 text-black hover:bg-emerald-400">
                  <Plus className="mr-2 h-4 w-4" />
                  New project
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
                      placeholder="Search projects..."
                    />
                  </div>
                  <Button variant="outline" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                    <Filter className="mr-2 h-4 w-4" />
                    Filter
                  </Button>
                </div>

                <div className="grid gap-4 xl:grid-cols-3">
                  {projects
                    .filter(
                      p =>
                        p.name.toLowerCase().includes(query.toLowerCase()) ||
                        p.location.toLowerCase().includes(query.toLowerCase())
                    )
                    .map(project => (
                      <Card key={project.id} className="border-zinc-800 bg-black/35">
                        <CardHeader>
                          <div className="flex items-start justify-between gap-3">
                            <div className="flex items-center gap-2">
                              {project.type === 'KOMERSIL' ? (
                                <Crown className="h-4 w-4 text-yellow-400" />
                              ) : (
                                <Shield className="h-4 w-4 text-sky-400" />
                              )}
                              <CardTitle className="text-lg text-zinc-100">{project.name}</CardTitle>
                            </div>
                            <Badge className="bg-emerald-500/15 text-emerald-300">
                              {project.active ? 'Active' : 'Paused'}
                            </Badge>
                          </div>
                          <CardDescription className="text-zinc-500">
                            {project.location} • {project.type}
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div className="text-sm text-zinc-400">Starting price</div>
                          <div className="text-zinc-100">{project.price}</div>
                          <div className="flex items-center justify-between border-t border-zinc-800 pt-3 text-sm text-zinc-400">
                            <span>
                              <span className="text-emerald-400">{project.leads}</span> leads
                            </span>
                            <span>
                              <span className="text-amber-400">{project.hot}</span> hot
                            </span>
                          </div>
                          <Button variant="outline" className="w-full border-zinc-700 bg-zinc-900 text-zinc-100">
                            <Building2 className="mr-2 h-4 w-4" />
                            View details
                          </Button>
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
