'use client'

import { useCallback, useMemo, useState } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  Edge,
  Node,
  Connection,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Zap, Play } from 'lucide-react'

const CustomNode = ({ data }: { data: any; selected: boolean }) => (
  <div className="rounded-lg border-2 border-emerald-500 bg-black px-4 py-3 text-center text-sm font-semibold text-zinc-100 shadow-[0_0_15px_rgba(16,185,129,0.2)] min-w-[180px]">
    {data.label}
  </div>
)

const initialNodes: Node[] = [
  { id: '1', type: 'custom', position: { x: 250, y: 100 }, data: { label: 'Lead Score > 80' } },
  { id: '2', type: 'custom', position: { x: 100, y: 250 }, data: { label: 'Generate Pitch Deck' } },
  { id: '3', type: 'custom', position: { x: 400, y: 250 }, data: { label: 'Send WhatsApp Alert' } },
]

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#10b981', strokeWidth: 2 } },
  { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: '#10b981', strokeWidth: 2 } },
]

export default function WorkflowBuilderPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)
  const [isDeploying, setIsDeploying] = useState(false)
  const nodeTypes = useMemo(() => ({ custom: CustomNode }), [])
  const onConnect = useCallback(
    (params: Edge | Connection) =>
      setEdges(eds => addEdge({ ...params, animated: true, style: { stroke: '#10b981', strokeWidth: 2 } }, eds)),
    [setEdges]
  )

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
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardDescription className="text-zinc-400">Automation</CardDescription>
                  <CardTitle className="text-2xl text-zinc-100">AI workflow orchestrator</CardTitle>
                </div>
                <Button className="bg-emerald-500 text-black hover:bg-emerald-400">
                  <Play className="mr-2 h-4 w-4" />
                  Deploy workflow
                </Button>
              </CardHeader>
            </Card>

            <div className="h-[72vh] overflow-hidden rounded-xl border border-zinc-800 bg-zinc-950/90">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                nodeTypes={nodeTypes}
                fitView
                style={{ background: '#000' }}
              >
                <Background color="#27272a" gap={16} />
                <Controls />
              </ReactFlow>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              {[
                ['Active Triggers', 'Lead Score > 80'],
                ['Actions', 'Generate Pitch Deck'],
                ['Connections', 'Animated data flow enabled'],
              ].map(([title, desc]) => (
                <Card key={title} className="border-zinc-800 bg-black/35">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg text-zinc-100">
                      <Zap className="h-4 w-4 text-emerald-400" />
                      {title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm text-zinc-400">{desc}</CardContent>
                </Card>
              ))}
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
