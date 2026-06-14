'use client'

import Link from 'next/link'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Upload, Box, FileText, Image, Video } from 'lucide-react'

const assetCards = [
  {
    href: '/dashboard/assets/siteplan-dropzone',
    title: 'Siteplan Dropzone',
    desc: 'Import completed siteplans',
    icon: Upload,
    active: true,
  },
  { href: '#', title: 'Document Library', desc: 'Coming soon', icon: FileText, active: false },
  { href: '#', title: 'Media Gallery', desc: 'Coming soon', icon: Image, active: false },
  { href: '#', title: 'Video Library', desc: 'Coming soon', icon: Video, active: false },
]

export default function AssetsPage() {
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
                  <Upload className="h-4 w-4 text-emerald-400" />
                  Asset workspace
                </CardDescription>
                <CardTitle className="text-2xl text-zinc-100">Asset management</CardTitle>
              </CardHeader>
            </Card>

            <div className="grid gap-4 md:grid-cols-2">
              {assetCards.map(item => {
                const Icon = item.icon
                const body = (
                  <Card
                    className={`border-zinc-800 bg-zinc-950/90 ${item.active ? 'hover:border-emerald-500/30' : 'opacity-60'}`}
                  >
                    <CardHeader>
                      <CardTitle className="flex items-center gap-3 text-lg text-zinc-100">
                        <div className="rounded-lg border border-zinc-800 bg-black/35 p-2">
                          <Icon className="h-5 w-5 text-emerald-400" />
                        </div>
                        {item.title}
                      </CardTitle>
                      <CardDescription className="text-zinc-500">{item.desc}</CardDescription>
                    </CardHeader>
                    <CardContent className="text-sm text-zinc-400">
                      Visual and operational asset handling for project pipelines.
                    </CardContent>
                  </Card>
                )
                return item.active ? (
                  <Link key={item.title} href={item.href}>
                    {body}
                  </Link>
                ) : (
                  <div key={item.title}>{body}</div>
                )
              })}
            </div>

            <Card className="border-zinc-800 bg-zinc-950/90">
              <CardHeader>
                <CardTitle className="text-xl text-zinc-100">About asset management</CardTitle>
                <CardDescription className="text-zinc-500">
                  Pipeline gateway between external systems and visual processing modules.
                </CardDescription>
              </CardHeader>
              <CardContent className="grid gap-6 md:grid-cols-2 text-sm text-zinc-400">
                <div>
                  <div className="mb-2 text-zinc-100">Supported file types</div>
                  <div>Images, 3D models, documents, and videos.</div>
                </div>
                <div>
                  <div className="mb-2 text-zinc-100">Processing pipeline</div>
                  <div>Validation, VFX enhancement, compositing, and optimization.</div>
                </div>
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </div>
  )
}
