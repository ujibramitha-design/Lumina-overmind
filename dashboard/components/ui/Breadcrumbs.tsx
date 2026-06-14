/**
 * LUMINA OVERMIND SYSTEM - Breadcrumbs Component
 *
 * Provides navigation breadcrumbs with proper accessibility and state management
 */

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { ChevronRight, Home } from 'lucide-react'

interface BreadcrumbItem {
  label: string
  href?: string
  icon?: React.ElementType
}

interface BreadcrumbsProps {
  items?: BreadcrumbItem[]
  className?: string
  showHome?: boolean
  separator?: React.ReactNode
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  items,
  className,
  showHome = true,
  separator = <ChevronRight className="w-4 h-4" />,
}) => {
  const pathname = usePathname()

  // Generate breadcrumbs from pathname if not provided
  const generatedItems = React.useMemo((): BreadcrumbItem[] => {
    if (items) return items

    const pathSegments = pathname.split('/').filter(Boolean)
    const breadcrumbs: BreadcrumbItem[] = []

    pathSegments.forEach((segment, index) => {
      const href = '/' + pathSegments.slice(0, index + 1).join('/')
      const label = segment
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')

      breadcrumbs.push({
        label,
        href: index < pathSegments.length - 1 ? href : undefined,
      })
    })

    return breadcrumbs
  }, [pathname, items])

  const allItems = React.useMemo(() => {
    if (!showHome) return generatedItems

    return [{ label: 'Dashboard', href: '/dashboard', icon: Home }, ...generatedItems]
  }, [generatedItems, showHome])

  if (allItems.length <= 1) return null

  return (
    <nav aria-label="Breadcrumb navigation" className={cn('flex items-center space-x-1 text-sm', className)}>
      <ol className="flex items-center space-x-1">
        {allItems.map((item, index) => (
          <li key={`${item.href}-${index}`} className="flex items-center">
            {index > 0 && (
              <span className="mx-1 text-zinc-500" aria-hidden="true">
                {separator}
              </span>
            )}

            {item.href ? (
              <Link
                href={item.href}
                className={cn(
                  'flex items-center space-x-1 transition-colors',
                  'hover:text-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 focus:ring-offset-zinc-900 rounded-sm',
                  index === allItems.length - 1 ? 'text-zinc-100 font-medium' : 'text-zinc-400'
                )}
                aria-current={index === allItems.length - 1 ? 'page' : undefined}
              >
                {item.icon && <item.icon className="w-4 h-4" />}
                <span>{item.label}</span>
              </Link>
            ) : (
              <span
                className={cn(
                  'flex items-center space-x-1',
                  index === allItems.length - 1 ? 'text-zinc-100 font-medium' : 'text-zinc-400'
                )}
                aria-current="page"
              >
                {item.icon && <item.icon className="w-4 h-4" />}
                <span>{item.label}</span>
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}

// Breadcrumb item component for custom usage
export const BreadcrumbItem: React.FC<{
  label: string
  href?: string
  icon?: React.ElementType
  isLast?: boolean
}> = ({ label, href, icon: Icon, isLast }) => {
  return (
    <span className="flex items-center space-x-1">
      {Icon && <Icon className="w-4 h-4" />}
      <span className={cn(isLast ? 'text-zinc-100 font-medium' : 'text-zinc-400')}>{label}</span>
    </span>
  )
}

// Hook for generating breadcrumbs programmatically
export const useBreadcrumbs = (customItems?: BreadcrumbItem[]) => {
  const pathname = usePathname()

  return React.useMemo(() => {
    if (customItems) return customItems

    const pathSegments = pathname.split('/').filter(Boolean)
    const breadcrumbs: BreadcrumbItem[] = []

    pathSegments.forEach((segment, index) => {
      const href = '/' + pathSegments.slice(0, index + 1).join('/')
      const label = segment
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')

      breadcrumbs.push({
        label,
        href: index < pathSegments.length - 1 ? href : undefined,
      })
    })

    return breadcrumbs
  }, [pathname, customItems])
}

export default Breadcrumbs
