'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useTranslations } from 'next-intl'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useIsAdmin } from '@/lib/store'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { useMobileMenu } from '@/lib/mobile-menu-context'
import { LanguageSwitcher } from '@/components/LanguageSwitcher'
import {
  ChevronDown,
  ChevronRight,
  Radar,
  Users,
  Building2,
  Target,
  TrendingUp,
  Search,
  RefreshCw,
  Network,
  DollarSign,
  Palette,
  FileText,
  Layout,
  Shield,
  Terminal,
  FileCheck,
  Lock,
  Menu,
  X,
} from 'lucide-react'

interface NavItem {
  title: string
  href?: string
  icon?: React.ElementType
  items?: NavItem[]
  badge?: string
  adminOnly?: boolean
}

interface SidebarProps {
  className?: string
  collapsed?: boolean
  onCollapse?: () => void
}

export function Sidebar({ className, collapsed = false, onCollapse }: SidebarProps) {
  const pathname = usePathname()
  const isAdmin = useIsAdmin()
  const t = useTranslations('navigation')
  const [openItems, setOpenItems] = useState<Set<string>>(new Set(['Intelligence Hub']))
  const { isMobileMenuOpen, setIsMobileMenuOpen } = useMobileMenu()

  const navigationItems: NavItem[] = [
    {
      title: t('intelligenceHub'),
      icon: Radar,
      items: [
        {
          title: t('liveRadar'),
          href: '/intelligence/live-radar',
          icon: Target,
          badge: 'LIVE',
        },
        {
          title: t('leadsCRM'),
          href: '/intelligence/leads-crm',
          icon: Users,
          badge: '25',
        },
        {
          title: t('urbanForesight'),
          href: '/intelligence/urban-foresight',
          icon: Building2,
        },
        {
          title: t('competitorIntel'),
          href: '/intelligence/competitor-intel',
          icon: Target,
        },
      ],
    },
    {
      title: t('growthAds'),
      icon: TrendingUp,
      items: [
        {
          title: t('campaignManager'),
          href: '/growth/campaign-manager',
          icon: TrendingUp,
        },
        {
          title: t('organicSEO'),
          href: '/growth/organic-seo',
          icon: Search,
        },
        {
          title: t('retargeting'),
          href: '/growth/retargeting',
          icon: RefreshCw,
        },
      ],
    },
    {
      title: t('partnerEcosystem'),
      icon: Network,
      items: [
        {
          title: t('brokerNetwork'),
          href: '/partners/broker-network',
          icon: Network,
        },
        {
          title: t('commissionTracker'),
          href: '/partners/commission-tracker',
          icon: DollarSign,
        },
      ],
    },
    {
      title: t('creativeStudio'),
      icon: Palette,
      items: [
        {
          title: t('contentGrid'),
          href: '/creative/content-grid',
          icon: Layout,
        },
        {
          title: t('autoBrochure'),
          href: '/creative/auto-brochure',
          icon: FileText,
        },
        {
          title: t('templateMaster'),
          href: '/creative/template-master',
          icon: Palette,
        },
      ],
    },
    {
      title: t('governance'),
      icon: Shield,
      items: [
        {
          title: 'System Logs',
          href: '/governance/system-logs',
          icon: FileCheck,
        },
        {
          title: 'Crisis Terminal',
          href: '/governance/crisis-terminal',
          icon: Terminal,
        },
        {
          title: 'Compliance',
          href: '/governance/compliance',
          icon: Shield,
        },
      ],
    },
    {
      title: t('classifiedVault'),
      icon: Lock,
      href: '/settings/classified-vault',
      badge: 'ADMIN',
      adminOnly: true,
    },
  ]

  const toggleItem = (title: string) => {
    const newOpenItems = new Set(openItems)
    if (newOpenItems.has(title)) {
      newOpenItems.delete(title)
    } else {
      newOpenItems.add(title)
    }
    setOpenItems(newOpenItems)
  }

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === href
    }
    return pathname.startsWith(href)
  }

  const renderNavItem = (item: NavItem, level: number = 0) => {
    // Hide admin-only items if user is not admin
    if (item.adminOnly && !isAdmin) {
      return null
    }

    const hasSubItems = item.items && item.items.length > 0
    const isOpen = openItems.has(item.title)
    const Icon = item.icon

    if (hasSubItems) {
      return (
        <Collapsible key={item.title} open={isOpen} onOpenChange={() => toggleItem(item.title)} className="w-full">
          <CollapsibleTrigger asChild>
            <Button
              variant="ghost"
              className={cn(
                'w-full justify-between text-left hover:bg-zinc-900 hover:text-emerald-500 transition-all duration-200',
                'px-3 py-2 rounded-lg font-medium',
                collapsed && 'justify-center px-2 py-2'
              )}
            >
              <div className="flex items-center gap-3">
                {Icon && (
                  <Icon className={cn('h-5 w-5 transition-colors', isOpen ? 'text-emerald-500' : 'text-zinc-400')} />
                )}
                {!collapsed && (
                  <span className={cn('text-sm transition-colors', isOpen ? 'text-emerald-500' : 'text-zinc-300')}>
                    {item.title}
                  </span>
                )}
              </div>
              {!collapsed && (
                <ChevronDown
                  className={cn(
                    'h-4 w-4 transition-transform duration-200',
                    isOpen ? 'rotate-180 text-emerald-500' : 'text-zinc-500'
                  )}
                />
              )}
            </Button>
          </CollapsibleTrigger>
          <CollapsibleContent className="space-y-1 mt-1">
            {!collapsed &&
              item.items?.map(subItem => (
                <Link
                  key={subItem.href}
                  href={subItem.href || '#'}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200',
                    'hover:bg-zinc-900 hover:text-emerald-500',
                    isActive(subItem.href || '')
                      ? 'bg-zinc-900 text-emerald-500 border-l-2 border-emerald-500'
                      : 'text-zinc-400'
                  )}
                >
                  {subItem.icon && <subItem.icon className="h-4 w-4" />}
                  <span className="flex-1">{subItem.title}</span>
                  {subItem.badge && (
                    <span
                      className={cn(
                        'px-2 py-0.5 text-xs rounded-full font-medium',
                        subItem.badge === 'LIVE'
                          ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                          : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      )}
                    >
                      {subItem.badge}
                    </span>
                  )}
                </Link>
              ))}
          </CollapsibleContent>
        </Collapsible>
      )
    }

    return (
      <Link
        key={item.href}
        href={item.href || '#'}
        className={cn(
          'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200',
          'hover:bg-zinc-900 hover:text-emerald-500',
          isActive(item.href || '') ? 'bg-zinc-900 text-emerald-500 border-l-2 border-emerald-500' : 'text-zinc-400'
        )}
      >
        {Icon && <Icon className="h-5 w-5" />}
        {!collapsed && <span className="flex-1">{item.title}</span>}
        {item.badge && !collapsed && (
          <span
            className={cn(
              'px-2 py-0.5 text-xs rounded-full font-medium',
              item.badge === 'LIVE'
                ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
            )}
          >
            {item.badge}
          </span>
        )}
      </Link>
    )
  }

  return (
    <>
      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 xl:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-label="Close sidebar"
        />
      )}
      
      {/* Sidebar */}
      <div
        className={cn(
          'flex flex-col h-full bg-zinc-950 border-r border-zinc-800 transition-all duration-300 fixed xl:relative z-50',
          collapsed ? 'w-16' : 'w-64',
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full xl:translate-x-0',
          className
        )}
      >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-zinc-800">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-600 rounded-lg flex items-center justify-center">
              <Target className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-bold text-white">Elite Hunter</span>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => {
            onCollapse?.()
            setIsMobileMenuOpen(false)
          }}
          className={cn(
            'text-zinc-400 hover:text-emerald-500 hover:bg-zinc-900 transition-colors',
            collapsed && 'mx-auto'
          )}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <Menu className="h-4 w-4" /> : <X className="h-4 w-4" />}
        </Button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">{navigationItems.map(item => renderNavItem(item))}</nav>

      {/* Footer */}
      <div className="p-4 border-t border-zinc-800">
        {!collapsed && (
          <div className="space-y-3">
            <LanguageSwitcher />
            <div className="flex items-center gap-2 text-xs text-zinc-500">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
              <span>System Online</span>
            </div>
            <div className="text-xs text-zinc-600">Version 2.0.1</div>
          </div>
        )}
        {collapsed && (
          <div className="flex justify-center">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          </div>
        )}
      </div>
    </div>
    </>
  )
}

export default Sidebar
