'use client'

import { useState, useEffect } from 'react'
import { Sidebar } from '@/components/Sidebar'
import TopHeader from '@/components/TopHeader'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ShieldAlert, AlertTriangle, CheckCircle, XCircle, TrendingUp } from 'lucide-react'
import { TerminalLogs } from '@/components/TerminalLogs'

interface Policy {
  id: string
  name: string
  description: string
  category: string
  severity: string
  enabled: boolean
}

interface ComplianceReport {
  period: { start_date: string; end_date: string }
  total_policies: number
  passed_policies: number
  failed_policies: number
  warning_policies: number
  compliance_score: number
  violations: any[]
  recommendations: string[]
}

export default function GovernancePage() {
  const [policies, setPolicies] = useState<Policy[]>([])
  const [complianceReport, setComplianceReport] = useState<ComplianceReport | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPolicies()
    fetchComplianceReport()
  }, [])

  const fetchPolicies = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/policy/policies')
      const data = await response.json()
      setPolicies(data.policies || [])
    } catch (error) {
      console.error('Failed to fetch policies:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchComplianceReport = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/policy/compliance-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
      const data = await response.json()
      setComplianceReport(data)
    } catch (error) {
      console.error('Failed to fetch compliance report:', error)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-500'
      case 'high': return 'text-orange-500'
      case 'medium': return 'text-yellow-500'
      case 'low': return 'text-green-500'
      default: return 'text-gray-500'
    }
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'security': return 'bg-red-500/20 text-red-400'
      case 'privacy': return 'bg-purple-500/20 text-purple-400'
      case 'access': return 'bg-blue-500/20 text-blue-400'
      case 'data': return 'bg-green-500/20 text-green-400'
      case 'compliance': return 'bg-yellow-500/20 text-yellow-400'
      default: return 'bg-gray-500/20 text-gray-400'
    }
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(16,185,129,0.12),transparent_35%),linear-gradient(180deg,#020617_0%,#000_100%)] text-zinc-100">
      <div className="flex min-h-screen">
        <aside className="hidden xl:block">
          <Sidebar />
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <TopHeader />
          <main className="mx-auto w-full max-w-[1600px] flex-1 px-4 py-4 sm:px-6 lg:px-8 space-y-6">
            {/* Compliance Score Card */}
            {complianceReport && (
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardDescription className="flex items-center gap-2 text-zinc-400">
                    <TrendingUp className="h-4 w-4 text-emerald-400" />
                    Overall compliance status
                  </CardDescription>
                  <CardTitle className="text-3xl text-zinc-100">
                    {complianceReport.compliance_score.toFixed(1)}%
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-3">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="h-5 w-5 text-green-500" />
                      <div>
                        <p className="text-sm text-zinc-400">Passed</p>
                        <p className="text-xl font-semibold">{complianceReport.passed_policies}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <XCircle className="h-5 w-5 text-red-500" />
                      <div>
                        <p className="text-sm text-zinc-400">Failed</p>
                        <p className="text-xl font-semibold">{complianceReport.failed_policies}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5 text-yellow-500" />
                      <div>
                        <p className="text-sm text-zinc-400">Warnings</p>
                        <p className="text-xl font-semibold">{complianceReport.warning_policies}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Policies Grid */}
            <Card className="border-zinc-800 bg-zinc-950/90">
              <CardHeader>
                <CardDescription className="flex items-center gap-2 text-zinc-400">
                  <ShieldAlert className="h-4 w-4 text-emerald-400" />
                  Active policies
                </CardDescription>
                <CardTitle className="text-2xl text-zinc-100">Policy Definitions</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p className="text-zinc-400">Loading policies...</p>
                ) : (
                  <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {policies.map((policy) => (
                      <Card key={policy.id} className="border-zinc-800 bg-zinc-900/50">
                        <CardHeader>
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <CardTitle className="text-lg">{policy.name}</CardTitle>
                              <CardDescription className="mt-1">{policy.description}</CardDescription>
                            </div>
                            <span className={`px-2 py-1 rounded text-xs ${getCategoryColor(policy.category)}`}>
                              {policy.category}
                            </span>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="flex items-center justify-between">
                            <span className={`text-sm font-medium ${getSeverityColor(policy.severity)}`}>
                              {policy.severity}
                            </span>
                            <span className={`text-xs ${policy.enabled ? 'text-green-400' : 'text-gray-500'}`}>
                              {policy.enabled ? 'Enabled' : 'Disabled'}
                            </span>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Recommendations */}
            {complianceReport && complianceReport.recommendations.length > 0 && (
              <Card className="border-zinc-800 bg-zinc-950/90">
                <CardHeader>
                  <CardTitle className="text-xl text-zinc-100">Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {complianceReport.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start gap-2 text-zinc-300">
                        <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Terminal Logs */}
            <Card className="border-zinc-800 bg-zinc-950/90">
              <CardHeader>
                <CardDescription className="flex items-center gap-2 text-zinc-400">
                  <ShieldAlert className="h-4 w-4 text-emerald-400" />
                  Security terminal
                </CardDescription>
                <CardTitle className="text-2xl text-zinc-100">Governance & security</CardTitle>
              </CardHeader>
              <CardContent>
                <TerminalLogs />
              </CardContent>
            </Card>
          </main>
        </div>
      </div>
    </div>
  )
}
