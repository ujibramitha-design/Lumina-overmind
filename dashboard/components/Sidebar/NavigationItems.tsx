/**
 * LUMINA OVERMIND SYSTEM - Sidebar Navigation Items
 *
 * Extracted navigation items configuration for better maintainability
 */

import {
  Radar,
  Users,
  Building2,
  Target,
  TrendingUp,
  RefreshCw,
  Network,
  DollarSign,
  Palette,
  FileText,
  Layout,
  Shield,
  Terminal,
  Lock,
  Clock,
  Image,
  Eye,
} from 'lucide-react'

export interface NavItem {
  title: string
  href?: string
  icon?: React.ElementType
  items?: NavItem[]
  badge?: string
  adminOnly?: boolean
}

export const navigationItems: NavItem[] = [
  {
    title: '🔍 Intelligence Hub',
    icon: Radar,
    items: [
      {
        title: 'Lead Generation',
        href: '/dashboard/leads',
        icon: Users,
        badge: 'AI',
      },
      {
        title: 'Market Analysis',
        href: '/dashboard/analysis',
        icon: TrendingUp,
      },
      {
        title: 'Property Intelligence',
        href: '/dashboard/property',
        icon: Building2,
      },
      {
        title: 'Target Scouting',
        href: '/dashboard/scouting',
        icon: Target,
        adminOnly: true,
      },
    ],
  },
  {
    title: '⚡ Automation Engine',
    icon: RefreshCw,
    items: [
      {
        title: 'Workflow Builder',
        href: '/dashboard/workflows',
        icon: Layout,
        badge: 'NEW',
      },
      {
        title: 'Task Scheduler',
        href: '/dashboard/scheduler',
        icon: Clock,
      },
      {
        title: 'API Integrations',
        href: '/dashboard/integrations',
        icon: Network,
      },
    ],
  },
  {
    title: '📊 Analytics & Reports',
    icon: FileText,
    items: [
      {
        title: 'Performance Metrics',
        href: '/dashboard/metrics',
        icon: TrendingUp,
      },
      {
        title: 'Lead Conversion',
        href: '/dashboard/conversion',
        icon: Target,
      },
      {
        title: 'ROI Analysis',
        href: '/dashboard/roi',
        icon: DollarSign,
      },
    ],
  },
  {
    title: '🎨 Creative Studio',
    icon: Palette,
    items: [
      {
        title: 'Visual Generator',
        href: '/dashboard/visual',
        icon: Palette,
        badge: 'AI',
      },
      {
        title: 'Brochure Designer',
        href: '/dashboard/brochure',
        icon: Layout,
      },
      {
        title: 'VR Experience',
        href: '/dashboard/vr',
        icon: Eye,
      },
    ],
  },
  {
    title: '🔐 System Admin',
    icon: Shield,
    adminOnly: true,
    items: [
      {
        title: 'User Management',
        href: '/dashboard/users',
        icon: Users,
      },
      {
        title: 'Security Settings',
        href: '/dashboard/security',
        icon: Lock,
      },
      {
        title: 'System Logs',
        href: '/dashboard/logs',
        icon: FileText,
      },
      {
        title: 'API Documentation',
        href: '/dashboard/api-docs',
        icon: Terminal,
      },
    ],
  },
]

// Helper function to filter navigation items based on user role
export const filterNavigationItems = (items: NavItem[], isAdmin: boolean): NavItem[] => {
  return items
    .filter(item => !item.adminOnly || isAdmin)
    .map(item => ({
      ...item,
      items: item.items?.filter(subItem => !subItem.adminOnly || isAdmin),
    }))
    .filter(item => item.items && item.items.length > 0)
}
