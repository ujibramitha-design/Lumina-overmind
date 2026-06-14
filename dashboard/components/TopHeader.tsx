'use client'

import React, { useState, useEffect, useRef, useCallback } from 'react'
import {
  Search,
  Bell,
  User,
  ChevronDown,
  Zap,
  Circle,
  Home,
  Target,
  TrendingUp,
  Tag,
  X,
  Crown,
  Shield,
  Building,
} from 'lucide-react'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'
import { useProjects, getProjectThemeColors } from '@/lib/store/projectStore'

interface Notification {
  id: string
  title: string
  message: string
  time: string
  type: 'lead' | 'system' | 'alert'
}

interface SearchResult {
  id: string
  title: string
  description: string
  type: 'lead' | 'runner' | 'campaign'
  [key: string]: any
}

interface SearchResponse {
  leads: SearchResult[]
  runners: SearchResult[]
  campaigns: SearchResult[]
}

const TopHeader: React.FC = () => {
  const [searchFocused, setSearchFocused] = useState(false)
  const [notificationOpen, setNotificationOpen] = useState(false)
  const [systemOnline, setSystemOnline] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchResponse>({
    leads: [],
    runners: [],
    campaigns: [],
  })
  const [isSearching, setIsSearching] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [projectDropdownOpen, setProjectDropdownOpen] = useState(false)

  const notificationRef = useRef<HTMLDivElement>(null)
  const searchRef = useRef<HTMLDivElement>(null)
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const projectDropdownRef = useRef<HTMLDivElement>(null)

  // Project management
  const {
    projects,
    activeProject,
    activeProjectId,
    setActiveProject,
    fetchProjects,
    isLoading: projectsLoading,
  } = useProjects()

  // Dummy notifications
  const notifications: Notification[] = [
    {
      id: '1',
      title: 'Hot Lead Found',
      message: 'High-intent lead detected in Serpong with score 9/10',
      time: '2 min ago',
      type: 'lead',
    },
    {
      id: '2',
      title: 'AI Model Deployed',
      message: 'New scoring model successfully deployed to production',
      time: '15 min ago',
      type: 'system',
    },
    {
      id: '3',
      title: 'Competitor Alert',
      message: 'Price drop detected at Perumahan Citra Indah',
      time: '1 hour ago',
      type: 'alert',
    },
  ]

  // Fetch projects on component mount
  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target as Node)) {
        setNotificationOpen(false)
      }
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setSearchOpen(false)
      }
      if (projectDropdownRef.current && !projectDropdownRef.current.contains(event.target as Node)) {
        setProjectDropdownOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Simulate system status blinking
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemOnline(prev => !prev)
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  // Debounced search function
  const performSearch = useCallback(async (query: string) => {
    if (query.length < 2) {
      setSearchResults({ leads: [], runners: [], campaigns: [] })
      setSearchOpen(false)
      return
    }

    setIsSearching(true)
    try {
      const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(query)}`)
      const data = await response.json()

      if (data.success) {
        setSearchResults(data.data)
        setSearchOpen(true)
      }
    } catch (error) {
      console.error('Search error:', error)
      setSearchResults({ leads: [], runners: [], campaigns: [] })
    } finally {
      setIsSearching(false)
    }
  }, [])

  // Handle search input with debounce
  const handleSearchChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const query = e.target.value
      setSearchQuery(query)
      setSearchFocused(true)

      // Clear existing timeout
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current)
      }

      // Set new timeout for debounce
      searchTimeoutRef.current = setTimeout(() => {
        performSearch(query)
      }, 300) // 300ms debounce
    },
    [performSearch]
  )

  // Handle search input focus
  const handleSearchFocus = useCallback(() => {
    setSearchFocused(true)
    if (searchQuery.length >= 2) {
      setSearchOpen(true)
    }
  }, [searchQuery])

  // Handle search input blur
  const handleSearchBlur = useCallback(() => {
    setSearchFocused(false)
    // Delay closing to allow click on results
    setTimeout(() => {
      setSearchOpen(false)
    }, 150)
  }, [])

  // Clear search
  const clearSearch = useCallback(() => {
    setSearchQuery('')
    setSearchResults({ leads: [], runners: [], campaigns: [] })
    setSearchOpen(false)
  }, [])

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'lead':
        return <div className="w-2 h-2 bg-emerald-500 rounded-full" />
      case 'system':
        return <div className="w-2 h-2 bg-blue-500 rounded-full" />
      case 'alert':
        return <div className="w-2 h-2 bg-amber-500 rounded-full" />
      default:
        return <div className="w-2 h-2 bg-zinc-500 rounded-full" />
    }
  }

  return (
    <header className="sticky top-0 z-50 bg-zinc-950/80 backdrop-blur-md border-b border-zinc-800">
      <div className="flex items-center justify-between px-6 py-3">
        {/* Project Switcher */}
        <div className="relative mr-6" ref={projectDropdownRef}>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setProjectDropdownOpen(!projectDropdownOpen)}
            className="flex items-center gap-2 px-3 py-2 hover:bg-zinc-800/50 transition-colors border border-zinc-700"
          >
            {activeProject ? (
              <>
                {activeProject.tipe_proyek === 'KOMERSIL' ? (
                  <Crown className="h-4 w-4 text-yellow-500" />
                ) : (
                  <Shield className="h-4 w-4 text-blue-500" />
                )}
                <span className="text-sm font-medium text-zinc-100">{activeProject.nama_proyek}</span>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    activeProject.tipe_proyek === 'KOMERSIL'
                      ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                      : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                  } border`}
                >
                  {activeProject.tipe_proyek}
                </span>
              </>
            ) : (
              <>
                <Building className="h-4 w-4 text-zinc-400" />
                <span className="text-sm text-zinc-400">No Project Selected</span>
              </>
            )}
            <ChevronDown className="h-3 w-3 text-zinc-400" />
          </Button>

          {/* Project Dropdown */}
          {projectDropdownOpen && (
            <div className="absolute left-0 mt-2 w-80 bg-zinc-900 border border-zinc-700 rounded-lg shadow-2xl overflow-hidden z-50">
              <div className="p-3 border-b border-zinc-800">
                <h3 className="text-sm font-semibold text-zinc-100">Select Project</h3>
                <p className="text-xs text-zinc-500 mt-1">
                  {projects.length} project{projects.length !== 1 ? 's' : ''} available
                </p>
              </div>

              <div className="max-h-64 overflow-y-auto">
                {projects.map(project => (
                  <div
                    key={project.id}
                    className="p-3 border-b border-zinc-800 hover:bg-zinc-800/30 transition-colors cursor-pointer"
                    onClick={() => {
                      setActiveProject(project.id)
                      setProjectDropdownOpen(false)
                    }}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          {project.tipe_proyek === 'KOMERSIL' ? (
                            <Crown className="h-4 w-4 text-yellow-500" />
                          ) : (
                            <Shield className="h-4 w-4 text-blue-500" />
                          )}
                          <div className="text-sm font-medium text-zinc-100">{project.nama_proyek}</div>
                        </div>
                        <div className="text-xs text-zinc-400 mt-1">
                          {project.lokasi} • RP {(project.harga_start / 1000000).toFixed(1)}M
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          <span
                            className={`text-xs px-2 py-1 rounded-full ${
                              project.tipe_proyek === 'KOMERSIL'
                                ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                                : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                            } border`}
                          >
                            {project.tipe_proyek}
                          </span>
                          <span className="text-xs text-zinc-500">{project.leads_count} leads</span>
                          {project.is_active && (
                            <span className="text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-400 border-green-500/30 border">
                              Active
                            </span>
                          )}
                        </div>
                      </div>
                      {activeProjectId === project.id && <div className="w-2 h-2 bg-green-500 rounded-full" />}
                    </div>
                  </div>
                ))}

                {projects.length === 0 && (
                  <div className="p-4 text-center text-zinc-400">
                    <div className="text-sm">No projects found</div>
                    <div className="text-xs mt-1">Create your first project to get started</div>
                  </div>
                )}
              </div>

              <div className="p-2 border-t border-zinc-800">
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full justify-center text-xs text-zinc-400 hover:text-zinc-100"
                  onClick={() => {
                    // Navigate to projects page
                    window.location.href = '/projects'
                  }}
                >
                  Manage Projects
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Left Section - Omni Search */}
        <div className="flex-1 max-w-xl" ref={searchRef}>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400" />
            <Input
              type="text"
              placeholder="Search leads, campaigns, or command... (Ctrl+K)"
              value={searchQuery}
              onChange={handleSearchChange}
              onFocus={handleSearchFocus}
              onBlur={handleSearchBlur}
              className={cn(
                'pl-10 pr-10 py-2 bg-zinc-900/50 border-zinc-700 text-zinc-100 placeholder-zinc-500',
                'focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500',
                'transition-all duration-200',
                searchFocused && 'ring-2 ring-emerald-500/50 border-emerald-500'
              )}
            />
            {/* Clear button or keyboard shortcut */}
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
              {searchQuery ? (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearSearch}
                  className="p-1 h-6 w-6 hover:bg-zinc-800/50 transition-colors"
                >
                  <X className="h-3 w-3 text-zinc-400" />
                </Button>
              ) : (
                <>
                  <kbd className="px-1.5 py-0.5 text-xs bg-zinc-800 border border-zinc-700 rounded text-zinc-400">
                    Ctrl
                  </kbd>
                  <kbd className="px-1.5 py-0.5 text-xs bg-zinc-800 border border-zinc-700 rounded text-zinc-400">
                    K
                  </kbd>
                </>
              )}
            </div>

            {/* Search Results Dropdown */}
            {searchOpen && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-lg shadow-2xl max-h-96 overflow-y-auto z-50">
                {isSearching ? (
                  <div className="p-4 text-center text-zinc-400">
                    <div className="inline-flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                      Searching...
                    </div>
                  </div>
                ) : (
                  <>
                    {/* Leads Section */}
                    {searchResults.leads.length > 0 && (
                      <div className="p-2">
                        <div className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                          <Home className="h-3 w-3" />
                          Leads
                        </div>
                        {searchResults.leads.map(lead => (
                          <div
                            key={lead.id}
                            className="px-3 py-2 hover:bg-zinc-800/50 cursor-pointer transition-colors rounded"
                            onClick={() => {
                              // Handle lead selection
                              clearSearch()
                            }}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1">
                                <div className="text-sm font-medium text-zinc-100">{lead.title}</div>
                                <div className="text-xs text-zinc-400 mt-1">{lead.description}</div>
                                <div className="flex items-center gap-2 mt-1">
                                  <span className="text-xs text-emerald-400 font-medium">{lead.price}</span>
                                  <span className="text-xs text-zinc-500">• {lead.location}</span>
                                  <span className="text-xs text-zinc-500">• Score: {lead.score}/10</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Runners Section */}
                    {searchResults.runners.length > 0 && (
                      <div className="p-2">
                        <div className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-blue-400 uppercase tracking-wider">
                          <Target className="h-3 w-3" />
                          Runners
                        </div>
                        {searchResults.runners.map(runner => (
                          <div
                            key={runner.id}
                            className="px-3 py-2 hover:bg-zinc-800/50 cursor-pointer transition-colors rounded"
                            onClick={() => {
                              // Handle runner selection
                              clearSearch()
                            }}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1">
                                <div className="text-sm font-medium text-zinc-100">{runner.name}</div>
                                <div className="text-xs text-zinc-400 mt-1">{runner.description}</div>
                                <div className="flex items-center gap-2 mt-1">
                                  <span
                                    className={`text-xs px-2 py-1 rounded-full ${
                                      runner.status === 'running'
                                        ? 'bg-emerald-500/20 text-emerald-400'
                                        : 'bg-zinc-700 text-zinc-400'
                                    }`}
                                  >
                                    {runner.status}
                                  </span>
                                  <span className="text-xs text-zinc-500">• {runner.category}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Campaigns Section */}
                    {searchResults.campaigns.length > 0 && (
                      <div className="p-2">
                        <div className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-purple-400 uppercase tracking-wider">
                          <TrendingUp className="h-3 w-3" />
                          Campaigns
                        </div>
                        {searchResults.campaigns.map(campaign => (
                          <div
                            key={campaign.id}
                            className="px-3 py-2 hover:bg-zinc-800/50 cursor-pointer transition-colors rounded"
                            onClick={() => {
                              // Handle campaign selection
                              clearSearch()
                            }}
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div className="flex-1">
                                <div className="text-sm font-medium text-zinc-100">{campaign.title}</div>
                                <div className="text-xs text-zinc-400 mt-1">{campaign.description}</div>
                                <div className="flex items-center gap-2 mt-1">
                                  <span className="text-xs text-purple-400 font-medium">
                                    {campaign.discount || campaign.interest_rate}
                                  </span>
                                  <span className="text-xs text-zinc-500">• Until {campaign.valid_until}</span>
                                  <span
                                    className={`text-xs px-2 py-1 rounded-full ${
                                      campaign.status === 'active'
                                        ? 'bg-purple-500/20 text-purple-400'
                                        : 'bg-zinc-700 text-zinc-400'
                                    }`}
                                  >
                                    {campaign.status}
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* No Results */}
                    {searchResults.leads.length === 0 &&
                      searchResults.runners.length === 0 &&
                      searchResults.campaigns.length === 0 && (
                        <div className="p-4 text-center text-zinc-400">
                          <div className="text-sm">No results found</div>
                          <div className="text-xs mt-1">Try searching for leads, runners, or campaigns</div>
                        </div>
                      )}
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Section - Actions & Profile */}
        <div className="flex items-center gap-4 ml-6">
          {/* Notifications */}
          <div className="relative" ref={notificationRef}>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setNotificationOpen(!notificationOpen)}
              className="relative p-2 hover:bg-zinc-800/50 transition-colors"
            >
              <Bell className="h-4 w-4 text-zinc-300" />
              {/* Unread indicator */}
              <div className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            </Button>

            {/* Notification Dropdown */}
            {notificationOpen && (
              <div className="absolute right-0 mt-2 w-80 bg-zinc-900 border border-zinc-700 rounded-lg shadow-2xl overflow-hidden">
                <div className="p-3 border-b border-zinc-800">
                  <h3 className="text-sm font-semibold text-zinc-100">Notifications</h3>
                  <p className="text-xs text-zinc-500 mt-1">3 unread messages</p>
                </div>

                <div className="max-h-96 overflow-y-auto">
                  {notifications.map(notification => (
                    <div
                      key={notification.id}
                      className="p-3 border-b border-zinc-800 hover:bg-zinc-800/30 transition-colors cursor-pointer"
                    >
                      <div className="flex items-start gap-3">
                        {getNotificationIcon(notification.type)}
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-zinc-100 truncate">{notification.title}</p>
                          <p className="text-xs text-zinc-400 mt-1 line-clamp-2">{notification.message}</p>
                          <p className="text-xs text-zinc-500 mt-2">{notification.time}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="p-2 border-t border-zinc-800">
                  <Button variant="ghost" size="sm" className="w-full text-xs text-zinc-400 hover:text-zinc-100">
                    Mark all as read
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* System Status */}
          <div className="flex items-center gap-2 px-3 py-1.5 bg-zinc-900/50 border border-zinc-700 rounded-full">
            <div className="flex items-center gap-1.5">
              <Circle className={cn('h-2 w-2 fill-current', systemOnline ? 'text-emerald-500' : 'text-emerald-700')} />
              <span className="text-xs text-zinc-400">System: {systemOnline ? 'Online' : 'Syncing...'}</span>
            </div>
          </div>

          {/* User Profile */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-zinc-100">Elite Hunter</p>
              <p className="text-xs text-zinc-500">Administrator</p>
            </div>
            <Avatar className="h-8 w-8 border border-zinc-700">
              <AvatarFallback className="bg-emerald-600 text-zinc-100 text-sm font-semibold">EH</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  )
}

export default TopHeader
