'use client'

import React, { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Brain, Rocket, Target, TrendingUp, Clock, Users, BarChart, Zap, Play } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

interface Project {
  id: string
  namaProyek: string
  tipeProyek: 'KOMERSIL' | 'SUBSIDI'
  lokasi: string
  hargaStart: number
  targetMarket: string
  isActive: boolean
  leadsCount: number
  hotLeadsCount: number
  conversionRate: number
  createdAt: string
  updatedAt: string
}

interface AdProposal {
  id: string
  projectId: string
  opsiStrategi: string
  targetAudience: string
  copywriting: string
  estimasiBudget: number
  status: 'PENDING' | 'APPROVED' | 'REJECTED'
  createdAt: string
  updatedAt: string
}

export default function ProjectDetailPage() {
  const params = useParams()
  const router = useRouter()
  const { toast } = useToast()
  const projectId = params.id as string

  const [project, setProject] = useState<Project | null>(null)
  const [proposals, setProposals] = useState<AdProposal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')

  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
  })

  useEffect(() => {
    if (projectId) {
      fetchProject()
      fetchProposals()
    }
  }, [projectId])

  const fetchProject = async () => {
    try {
      const response = await fetch(`/api/projects/${projectId}`)
      if (!response.ok) throw new Error('Failed to fetch project')

      const data = await response.json()
      setProject(data.data)
    } catch (error) {
      console.error('Error fetching project:', error)
      toast({
        title: 'Error',
        description: 'Failed to fetch project details',
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fetchProposals = async () => {
    try {
      const response = await fetch(`/api/ads/proposals?project_id=${projectId}`)
      if (!response.ok) throw new Error('Failed to fetch proposals')

      const data = await response.json()
      setProposals(data.data || [])

      // Update stats
      setStats({
        total: data.total || 0,
        pending: data.pending || 0,
        approved: data.approved || 0,
        rejected: data.rejected || 0,
      })
    } catch (error) {
      console.error('Error fetching proposals:', error)
      toast({
        title: 'Error',
        description: 'Failed to fetch ad proposals',
        variant: 'destructive',
      })
    }
  }

  const handleGenerateAds = async () => {
    if (!project) return

    setIsGenerating(true)
    try {
      const response = await fetch(`/api/ads/generate/${projectId}`, {
        method: 'POST',
      })

      if (!response.ok) throw new Error('Failed to generate ads')

      const result = await response.json()

      toast({
        title: 'Success!',
        description: result.message || 'AI CMO generated ad proposals successfully',
      })

      // Refresh proposals
      await fetchProposals()
    } catch (error) {
      console.error('Error generating ads:', error)
      toast({
        title: 'Error',
        description: error.message || 'Failed to generate ad proposals',
        variant: 'destructive',
      })
    } finally {
      setIsGenerating(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
      case 'APPROVED':
        return 'bg-green-500/20 text-green-400 border-green-500/30'
      case 'REJECTED':
        return 'bg-red-500/20 text-red-400 border-red-500/30'
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500/30'
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 border-t-transparent"></div>
          <p className="mt-4 text-emerald-400">Loading project details...</p>
        </div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Project Not Found</h1>
          <p className="text-gray-400">The project you're looking for doesn't exist.</p>
          <Button onClick={() => router.push('/projects')} className="mt-4">
            Back to Projects
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-6">
            <Button variant="ghost" onClick={() => router.push('/projects')} className="text-gray-400 hover:text-white">
              <ArrowLeft className="h-4 w-4" />
            </Button>

            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white">{project.namaProyek}</h1>
              <p className="text-gray-300">{project.lokasi}</p>
            </div>

            <div className="flex gap-2">
              <Badge
                className={
                  project.tipeProyek === 'KOMERSIL'
                    ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                    : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                }
              >
                {project.tipeProyek}
              </Badge>

              <Badge
                className={
                  project.isActive
                    ? 'bg-green-500/20 text-green-400 border-green-500/30'
                    : 'bg-gray-500/20 text-gray-400 border-gray-500/30'
                }
              >
                {project.isActive ? 'Active' : 'Inactive'}
              </Badge>
            </div>
          </div>
        </div>

        {/* AI CMO Trigger Button */}
        <div className="mb-8">
          <Card className="bg-gradient-to-r from-emerald-600/20 to-blue-600/20 backdrop-blur-sm border-emerald-500/50">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-semibold text-white mb-2 flex items-center gap-2">
                    <Brain className="h-6 w-6 text-emerald-400" />
                    AI Chief Marketing Officer
                  </h3>
                  <p className="text-gray-300">
                    Generate context-aware ad proposals based on project data, existing leads, and market analysis
                  </p>
                </div>

                <Button
                  onClick={handleGenerateAds}
                  disabled={isGenerating}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 disabled:opacity-50"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white border-t-transparent mr-2"></div>
                      <span>AI sedang menganalisis...</span>
                    </>
                  ) : (
                    <>
                      <Rocket className="h-4 w-4 mr-2" />
                      <span>Tugaskan AI CMO (Susun Draf Iklan)</span>
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger
              value="overview"
              className="data-[state=active]:bg-slate-800 data-[state=inactive]:bg-slate-700"
            >
              <Target className="h-4 w-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger
              value="proposals"
              className="data-[state=active]:bg-slate-800 data-[state=inactive]:bg-slate-700"
            >
              <Zap className="h-4 w-4" />
              Proposals ({stats.total})
            </TabsTrigger>
            <TabsTrigger
              value="analytics"
              className="data-[state=active]:bg-slate-800 data-[state=inactive]:bg-slate-700"
            >
              <TrendingUp className="h-4 w-4" />
              Analytics
            </TabsTrigger>
            <TabsTrigger
              value="settings"
              className="data-[state=active]:bg-sale-800 data-[state=inactive]:bg-slate-700"
            >
              <BarChart className="h-4 w-4" />
              Settings
            </TabsTrigger>
          </TabsList>
        </Tabs>

        {/* Tab Content */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Project Performance</p>
                    <p className="text-2xl font-bold text-white">{project.leadsCount}</p>
                  </div>
                  <Users className="h-8 w-8 text-blue-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Hot Leads</p>
                    <p className="text-2xl font-bold text-emerald-400">{project.hotLeadsCount}</p>
                  </div>
                  <Target className="h-8 w-8 text-emerald-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Conversion Rate</p>
                    <p className="text-2xl font-bold text-purple-400">{project.conversionRate.toFixed(1)}%</p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-purple-400" />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Project Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-400 text-sm">Project Type</p>
                  <p className="text-white font-medium">{project.tipeProyek}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Location</p>
                  <p className="text-white font-medium">{project.lokasi}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Starting Price</p>
                  <p className="text-white font-medium">{formatCurrency(project.hargaStart)}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Target Market</p>
                  <p className="text-white font-medium">{project.targetMarket}</p>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-700">
                <p className="text-gray-400 text-sm mb-2">Created</p>
                <p className="text-white">{formatDate(project.createdAt)}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="proposals" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {proposals.map(proposal => (
              <Card
                key={proposal.id}
                className="bg-slate-800/50 backdrop-blur-sm border-slate-700 hover:border-emerald-500/50 transition-all duration-300"
              >
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between">
                    <Badge className={getStatusColor(proposal.status)}>{proposal.status}</Badge>
                    <p className="text-gray-400 text-xs">{formatDate(proposal.createdAt)}</p>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-2">{proposal.opsiStrategi}</h4>
                    <p className="text-sm text-gray-300 mb-3">{proposal.targetAudience}</p>
                    <p className="text-sm text-gray-300">{proposal.copywriting}</p>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-slate-700">
                    <span className="text-emerald-400 font-semibold">{formatCurrency(proposal.estimasiBudget)}</span>
                    <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/30">Budget</Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {proposals.length === 0 && (
            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardContent className="text-center py-12">
                <Zap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No Ad Proposals Yet</h3>
                <p className="text-gray-400 mb-4">Generate AI-powered ad proposals to get started</p>
                <Button onClick={handleGenerateAds} disabled={isGenerating}>
                  <Rocket className="h-4 w-4 mr-2" />
                  Generate Proposals
                </Button>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Ad Performance</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Total Proposals</span>
                  <span className="text-2xl font-bold text-white">{stats.total}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Approved</span>
                  <span className="text-2xl font-bold text-green-400">{stats.approved}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Rejected</span>
                  <span className="text-2xl font-bold text-red-400">{stats.rejected}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Pending</span>
                  <span className="text-2xl font-bold text-yellow-400">{stats.pending}</span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
              <CardHeader>
                <CardTitle className="text-white">Budget Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  {proposals.map((proposal, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">{proposal.opsiStrategi}</span>
                      <span className="text-white font-medium">{formatCurrency(proposal.estimasiBudget)}</span>
                    </div>
                  ))}
                </div>

                {proposals.length > 0 && (
                  <div className="pt-4 border-t border-slate-700">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400">Total Budget</span>
                      <span className="text-xl font-bold text-emerald-400">
                        {formatCurrency(proposals.reduce((sum, p) => sum + p.estimasiBudget, 0))}
                      </span>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardHeader>
              <CardTitle className="text-white">Project Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Alert>
                <AlertDescription>Project settings and configuration options will be available here.</AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </TabsContent>
      </div>
    </div>
  )
}
