'use client'

import { useState } from 'react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Users, Plus, Calculator, Crown, Award, Medal } from 'lucide-react'

export default function PartnerPage() {
  const [dealValue, setDealValue] = useState('')
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8">
            <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardDescription className="text-zinc-400">Network</CardDescription>
                    <CardTitle className="text-2xl text-zinc-100">Partner & broker directory</CardTitle>
                  </div>
                  <Button className="bg-emerald-500 text-black hover:bg-emerald-400" aria-label="Invite new partner">
                    <Plus className="mr-2 h-4 w-4" />
                    Invite partner
                  </Button>
                </CardHeader>
                <CardContent className="space-y-3">
                  {[
                    ['PT. Property Pro Indonesia', 'Gold', '47 deals'],
                    ['CV. Serang Property Hub', 'Silver', '23 deals'],
                    ['PT. Banten Real Estate', 'Gold', '62 deals'],
                  ].map(([name, tier, deals]) => (
                    <div
                      key={name as string}
                      className="rounded-xl border border-zinc-800 bg-black/35 p-4 flex items-center justify-between"
                    >
                      <div>
                        <div className="text-sm font-medium text-zinc-100">{name}</div>
                        <div className="text-xs text-zinc-500">{deals}</div>
                      </div>
                      <Badge className="bg-emerald-500/15 text-emerald-300">{tier}</Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="text-zinc-400">Calculator</CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">Commission calculator</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Input
                    value={dealValue}
                    onChange={e => setDealValue(e.target.value)}
                    placeholder="Deal value (Rp)"
                    className="border-zinc-700 bg-zinc-900 text-zinc-100"
                  />
                  <div className="grid grid-cols-3 gap-2">
                    <Button variant="outline" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                      <Crown className="mr-2 h-4 w-4 text-yellow-400" />
                      Gold
                    </Button>
                    <Button variant="outline" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                      <Medal className="mr-2 h-4 w-4 text-zinc-300" />
                      Silver
                    </Button>
                    <Button variant="outline" className="border-zinc-700 bg-zinc-900 text-zinc-100">
                      <Award className="mr-2 h-4 w-4 text-orange-400" />
                      Bronze
                    </Button>
                  </div>
                  <Button className="w-full bg-emerald-500 text-black hover:bg-emerald-400" aria-label="Calculate commission based on deal value">
                    <Calculator className="mr-2 h-4 w-4" />
                    Calculate commission
                  </Button>
                </CardContent>
              </Card>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
