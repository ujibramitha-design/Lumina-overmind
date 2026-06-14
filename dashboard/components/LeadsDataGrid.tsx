'use client'

import React, { useState, useMemo, useEffect, useCallback, useRef } from 'react'
import { useRouter } from 'next/navigation'
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  flexRender,
  ColumnDef,
  SortingState,
  ColumnFiltersState,
} from '@tanstack/react-table'
import { useVirtualizer } from '@tanstack/react-virtual'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Search,
  Filter,
  Download,
  Eye,
  ExternalLink,
  Phone,
  Mail,
  MapPin,
  TrendingUp,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  RefreshCw,
} from 'lucide-react'
import { useProjects } from '@/lib/store/projectStore'

interface Lead {
  id: number
  business_name: string
  contact: string
  url: string
  keywords: string[]
  source: string
  score: number
  location: string
  status: 'new' | 'contacted' | 'qualified' | 'closed'
  date_found: string
}

export function LeadsDataGrid() {
  const router = useRouter()
  const [leads, setLeads] = useState<Lead[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])

  // Ref for virtualization container
  const tableContainerRef = useRef<HTMLDivElement>(null)

  // Project isolation
  const { activeProjectId, activeProject } = useProjects()

  // Fetch data from API with project isolation
  useEffect(() => {
    const fetchLeads = async () => {
      try {
        setIsLoading(true)
        setError('')

        // Build URL with project_id parameter for data isolation
        let apiUrl = '/api/leads'
        if (activeProjectId) {
          apiUrl += `?project_id=${activeProjectId}`
        }

        const response = await fetch(apiUrl)

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to fetch leads')
        }

        const result = await response.json()

        if (result.success && result.data) {
          setLeads(result.data)
        } else {
          throw new Error(result.error || 'Invalid response format')
        }
      } catch (err) {
        console.error('Error fetching leads:', err)
        setError(err instanceof Error ? err.message : 'Unknown error occurred')
        // Set empty array on error to prevent crashes
        setLeads([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchLeads()
  }, [activeProjectId]) // Re-fetch when project changes

  // Define columns for TanStack Table
  const columns: ColumnDef<Lead>[] = [
    {
      accessorKey: 'id',
      header: 'ID',
      cell: ({ row }) => <div className="text-zinc-100 font-medium">{row.getValue('id')}</div>,
    },
    {
      accessorKey: 'business_name',
      header: ({ column }) => (
        <div
          className="flex items-center space-x-2 cursor-pointer hover:text-emerald-500 transition-colors"
          onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
        >
          <span>Business Name</span>
          <ArrowUpDown className="h-4 w-4" />
          {column.getIsSorted() === 'asc' && <ArrowUp className="h-3 w-3" />}
          {column.getIsSorted() === 'desc' && <ArrowDown className="h-3 w-3" />}
        </div>
      ),
      cell: ({ row }) => <div className="text-zinc-100 font-medium">{row.getValue('business_name')}</div>,
    },
    {
      accessorKey: 'contact',
      header: 'Contact/URL',
      cell: ({ row }) => {
        const lead = row.original
        return (
          <div className="space-y-1">
            <div className="text-zinc-300 text-sm">{lead.contact}</div>
            <div className="text-zinc-500 text-xs">{lead.url}</div>
          </div>
        )
      },
    },
    {
      accessorKey: 'keywords',
      header: 'Keywords',
      cell: ({ row }) => {
        const keywords = row.getValue('keywords') as string[]
        return (
          <div className="flex flex-wrap gap-1">
            {keywords.map((keyword, index) => (
              <Badge key={index} className="text-xs bg-zinc-800 text-zinc-300 border-zinc-700">
                {keyword}
              </Badge>
            ))}
          </div>
        )
      },
    },
    {
      accessorKey: 'source',
      header: ({ column }) => (
        <div
          className="flex items-center space-x-2 cursor-pointer hover:text-emerald-500 transition-colors"
          onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
        >
          <span>Source</span>
          <ArrowUpDown className="h-4 w-4" />
          {column.getIsSorted() === 'asc' && <ArrowUp className="h-3 w-3" />}
          {column.getIsSorted() === 'desc' && <ArrowDown className="h-3 w-3" />}
        </div>
      ),
      cell: ({ row }) => <div className="text-zinc-300">{row.getValue('source')}</div>,
    },
    {
      accessorKey: 'score',
      header: ({ column }) => (
        <div
          className="flex items-center space-x-2 cursor-pointer hover:text-emerald-500 transition-colors"
          onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
        >
          <span>Score</span>
          <ArrowUpDown className="h-4 w-4" />
          {column.getIsSorted() === 'asc' && <ArrowUp className="h-3 w-3" />}
          {column.getIsSorted() === 'desc' && <ArrowDown className="h-3 w-3" />}
        </div>
      ),
      cell: ({ row }) => {
        const score = row.getValue('score') as number
        let badgeClass = ''
        let badgeText = ''

        if (score >= 80) {
          badgeClass = 'bg-emerald-500/20 text-emerald-500 border-emerald-500/30'
          badgeText = 'HOT'
        } else if (score >= 60) {
          badgeClass = 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
          badgeText = 'WARM'
        } else {
          badgeClass = 'bg-red-500/20 text-red-400 border-red-500/30'
          badgeText = 'COLD'
        }

        return (
          <div className="flex items-center space-x-2">
            <span className="text-zinc-100 font-semibold">{score}</span>
            <Badge className={badgeClass}>{badgeText}</Badge>
          </div>
        )
      },
    },
    {
      id: 'actions',
      header: 'Action',
      cell: ({ row }) => (
        <Button
          variant="outline"
          size="sm"
          onClick={() => router.push(`/leads/${row.original.id}`)}
          className="border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/10 hover:border-emerald-500 hover:text-emerald-300 transition-all duration-200"
        >
          <ExternalLink className="w-3 h-3 mr-1" />
          View 360°
        </Button>
      ),
    },
  ]

  // Memoized filtered data
  const filteredData = useMemo(() => {
    if (!searchTerm) return leads

    const lowercasedSearch = searchTerm.toLowerCase()
    return leads.filter(
      lead =>
        lead.business_name.toLowerCase().includes(lowercasedSearch) ||
        lead.contact.toLowerCase().includes(lowercasedSearch) ||
        lead.url.toLowerCase().includes(lowercasedSearch) ||
        lead.keywords.some((keyword: string) => keyword.toLowerCase().includes(lowercasedSearch)) ||
        lead.source.toLowerCase().includes(lowercasedSearch) ||
        lead.location.toLowerCase().includes(lowercasedSearch)
    )
  }, [leads, searchTerm])

  // Memoized stats calculations
  const stats = useMemo(
    () => ({
      total: leads.length,
      filtered: filteredData.length,
      hot: leads.filter((l: Lead) => l.score >= 80).length,
      warm: leads.filter((l: Lead) => l.score >= 60 && l.score < 80).length,
      cold: leads.filter((l: Lead) => l.score < 60).length,
    }),
    [leads, filteredData.length]
  )

  // Create table instance
  const table = useReactTable({
    data: filteredData,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    state: {
      sorting,
      columnFilters,
    },
  })

  // Callback functions with memoization
  const handleRefresh = useCallback(() => {
    const fetchLeads = async () => {
      try {
        setIsLoading(true)
        setError('')

        const response = await fetch('/api/leads')

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to fetch leads')
        }

        const result = await response.json()

        if (result.success && result.data) {
          setLeads(result.data)
        } else {
          throw new Error(result.error || 'Invalid response format')
        }
      } catch (err) {
        console.error('Error refreshing leads:', err)
        setError(err instanceof Error ? err.message : 'Unknown error occurred')
        setLeads([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchLeads()
  }, [])

  const handleExport = useCallback(() => {
    const csv = [
      ['ID', 'Business Name', 'Contact', 'URL', 'Keywords', 'Source', 'Score', 'Location', 'Status', 'Date'],
      ...filteredData.map(lead => [
        lead.id,
        lead.business_name,
        lead.contact,
        lead.url,
        lead.keywords.join(';'),
        lead.source,
        lead.score,
        lead.location,
        lead.status,
        lead.date_found,
      ]),
    ]
      .map(row => row.join(','))
      .join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'leads_export.csv'
    a.click()
    window.URL.revokeObjectURL(url)
  }, [filteredData])

  const handleRowClick = useCallback(
    (leadId: number) => {
      router.push(`/leads/${leadId}`)
    },
    [router]
  )

  // Virtualization setup
  const rowVirtualizer = useVirtualizer({
    count: table.getRowModel().rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => 60, // Estimated row height
    overscan: 10, // Render 10 extra rows above and below
  })

  return (
    <Card className="bg-zinc-950 border-zinc-800">
      <CardHeader className="border-b border-zinc-800">
        <div className="flex items-center justify-between">
          <CardTitle className="text-zinc-100 flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-emerald-500" />
            Leads Intelligence Grid
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              disabled={isLoading}
              className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-emerald-500"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleExport}
              className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-emerald-500"
            >
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-flex items-center gap-2 text-emerald-500 font-mono text-sm animate-pulse">
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                Establishing Secure Connection to Intelligence Database...
                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
              </div>
              <div className="mt-2 text-zinc-500 text-xs">Decrypting lead data streams...</div>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && !isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="text-red-500 font-mono text-sm mb-2">⚠ DATABASE CONNECTION ERROR</div>
              <div className="text-zinc-400 text-xs max-w-md">{error}</div>
              <Button
                onClick={handleRefresh}
                className="mt-4 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-emerald-500"
                size="sm"
              >
                Retry Connection
              </Button>
            </div>
          </div>
        )}

        {/* Data Grid */}
        {!isLoading && !error && (
          <>
            {/* Global Filter */}
            <div className="flex items-center gap-4 mb-6">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-zinc-500" />
                <Input
                  placeholder="Search leads..."
                  value={searchTerm}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchTerm(e.target.value)}
                  className="pl-10 bg-zinc-900 border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:border-emerald-500 focus:ring-emerald-500"
                />
              </div>
            </div>

            {/* Virtualized TanStack Table */}
            <div
              ref={tableContainerRef}
              className="rounded-md border border-zinc-800 overflow-hidden"
              style={{ height: '600px', overflow: 'auto' }}
            >
              <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, width: '100%', position: 'relative' }}>
                <table className="w-full">
                  <thead className="bg-zinc-900/50 sticky top-0 z-10">
                    <tr className="border-b border-zinc-800">
                      {table.getHeaderGroups().map(headerGroup => (
                        <tr key={headerGroup.id}>
                          {headerGroup.headers.map(header => (
                            <th
                              key={header.id}
                              className="px-4 py-3 text-left text-zinc-400 font-medium border-r border-zinc-800 last:border-r-0"
                            >
                              {header.isPlaceholder
                                ? null
                                : flexRender(header.column.columnDef.header, header.getContext())}
                            </th>
                          ))}
                        </tr>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {rowVirtualizer.getVirtualItems().map((virtualRow: any) => {
                      const row = table.getRowModel().rows[virtualRow.index]
                      return (
                        <tr
                          key={row.id}
                          className="border-b border-zinc-800 hover:bg-zinc-900/50 hover:border-emerald-500/20 transition-all duration-200 cursor-pointer group"
                          onClick={() => handleRowClick(row.original.id)}
                          style={{
                            height: `${virtualRow.size}px`,
                            transform: `translateY(${virtualRow.start}px)`,
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            width: '100%',
                          }}
                        >
                          {row.getVisibleCells().map(cell => (
                            <td
                              key={cell.id}
                              className="px-4 py-3 text-zinc-300 border-r border-zinc-800 last:border-r-0 group-hover:text-zinc-100 transition-colors"
                            >
                              {flexRender(cell.column.columnDef.cell, cell.getContext())}
                            </td>
                          ))}
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Project Context Header */}
            {activeProject && (
              <div className="mb-4 p-3 bg-zinc-900/50 border border-zinc-800 rounded-lg">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-3 h-3 rounded-full ${
                        activeProject.tipe_proyek === 'KOMERSIL' ? 'bg-yellow-500' : 'bg-blue-500'
                      }`}
                    />
                    <div>
                      <div className="text-sm font-medium text-zinc-100">{activeProject.nama_proyek}</div>
                      <div className="text-xs text-zinc-400">
                        {activeProject.lokasi} • {activeProject.tipe_proyek}
                      </div>
                    </div>
                  </div>
                  <div
                    className={`px-2 py-1 text-xs rounded-full border ${
                      activeProject.tipe_proyek === 'KOMERSIL'
                        ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                        : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                    }`}
                  >
                    {activeProject.tipe_proyek}
                  </div>
                </div>
              </div>
            )}

            {/* Stats Footer */}
            <div className="mt-4 pt-4 border-t border-zinc-800">
              <div className="flex items-center justify-between text-sm text-zinc-400">
                <span>
                  {activeProject
                    ? `Showing ${stats.filtered} of ${stats.total} leads for ${activeProject.nama_proyek}`
                    : `Showing ${stats.filtered} of ${stats.total} leads`}
                </span>
                <div className="flex items-center gap-4">
                  <span>Hot: {stats.hot}</span>
                  <span>Warm: {stats.warm}</span>
                  <span>Cold: {stats.cold}</span>
                </div>
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}

export default LeadsDataGrid
