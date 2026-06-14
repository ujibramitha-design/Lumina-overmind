'use client'

import React, { useState, useEffect } from 'react'
import { CheckCircle, XCircle, RefreshCw, Eye, Edit3, Rocket, Target, Clock, DollarSign, BarChart } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { Alert, AlertDescription } from '@/components/ui/alert'

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
  project?: {
    id: string
    namaProyek: string
    tipeProyek: 'KOMERSIL' | 'SUBSIDI'
    lokasi: string
    hargaStart: number
  }
}

export default function AdsApprovalPage() {
  const { toast } = useToast()
  const [proposals, setProposals] = useState<AdProposal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [processingId, setProcessingId] = useState<string | null>(null)
  const [selectedProposal, setSelectedProposal] = useState<AdProposal | null>(null)
  const [showDetailsModal, setShowDetailsModal] = useState(false)
  const [showReviseModal, setShowReviseModal] = useState(false)
  const [revisionInstructions, setRevisionInstructions] = useState('')

  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
  })

  useEffect(() => {
    fetchProposals()
  }, [])

  const fetchProposals = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('/api/ads/proposals?status=PENDING')
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
    } finally {
      setIsLoading(false)
    }
  }

  const handleApprove = async (proposalId: string) => {
    setProcessingId(proposalId)
    try {
      const response = await fetch(`/api/ads/proposals/${proposalId}/approve`, {
        method: 'POST',
      })

      if (!response.ok) throw new Error('Failed to approve proposal')

      await response.json()

      toast({
        title: 'Success',
        description: 'Proposal approved and launched successfully',
      })

      // Refresh proposals
      await fetchProposals()
    } catch (error) {
      console.error('Error approving proposal:', error)
      toast({
        title: 'Error',
        description: 'Failed to approve proposal',
        variant: 'destructive',
      })
    } finally {
      setProcessingId(null)
    }
  }

  const handleReject = async (proposalId: string) => {
    setProcessingId(proposalId)
    try {
      const response = await fetch(`/api/ads/proposals/${proposalId}/reject`, {
        method: 'POST',
      })

      if (!response.ok) throw new Error('Failed to reject proposal')

      toast({
        title: 'Success',
        description: 'Proposal rejected successfully',
      })

      // Refresh proposals
      await fetchProposals()
    } catch (error) {
      console.error('Error rejecting proposal:', error)
      toast({
        title: 'Error',
        description: 'Failed to reject proposal',
        variant: 'destructive',
      })
    } finally {
      setProcessingId(null)
    }
  }

  const handleRevise = async (proposalId: string) => {
    if (!revisionInstructions.trim()) {
      toast({
        title: 'Error',
        description: 'Please provide revision instructions',
        variant: 'destructive',
      })
      return
    }

    setProcessingId(proposalId)
    try {
      const response = await fetch(`/api/ads/proposals/${proposalId}/revise`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          revisionInstructions,
        }),
      })

      if (!response.ok) throw new Error('Failed to revise proposal')

      await response.json()

      toast({
        title: 'Success',
        description: 'Proposal revised successfully',
      })

      // Close modal and refresh
      setShowReviseModal(false)
      setRevisionInstructions('')
      await fetchProposals()
    } catch (error) {
      console.error('Error revising proposal:', error)
      toast({
        title: 'Error',
        description: 'Failed to revise proposal',
        variant: 'destructive',
      })
    } finally {
      setProcessingId(null)
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

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'PENDING':
        return <Clock className="h-4 w-4" />
      case 'APPROVED':
        return <CheckCircle className="h-4 w-4" />
      case 'REJECTED':
        return <XCircle className="h-4 w-4" />
      default:
        return <Clock className="h-4 w-4" />
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                <Rocket className="h-8 w-8 text-emerald-400" />
                Command Center - Pusat Persetujuan Jenderal
              </h1>
              <p className="text-gray-300">Review and approve AI-generated advertising proposals</p>
            </div>

            <Button
              onClick={fetchProposals}
              disabled={isLoading}
              variant="outline"
              className="border-slate-600 text-slate-300 hover:bg-slate-800"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Total Proposals</p>
                  <p className="text-2xl font-bold text-white">{stats.total}</p>
                </div>
                <BarChart className="h-8 w-8 text-blue-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Pending Review</p>
                  <p className="text-2xl font-bold text-yellow-400">{stats.pending}</p>
                </div>
                <Clock className="h-8 w-8 text-yellow-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Approved</p>
                  <p className="text-2xl font-bold text-green-400">{stats.approved}</p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 backdrop-blur-sm border-slate-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Rejected</p>
                  <p className="text-2xl font-bold text-red-400">{stats.rejected}</p>
                </div>
                <XCircle className="h-8 w-8 text-red-400" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Alert */}
        {stats.pending === 0 && !isLoading && (
          <Alert className="mb-6 bg-blue-500/20 border-blue-500/30">
            <AlertDescription className="text-blue-300">
              All proposals have been reviewed. No pending proposals require approval.
            </AlertDescription>
          </Alert>
        )}

        {/* Proposals Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {proposals.map(proposal => (
            <Card
              key={proposal.id}
              className="bg-slate-800/50 backdrop-blur-sm border-slate-700 hover:border-emerald-500/50 transition-all duration-300"
            >
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(proposal.status)}
                    <Badge className={getStatusColor(proposal.status)}>{proposal.status}</Badge>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => {
                        setSelectedProposal(proposal)
                        setShowDetailsModal(true)
                      }}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">{proposal.opsiStrategi}</h3>
                  <p className="text-sm text-gray-400">{proposal.project?.namaProyek || 'Unknown Project'}</p>
                  <div className="flex items-center gap-2 mt-2">
                    <Badge
                      className={
                        proposal.project?.tipeProyek === 'KOMERSIL'
                          ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                          : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                      }
                    >
                      {proposal.project?.tipeProyek || 'UNKNOWN'}
                    </Badge>
                    <span className="text-xs text-gray-500">{proposal.project?.lokasi || 'Unknown Location'}</span>
                  </div>
                </div>

                <div>
                  <p className="text-sm text-gray-300 mb-2">
                    <span className="font-medium">Target:</span> {proposal.targetAudience}
                  </p>
                  <p className="text-sm text-gray-300 mb-2">
                    <span className="font-medium">Copy:</span>{' '}
                    {proposal.copywriting.length > 100
                      ? proposal.copywriting.substring(0, 100) + '...'
                      : proposal.copywriting}
                  </p>
                  <div className="flex items-center gap-2 text-sm">
                    <DollarSign className="h-4 w-4 text-emerald-400" />
                    <span className="text-emerald-400 font-medium">{formatCurrency(proposal.estimasiBudget)}</span>
                  </div>
                </div>

                <div className="flex gap-2 pt-4 border-t border-slate-700">
                  <Button
                    size="sm"
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white"
                    onClick={() => handleApprove(proposal.id)}
                    disabled={processingId === proposal.id}
                  >
                    {processingId === proposal.id ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Approve & Launch
                      </>
                    )}
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    className="flex-1 border-red-500/50 text-red-400 hover:bg-red-500/20"
                    onClick={() => handleReject(proposal.id)}
                    disabled={processingId === proposal.id}
                  >
                    {processingId === proposal.id ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <XCircle className="h-4 w-4 mr-2" />
                        Reject
                      </>
                    )}
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    className="flex-1 border-blue-500/50 text-blue-400 hover:bg-blue-500/20"
                    onClick={() => {
                      setSelectedProposal(proposal)
                      setShowReviseModal(true)
                    }}
                    disabled={processingId === proposal.id}
                  >
                    {processingId === proposal.id ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Edit3 className="h-4 w-4 mr-2" />
                        Revise
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-20">
            <RefreshCw className="h-8 w-8 text-emerald-400 animate-spin" />
            <span className="ml-3 text-emerald-400">Loading proposals...</span>
          </div>
        )}

        {/* Empty State */}
        {!isLoading && proposals.length === 0 && (
          <div className="text-center py-20">
            <Target className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-300 mb-2">No Pending Proposals</h3>
            <p className="text-gray-400">All proposals have been reviewed. Check back later for new proposals.</p>
          </div>
        )}
      </div>

      {/* Details Modal */}
      {showDetailsModal && selectedProposal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <Card className="bg-slate-900 border-slate-700 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <CardHeader className="flex items-center justify-between border-b border-slate-700">
              <CardTitle className="text-white">Proposal Details</CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowDetailsModal(false)}
                className="text-gray-400 hover:text-white"
              >
                ×
              </Button>
            </CardHeader>

            <CardContent className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-white mb-2">{selectedProposal.opsiStrategi}</h3>
                <Badge className={getStatusColor(selectedProposal.status)}>{selectedProposal.status}</Badge>
              </div>

              <div>
                <h4 className="text-white font-medium mb-2">Target Audience</h4>
                <p className="text-gray-300">{selectedProposal.targetAudience}</p>
              </div>

              <div>
                <h4 className="text-white font-medium mb-2">Copywriting</h4>
                <p className="text-gray-300 whitespace-pre-wrap">{selectedProposal.copywriting}</p>
              </div>

              <div>
                <h4 className="text-white font-medium mb-2">Budget Estimation</h4>
                <p className="text-emerald-400 text-lg font-semibold">
                  {formatCurrency(selectedProposal.estimasiBudget)}
                </p>
              </div>

              <div>
                <h4 className="text-white font-medium mb-2">Project Details</h4>
                <div className="space-y-1 text-sm">
                  <p className="text-gray-300">
                    <span className="font-medium">Project:</span> {selectedProposal.project?.namaProyek || 'Unknown'}
                  </p>
                  <p className="text-gray-300">
                    <span className="font-medium">Type:</span> {selectedProposal.project?.tipeProyek || 'Unknown'}
                  </p>
                  <p className="text-gray-300">
                    <span className="font-medium">Location:</span> {selectedProposal.project?.lokasi || 'Unknown'}
                  </p>
                  <p className="text-gray-300">
                    <span className="font-medium">Price:</span>{' '}
                    {formatCurrency(selectedProposal.project?.hargaStart || 0)}
                  </p>
                </div>
              </div>

              <div className="flex gap-2 pt-4 border-t border-slate-700">
                <Button
                  className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white"
                  onClick={() => {
                    setShowDetailsModal(false)
                    handleApprove(selectedProposal.id)
                  }}
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Approve & Launch
                </Button>

                <Button
                  variant="outline"
                  className="flex-1 border-red-500/50 text-red-400 hover:bg-red-500/20"
                  onClick={() => {
                    setShowDetailsModal(false)
                    handleReject(selectedProposal.id)
                  }}
                >
                  <XCircle className="h-4 w-4 mr-2" />
                  Reject
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Revise Modal */}
      {showReviseModal && selectedProposal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <Card className="bg-slate-900 border-slate-700 max-w-lg w-full">
            <CardHeader className="flex items-center justify-between border-b border-slate-700">
              <CardTitle className="text-white">Revise Proposal</CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowReviseModal(false)}
                className="text-gray-400 hover:text-white"
              >
                ×
              </Button>
            </CardHeader>

            <CardContent className="space-y-4">
              <div>
                <h3 className="text-white font-medium mb-2">Revise: {selectedProposal.opsiStrategi}</h3>
                <p className="text-gray-300 text-sm">
                  {selectedProposal.project?.namaProyek} - {selectedProposal.project?.tipeProyek}
                </p>
              </div>

              <div>
                <label htmlFor="revision" className="block text-sm font-medium text-gray-300 mb-2">
                  Revision Instructions
                </label>
                <textarea
                  id="revision"
                  value={revisionInstructions}
                  onChange={e => setRevisionInstructions(e.target.value)}
                  placeholder="Provide specific instructions for revising this proposal..."
                  className="w-full bg-slate-800 border-slate-600 text-white placeholder:text-gray-400 rounded-lg px-4 py-3 focus:border-emerald-500 focus:ring-emerald-500/20 focus:border-emerald-500 h-32"
                  rows={4}
                />
              </div>

              <div className="flex gap-2 pt-4 border-t border-slate-700">
                <Button
                  variant="outline"
                  onClick={() => setShowReviseModal(false)}
                  className="flex-1 border-slate-600 text-slate-300 hover:bg-slate-800"
                >
                  Cancel
                </Button>

                <Button
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                  onClick={() => handleRevise(selectedProposal.id)}
                  disabled={processingId === selectedProposal.id}
                >
                  {processingId === selectedProposal.id ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Edit3 className="h-4 w-4 mr-2" />
                      Submit Revision
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
